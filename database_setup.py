import sqlite3, requests, json

# This is designed to transfer files from a JSON to an SQL database
# It organizes data into 2 tables, hacker and hacker_skills.
# hacker consists of a person's: hacker_id (PRIMARY), name, company, email, and phone
# hacker_skill consists of: hacker_id (FOREIGN), skill, and rating, where hacker_id is used to link the 2 tables.
def get_db():
    try:
        # HTTP request for the JSON
        json_url = "https://gist.githubusercontent.com/DanielYu842/607c1ae9c63c4e83e38865797057ff8f/raw/b84b8bce73fadb341258e86265a6091779908344/HTN_2023_BE_Challenge_Data.json"
        resp = requests.get(json_url)
        if resp.status_code == 200:
            data = json.loads(resp.text)
        else:
            raise requests.HTTPError

        # Connecting to database, hackers.db (creates it if doesn't exist yet)
        conn = sqlite3.connect('hackers.db')
        cursor = conn.cursor()

        # Setting up the 2 tables
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS hackers (
                hacker_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                name TEXT,
                company TEXT,
                email TEXT,
                phone TEXT
            );''')
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS hacker_skills (
                hacker_id INTEGER,
                skill TEXT,
                rating INTEGER,
                FOREIGN KEY (hacker_id) REFERENCES hackers(hacker_id)
            );''')

        # Iterate over each hacker in the JSON, and add corresponding data
        for hacker in data:
            cursor.execute('''
                INSERT INTO hackers (name , company, email, phone)
                VALUES (?, ?, ?, ?);''', (hacker['name'], hacker['company'], hacker['email'], hacker['phone']))
            
            current_hacker_id = cursor.lastrowid # keep track of current hacker, to link hackers and hacker_skills

            # Nested for-loop to go through each entry of skills for a single hacker
            for skl in hacker['skills']:
                cursor.execute('''
                    INSERT INTO hacker_skills (hacker_id, skill, rating)
                    VALUES (?, ?, ?);''', (current_hacker_id, skl['skill'], skl['rating']))

        # DONE
        conn.commit()
        conn.close()

    except requests.exceptions.HTTPError:
        print("HTTP Error {}", resp.status_code)
        exit

    except requests.exceptions.RequestException:
        print("Network Error: Could not connect to the URL")
        exit

    except sqlite3.OperationalError:
        conn.close()
        print("Operational Error: Could not connect to the database or invalid command executed. No changes made.")
        exit

if __name__ == '__main__':
    get_db()