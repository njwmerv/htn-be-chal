This is the submission of Nicanor (Mari) Montoya for the Hack the North Back-end Organizer Coding Challenge

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

database_setup.py
  get_db()
    - Sends an HTTP request for the JSON then creates an SQL database with the data organized into the
      tables mentioned above

app.py
  Endpoint: /users/
    - Returns a JSON of all user data
  Endpoint: /users/INT
    - Returns a JSON of a specific user's data
  Endpoint: /users/INT + JSON
    - Updates a user's data in the database, then returns their updated data
  Endpoint: /skills/
    - Returns a JSON of skills of users and their frequency in the database
  Endpoint: /skills/?min_frequency=INT&max_frequency=INT
    - Returns a JSON of skills of users and their frequency, but only for skills whose frequency are within the bounds set
  
