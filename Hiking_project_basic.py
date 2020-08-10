################################################################################
#                   #### Hiking_project_basic.py #####                         #
#                 #### written by: Etienne Deneault #####                      #
################################################################################

import sqlite3

# Query SQLite Indexed DataBase and collect information into Dictionaries
db = sqlite3.connect('SQL_data/index.sqlite')
cur = db.cursor()

cur.execute('SELECT id, difficulty FROM Difficulties')
difficulties = dict()
for trail_row in cur :
    difficulties[trail_row[0]] = trail_row[1]

cur.execute('SELECT id, location FROM Locations')
locations = dict()
for trail_row in cur :
    locations[trail_row[0]] = trail_row[1]

# cur.execute('SELECT id, guid,sender_id,subject_id,headers,body FROM Messages')
cur.execute('''SELECT id, name, stars, starVotes, url, length, longitude,
                latitude FROM Trails''')
trails = dict()
for trail_row in cur :
    trails[trail_row[0]] = (trail_row[1],trail_row[2],trail_row[3],trail_row[4],
                            trail_row[5], trail_row[6], trail_row[7])

print("Loaded trails=",len(trails),"locations=",len(locations),
        "difficulties=", len(difficulties))
print()

db.close()

##### BREAK it apart #####
# Make a url dictionary
urls = dict()
# Load the dictionary
for (trail_id, trail) in list(trails.items()):
    url = trail[3]
    urls[url] = urls.get(url,0)
# Seperate tuples by converting into list and print out the first 10
Listurl = [url[:] for url in urls]
First10 = (Listurl[:10])

#for url in First10: print(url)

# Trailname Dict
Trailnames = dict()
# Load the dictionary
for (trail_id, trail) in list(trails.items()):
    name = trail[0]
    Trailnames[name] = Trailnames.get(name,0)
# Seperate tuples by converting into list and print out the first 10
Listname = [name[:] for name in Trailnames]
First10 = (Listname[:10])
# for name in First10: print(name)

Traillengths = dict()
# Load the dictionary
for (trail_id, trail) in list(trails.items()):
    length = trail[4]
    Traillengths[length] = Traillengths.get(length,0)
# Seperate tuples by converting into list (convert float to str)
# and print out the first 10
Listlengths = [str(length) for length in Traillengths]
First10 = (Listlengths[:10])
# for length in First10: print(float(length))

# Trail locations Dict
Traillocations = dict()
#Load the dictionary
for (location_id, location) in list(locations.items()):
    location = str(location[0:])
    # print(location)
    Traillocations[location] = Traillocations.get(location,0)
# Seperate tuples by converting into list (convert float to str)
# and print out the first 10
Listlocations = [location[:] for location in Traillocations]
First10 = (Listlocations[:10])
# print first 10 trail names
# for location in First10: print(location)

##### QUESTIONS and ANSWERS #####

print('How long is the longest trail?')

Listlengths = sorted(Listlengths, key=float, reverse=True)
print(Listlengths[0])

print('What is the name of the longest trail?')

Llength = 0
Lname = None
for (trail_id, trail) in list(trails.items()):
    length = trail[4]
    name = trail[0]
    # print(name, length)
    if length < Llength: continue
    Llength = length
    Lname = name
result = (trails)
# print(trails)
print(Lname, Llength)

# a little bit of SQLite, there is probable o more elegant way but...
# this method was the first I thought of...

print('How many trails in each difficulty rating categories?')
db = sqlite3.connect('SQL_data/index.sqlite')
cur = db.cursor()

cur.execute('''SELECT Trails.name, Difficulties.difficulty FROM Difficulties
                JOIN Trails ON Trails.difficulty_id = Difficulties.id''')

# Initalize counter lists
blueBlack = list()
blue = list()
black = list()
green = list()
greenBlue = list()
dblack = list()
missing  = list()
# Iterate through response and read in
for row in cur:
    row = cur.fetchone()
    difficulty = row[1]
    # seperate into colors and counrts
    if difficulty == None: continue
    if difficulty == "blueBlack": blueBlack.append(difficulty)
    if difficulty == "blue": blue.append(difficulty)
    if difficulty == "black": black.append(difficulty)
    if difficulty == "green": green.append(difficulty)
    if difficulty == "greenBlue": greenBlue.append(difficulty)
    if difficulty == "dblack": dblack.append(difficulty)
    if difficulty == "missing": missing.append(difficulty)
    else:
        continue
db.commit()
# Display results
print("blue:", len(blue), "green", len(green), "black:", len(black))
print( "blueBlack:", len(blueBlack), "greenBlue:", len(greenBlue),
        "dblack:", len(dblack))
print("missing:", len(missing))
