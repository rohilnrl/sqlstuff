import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

handle = open('roster_data.json', 'r')
js = json.loads(handle.read())

for element in js:
    try:
        name = element[0]
    except:
        name = None

    try:
        course = element[1]
    except:
        course = None

    try:
        role = element[2]
    except:
        role = None

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (course,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (course,))
    course_id = cur.fetchone()[0]

    cur.execute('INSERT INTO Member (user_id, course_id, role) VALUES (?, ?, ?)', (user_id, course_id, role))

    conn.commit()

handle.close()
