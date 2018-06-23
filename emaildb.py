import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1):
    fname = 'mbox-short.txt'

fh = open(fname)
for line in fh:
    line = line.strip()
    if not line.startswith('From: '):
        continue

    pieces = line.split()
    email = pieces[1]

    cur.execute('SELECT count FROM Counts WHERE email = ?', (email, ))
    row = cur.fetchone()

    if row is not None:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (email,))
    else:
        cur.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (email,))

    conn.commit()

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.executeN(sqlstr):
    print(str(row[0]), row[1])

cur.close()
