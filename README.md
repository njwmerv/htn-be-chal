This is the submission of Nicanor (Mari) Montoya for the Hack the North Back-end Organizer Coding Challenge

```
Database Schema: hackers.db
hackers
CREATE TABLE hackers (
    hacker_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    company TEXT,
    email TEXT,
    phone TEXT
);
hacker_skills
CREATE TABLE hacker_skills (
    hacker_id INTEGER,
    skill TEXT,
    rating INTEGER,
    FOREIGN KEY (hacker_id) REFERENCES hackers(hacker_id)
);
CREATE TABLE IF NOT EXISTS hacker_events (
    hacker_id INTEGER,
    event TEXT,
    rating INTEGER CHECK ((rating >= 0 AND rating <= 10) OR rating IS NULL) DEFAULT NULL,
    FOREIGN KEY (hacker_id) REFERENCES hackers(hacker_id
);
```
```
database_setup.py
    get_db()
    - Sends an HTTP request for the JSON then creates an SQL database with the data organized into the
      tables mentioned above
    - hackers & hacker_skills start with data, while hacker_events starts empty (as if HTN hasn't started yet)

app.py
  Endpoint: GET /users/
    - Returns a JSON of all user data
  Endpoint: GET /users/INT
    - Returns a JSON of a specific user's data
  Endpoint: PUT /users/INT + JSON
    - Updates a user's data in the database, then returns their updated data
  Endpoint: GET /skills/
    - Returns a JSON of skills of users and their frequency in the database
  Endpoint: GET /skills/?min_frequency=INT&max_frequency=INT
    - Returns a JSON of skills of users and their frequency, but only for skills whose frequency are within the bounds set
  Endpoint: GET /events/
    - Returns a JSON of events attended w/ number of total attendees and average rating (if possible)
  Endpoint: GET /events/?min_frequency=INT&max_frequency=INT&min_rating=INT&max_rating=INT
    - Returns a JSON of events attended with the constraints given
```
Extra Notes:
1. Right now, events are treated the same as skills, but I would hope to make a few changes, if I have the time.
- Instead of making some PUT + JSON request, hackers could scan a QR code, which redirects them to a url like: /events/<EVENT_NAME>
    which adds a new row to hacker_events, with their hacker_id
- This page would also have the option of adding a rating
