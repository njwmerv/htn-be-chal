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
```
```
database_setup.py
    get_db()
    - Sends an HTTP request for the JSON then creates an SQL database with the data organized into the
      tables mentioned above

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
```
Extra Notes:
1. When getting user data, the categories are sorted alphabetically, instead of the order given in the code.
2. If I were to implement some functionality for events, I would handle it very similarly to skills:
- A whole separate table for events attended, with columns: hacker_id | event | rating (optional)
- hacker_id would be a foreign key to link it to the other tables.
- For a hacker to register to an event, they could scan a QR code that redirects them to a url, like /event/(EVENT_NAME),
  which would trigger the event being added to hacker_events with their hacker_id
