import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Requesting all users' data
@app.route('/users/', methods=['GET'])
def get_all_users():
    # Checking for errors connecting to or accessing the database
    try:
        # Connecting to database
        conn = sqlite3.connect('hackers.db')
        cursor = conn.cursor()

        # Query for all users' personal info
        cursor.execute('SELECT * FROM hackers;')
        hackers = cursor.fetchall()
    except sqlite3.OperationalError as err:
        conn.close()
        return f"Operational Error: {err}", 500
    
    all_users = {} # Where organized data will be stored then converted into a JSON

    # Iterating over each hacker
    for hacker in hackers:
        hid = hacker[0] # hacker = (hacker_id, name, company, email, phone)

        # Collect and organize their skills
        try:
            cursor.execute('SELECT skill, rating FROM hacker_skills WHERE ? = hacker_id;', (hid,))
            skills_of_hacker = cursor.fetchall()

            cursor.execute('SELECT event, rating FROM hacker_events WHERE ? = hacker_id;', (hid,))
            events_attended = cursor.fetchall()

        except sqlite3.OperationalError as err:
            conn.close()
            return f"Operational Error: {err}", 500

        # Add the hacker's info to all_users to be JSONified later
        all_users[hid] = {
            "1. name": hacker[1],
            "2. company": hacker[2],
            "3. email": hacker[3],
            "4. phone": hacker[4],
            "5. skills": skills_of_hacker,
            "6. events": events_attended
        }
        
    conn.close() # Done accessing database

    return jsonify(all_users) # Return the data as JSON

# Requesting a specific user's data
@app.route('/users/<int:hacker_id>/', methods=['GET'])
def get_one_user(hacker_id):
    # Checking for errors connecting to or accessing the database
    try:
        # Connecting to database
        conn = sqlite3.connect('hackers.db')
        cursor = conn.cursor()

        # Querying for the hacker's personal data
        cursor.execute('SELECT * FROM hackers WHERE hacker_id = ?;', (hacker_id,))
        results = cursor.fetchall()

        # Checking if the query found 1 hacker or not
        if len(results) != 1:
            conn.close()
            return "Hacker not found", 404
        else:
            hacker = results[0]

        # Querying their skills
        cursor.execute('SELECT skill, rating FROM hacker_skills WHERE hacker_id = ?;', (hacker_id,))
        skills = cursor.fetchall()

        # Querying their events
        cursor.execute('SELECT event, rating FROM hacker_events WHERE hacker_id = ?;', (hacker_id,))
        events = cursor.fetchall()

        conn.close() # Done using the database
    
    except sqlite3.OperationalError as err:
        conn.close()
        return f"Operational Error: {err}", 500

    # Combining all of it to JSONify
    one_user = {
            "1. name": hacker[1],
            "2. company": hacker[2],
            "3. email": hacker[3],
            "4. phone": hacker[4],
            "5. skills": skills,
            "6. events": events
    }

    return jsonify(one_user) # Done

# Updates the data of a user if given a valid JSON file, then returns the updated version
@app.route('/users/<int:hacker_id>/', methods=['PUT'])
def update_user(hacker_id):
    # Checking if the JSON is valid
    try:
        updated_data = request.json
        if updated_data is None:
            return "JSON file not found", 404
    except Exception as err:
        return f"Problem accessing the JSON\n{err}", 400
    
    # Checking for errors connecting to or accessing the database
    try:
        # Connecting to database
        conn = sqlite3.connect('hackers.db')
        cursor = conn.cursor()

        # Querying for the hacker's personal data
        cursor.execute('SELECT COUNT(*) FROM hackers WHERE hacker_id = ?;', (hacker_id,))
        results = cursor.fetchall()

        # Checking if the query found 1 hacker or not
        if results[0] != (1,):
            conn.close()
            return "Hacker not found", 404

    except sqlite3.OperationalError as err:
        conn.close()
        return f"Operational Error: {err}", 500
    
    # Updating the database
    try:
        for data in updated_data:
            # For updating hackers
            if data == 'name':
                cursor.execute('UPDATE hackers SET name = ? WHERE hacker_id = ?;', (updated_data[data], hacker_id))
            elif data == 'company':
                cursor.execute('UPDATE hackers SET company = ? WHERE hacker_id = ?;', (updated_data[data], hacker_id))
            elif data == 'email':
                cursor.execute('UPDATE hackers SET email = ? WHERE hacker_id = ?;', (updated_data[data], hacker_id))
            elif data == 'phone':
                cursor.execute('UPDATE hackers SET phone = ? WHERE hacker_id = ?;', (updated_data[data], hacker_id))
            
            # For updating hacker_skills
            elif data == 'skills':
                # Querying for all current skills
                cursor.execute('SELECT skill FROM hacker_skills WHERE hacker_id = ?;', (hacker_id,))
                current_skills = cursor.fetchall()
                
                # Checking every skill to change
                for skl in updated_data['skills']:
                    # Must check if a user already has a skill or not
                    if (skl['skill'],) in current_skills: # Updating a skill
                        cursor.execute('UPDATE hacker_skills SET rating = ? WHERE hacker_id = ?;', (skl['rating'], hacker_id))
                    else: # Adding a skill they didn't have yet
                        cursor.execute('''
                            INSERT INTO hacker_skills (hacker_id, skill, rating)
                            VALUES (?, ?, ?);''', (hacker_id, skl['skill'], skl['rating']))
                        
            # For updating hacker_events
            elif data == 'events':
                # Querying for all their attended events
                cursor.execute('SELECT event FROM hacker_events WHERE hacker_id = ?;', (hacker_id,))
                attended_events = cursor.fetchall()

                # Checking every skill to change
                for evt in updated_data['events']:
                    # Must check if a user rated this event
                    if (len(evt) == 2): # rated
                        if (evt['event'],) in attended_events: # Updating event rating
                            cursor.execute('UPDATE hacker_events SET rating = ? WHERE hacker_id = ?;', (evt['rating'], hacker_id))
                        else:
                            cursor.execute('''
                                INSERT INTO hacker_events (hacker_id, event, rating)
                                VALUES (?, ?, ?);''', (hacker_id, evt['event'], evt['rating']))
                    elif (len(evt) == 1): # unrated
                        if (evt['event'],) in attended_events: # Updating event rating but given no rating, so skip
                            continue
                        else:
                            cursor.execute('''
                                INSERT INTO hacker_events (hacker_id, event)
                                VALUES (?, ?);''', (hacker_id, evt['event']))
        
        # Done modifying the database
        conn.commit()
        conn.close()
        
    except sqlite3.OperationalError as err:
        conn.close()
        return f"Operational Error: {err}", 500

    return get_one_user(hacker_id) # Return all their data

# Returns a list of skills and their frequency
@app.route('/skills/', methods=['GET'])
def get_skills():
    # Extracting min_frequency and max_frequency parameters from the query string
    # Given as strings first
    min_frq = request.args.get('min_frequency')
    max_frq = request.args.get('max_frequency')
    
    # Can't have negative frequency
    if min_frq is None:
        min_frq = 0
    else:
        min_frq = abs(int(min_frq))

    try:
        # Connecting to database
        conn = sqlite3.connect('hackers.db')
        cursor = conn.cursor()

        # User has option of not providing any of the bounds.
        # Given no bounds, show frequency of all skills
        if max_frq == None:
            cursor.execute('''
                SELECT skill, COUNT(skill) AS frequency
                FROM hacker_skills
                GROUP BY skill
                HAVING frequency >= ?
                ORDER BY frequency DESC;''', (min_frq,))
        
        # If given both, apply both
        else:
            max_frq = abs(int(max_frq))
            cursor.execute('''
                SELECT skill, COUNT(skill) AS frequency
                FROM hacker_skills
                GROUP BY skill
                HAVING frequency BETWEEN ? AND ?
                ORDER BY frequency DESC;''', (min(min_frq, max_frq), max(min_frq, max_frq)))
        
        skills = cursor.fetchall() # Final results

        conn.close() # Done
    
    except sqlite3.OperationalError as err:
        conn.close()
        return f"Operational Error: Could not connect to the database\n{err}", 500

    except TypeError as err:
        conn.close()
        return f"Type Error: Invalid query string parameter type given\n{err}", 400
    
    return jsonify(skills) # Return JSONified

@app.route('/events/', methods=['GET'])
def get_events():
    # Extracting parameters from the query string
    # Given as strings first
    min_frq = request.args.get('min_frequency')
    max_frq = request.args.get('max_frequency')
    min_rtg = request.args.get('min_rating')
    max_rtg = request.args.get('max_rating')

    if min_frq is None:
        min_frq = 0
    else:
        min_frq = abs(int(min_frq))
    if min_rtg is None:
        min_rtg = 0
    else:
        min_rtg = abs(int(min_rtg))
    if max_rtg is None:
        max_rtg = 10
    else:
        max_rtg = abs(int(max_rtg))

    try:
        # Connecting to database
        conn = sqlite3.connect('hackers.db')
        cursor = conn.cursor()

        # User has option of not providing any of the bounds.
        # Given no bounds, show frequency of all skills
        if max_frq == None:
            cursor.execute('''
                    SELECT event, rating, COUNT(event) as frq, AVG(rating) AS avg
                    FROM hacker_events
                    WHERE rating IS NOT NULL
                    GROUP BY event
                    HAVING avg BETWEEN ? AND ?
                        AND frq >= ?
                    ORDER BY avg DESC;''', (min(min_rtg, max_rtg), max(min_rtg, max_rtg), min_frq))
        
        # If given both, apply both
        else:
            max_frq = abs(int(max_frq))
            cursor.execute('''
                SELECT event, rating, COUNT(event) as frq, AVG(rating) AS avg
                FROM hacker_events
                WHERE rating IS NOT NULL
                GROUP BY event
                HAVING frq BETWEEN ? AND ?
                    AND avg BETWEEN ? AND ?
                ORDER BY avg DESC;''', (min(min_frq, max_frq), max(min_frq, max_frq), min(min_rtg, max_rtg), max(min_rtg, max_rtg)))
            
        rated_events = cursor.fetchall()

        if max_frq == None:
            cursor.execute('''
                    SELECT event, COUNT(event) AS frq
                    FROM hacker_events
                    WHERE rating IS NULL
                    GROUP BY event
                    HAVING frq >= ?;''', (min_frq,))
        
        # If given both, apply both
        else:
            max_frq = abs(int(max_frq))
            cursor.execute('''
                SELECT event, COUNT(event) as frq
                FROM hacker_events
                WHERE rating IS NULL
                GROUP BY event
                HAVING frq BETWEEN ? AND ?;''', (min(min_frq, max_frq), max(min_frq, max_frq)))

        unrated_events = cursor.fetchall()

        conn.close() # Done
    
    except sqlite3.OperationalError as err:
        conn.close()
        return f"Operational Error: Could not connect to the database\n{err}", 500

    except TypeError as err:
        conn.close()
        return f"Type Error: Invalid query string parameter type given\n{err}", 400

    return jsonify(rated_events + unrated_events) # Return JSONified

if __name__ == '__main__':
    app.run(debug=True)
