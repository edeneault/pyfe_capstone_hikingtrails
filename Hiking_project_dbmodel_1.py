################################################################################
#                   #### Hiking_project_dmodel.py #####                        #
#                 #### written by: Etienne Deneault #####                      #
#    In the context of a Capstone project in the Pyfe Specialization.          #
#    This program is meant to clean and index the data to a new database.      #
#    The new database is cleaned of the columns of unnecessary columns and     #
#    creates an index for columns with repeating data.  Surely, it could be    #
#    compressed further and will likely need to be, given the quantity of data #
#    that the scraper program retrieves.                                       #
################################################################################

import sqlite3

conn = sqlite3.connect('SQL_data/index.sqlite')
cur = conn.cursor()

# Drop tables to re-index all of Trailsdb
cur.execute('''DROP TABLE IF EXISTS Trails ''')
cur.execute('''DROP TABLE IF EXISTS Locations''')
cur.execute('''DROP TABLE IF EXISTS Difficulties ''')


cur.execute('''
CREATE TABLE IF NOT EXISTS Trails
    (id INTEGER NOT NULL UNIQUE PRIMARY KEY, name TEXT UNIQUE, difficulty_id INTEGER,
    stars INTEGER, starVotes INTEGER, location_id INTEGER, url TEXT UNIQUE, length INTEGER,
    longitude INTEGER, latitude INTEGER) ''');

cur.execute('''CREATE TABLE IF NOT EXISTS Locations
    (id INTEGER PRIMARY KEY, location TEXT)''');

cur.execute('''CREATE TABLE IF NOT EXISTS Difficulties
    (id INTEGER PRIMARY KEY, difficulty TEXT)''')

conn.commit()


# # Open the main content (Read only)
conn_1 = sqlite3.connect('file:SQL_data/trails.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()

# Types = dict()
# Locations = dict()
# Difficulties = dict()
# Conditions = dict()

cur_1.execute('''SELECT id, name, difficulty, stars, starVotes, location, url, length, longitude,
    latitude FROM Trailsdb''')
print('next')


Locations = dict()
Difficulties = dict()

count = 0

for Trailsdb_row in cur_1 :
    id = Trailsdb_row[0]
    name = Trailsdb_row[1]
    difficulty = Trailsdb_row[2]
    stars = Trailsdb_row[3]
    starVotes = Trailsdb_row[4]
    location = Trailsdb_row[5]
    url = Trailsdb_row[6]
    length = Trailsdb_row[7]
    longitude = Trailsdb_row[8]
    latitude = Trailsdb_row[9]

    location_id = Locations.get(location, None)
    difficulty_id = Difficulties.get(difficulty, None)

    if location_id is None :
        cur.execute('INSERT OR IGNORE INTO Locations ( location ) VALUES ( ? )', ( location, ) )
        conn.commit()
        cur.execute('SELECT id FROM Locations WHERE location=? LIMIT 1', ( location, ))
        try:
            row = cur.fetchone()
            location_id = row[0]
            Locations[location] = location_id
        except:
            print('Could not retrieve location id', location)
            break

    if difficulty_id is None :
        cur.execute('INSERT OR IGNORE INTO Difficulties ( difficulty ) VALUES ( ? )', ( difficulty, ) )
        conn.commit()
        cur.execute('SELECT id FROM Difficulties WHERE difficulty=? LIMIT 1', ( difficulty, ))
        try:
            row = cur.fetchone()
            difficulty_id = row[0]
            Difficulties[difficulty] = difficulty_id
        except:
            print('Could not retrieve difficulty id',difficulty)
            break
    # print(id , name, stars, starVotes, url, length, longitude, latitude)
    count = count + 1
    cur.execute('INSERT OR IGNORE INTO Trails (id, name, difficulty_id, stars ,starVotes, location_id, url, length, longitude, latitude) VALUES ( ?,?,?,?,?,?,?,?,?,?)',
            (id, name, difficulty_id, stars, starVotes, location_id, url, length, longitude, latitude))

    # cur.execute('select location, Locations.location FROM Trails join Locations on Trails.location_id = Locations.id')

    conn.commit()

print("Number of locations:", len(Locations))
print("Read:", count)
