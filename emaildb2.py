import sqlite3

conn = sqlite3.connect('assign.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fh = open('mbox.txt')
for line in fh:
    line = line.strip()

    if not line.startswith('From: '):
        continue

    email = line.split()[1].split('@')[1]

    cur.execute('SELECT count FROM Counts WHERE org = ?', (email, ))
    row = cur.fetchone()

    if row is not None:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (email,))
    else:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (email,))

conn.commit()
