################################################################################
#                   #### Hiking_project_basic.py #####                         #
#                 #### written by: Etienne Deneault #####                      #
#    In the context of a Capstone project in the Pyfe Specialization.          #
#    This program is a program that request the user to input COORDINATES      #
#    and SEARCH AREA RANGE and returns the TOP 10 hiking trails in the         #
#    SEARRC AREA.The program also produces a interative data visualization     #
#    The program also produces a interative data visualization using Bokeh.    #
################################################################################
import json
import requests
import sqlite3
from shapely.geometry import Point, Polygon

# Enter Hiking Project API key here. Further Dev needed for encrytion through env variable external program.
api_key = "your_api_key"
# key = '?registrationkey={}'.format(config.bls_key)
#api_key = open('confapi.py', 'w')
# api_key = f
# with open('confapi.py', 'r') as api_key:
    # api_key = (api_key.read())


# Base URL for getTrails method
url = 'https://www.hikingproject.com/data/get-trails?'


def USBoundchk():
    # Function to check if coordinates entered are within the Mainland US
    p1 = Point(lon,lat)
    # p2 = Point(-1, -1) # Variation for multiple points input
    # Create a Polygon based on United States Boundry Box Coordinates
    coords = [(-82.4423472248,25.062761981), (-85.6719092689,29.570088284), (-89.362854179,29.650311372), (-97.9443083368,26.5579317639), (-117.2294984422,32.2612294633), (-125.072755035,41.8816215194), (-124.2423002086,48.2581198196), (-121.566356834,49.3519856698), (-96.4679400287,48.808034488), (-92.0388082824,48.5643678729), (-84.6569184623,46.8886898289), (-81.7964176498,42.8361752569), (-76.3522736392,43.7095457837), (-70.2622322402,46.3181308653), (-68.1399397216,47.014662257), (-66.4790086112,44.7016972202), (-69.7085706554,43.3080101182), (-76.1677269302,38.7876636101), (-75.7986335121,35.6284188995), (-80.7814268432,30.8459373794), (-79.5818678699,26.4753651459), (-82.4423472248,25.062761981)]
    poly = Polygon(coords)
    # print(poly)
    # Check if p1 and p2 are within the polygon using the within function
    if p1.within(poly):
        p1 = Point(lat,lon)
        print()
        return print("COORDINATES VALIDATED", p1)
    else:
        return print("\nThe coordinates entered do not appear to be in the Mainland United States,\nplease try again.")

##### Main Loop #####
if __name__ == "__main__":

    while True:
        # Input Section # Further dev needed to prevent tracebacks with certain values not interpreted correctly causing float to fail.
        try:
            lat = input('Enter your search area - LATITUDE coordinate: ')
            lat = float(lat)
        except ValueError:
            print("I did not understand the input, please try again using a coordinate value.")
            continue

        try:
            lon = input('Enter your search area - LONGITUDE coordinate: ')
            lon = float(lon)
        except ValueError:
            print("I did not understand the input, please try again using a coordinate value.")
            continue

        # Call function to check if coordinates are within US Mainland Boundry Box
        USBoundchk()
        try:
            print()
            maxDistance = input('Enter Maximun Search Distance (0-200 (miles)) from Coordinates entered: ')
            maxDistance = int(maxDistance)
        except ValueError:
            print("I did not understand the input, please try again using a distance value (0-200 miles).")
            continue
        # if len(maxDistance) < 1: break

        parameters = {"lat": lat, "lon": lon, "maxDistance": maxDistance, "key": api_key}

        # Make a get request with the parameters.
        response = requests.get(url, params=parameters)
        # RESPONSE CHECK - prints
        # print(response.url)
        # print(response.headers)
        # print(response.status_code)

        # Create DataBase using sqlite3
        db = sqlite3.connect("trails.sqlite")
        cur = db.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Trailsdb (id INTEGER NOT NULL PRIMARY KEY UNIQUE, name TEXT,
            type TEXT, summary TEXT UNIQUE, difficulty TEXT, stars INTEGER, starVotes INTEGER,
            location TEXT, url TEXT UNIQUE, length INTEGER, ascent INTEGER, descent INTEGER, high INTEGER,
            low INTEGER, longitude INTEGER, latitude INTEGER, conditionStatus TEXT, conditionDetails TEXT,
            conditionDate TEXT)''')
        # print(response.text)
        str_data = response.text
        json_data = json.loads(str_data)

        # Insert or replace (update)  ##### Over time this will keep the DataBase updating and growing i.e. Condition Staus INFORMATION
        # and compounding effect of searches (crawling hikingproject.com trail DataBase #####
        for trail in json_data['trails']:
            #print(child)
            cur.execute("Insert or replace into trailsdb values ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (trail['id'], trail['name'], trail['type'], trail['summary'], trail['difficulty'],
                            trail['stars'], trail['starVotes'], trail['location'], trail['url'], trail['length'],
                            trail['ascent'], trail['descent'], trail['high'], trail['low'],trail['longitude'],
                            trail['latitude'], trail['conditionStatus'], trail['conditionDetails'],
                            trail['conditionDate']))
            db.commit()


        trails= dict()

        # Trails loaded - OUTPUT SECTION
        print()
        print()
        print("##########  TOP 10 Trails in your defined search area:  ##########")
        print()
        Trcounter = 0
        for trail in json_data["trails"]:
            Trcounter = Trcounter + 1
            print()
            print("     ", "Trail #:", Trcounter, "info -")
            print()
            print("          ", "TRAIL NAME:", trail["name"], "DIFFICULTY:", trail['difficulty'], "LENGTH:", trail['length'], "STARS:", trail['stars'])
            print("          ", "TRAIL SUMMARY", trail['summary'])
            print("          ", "LATITUDE:", trail['latitude'], "LONGITUDE:", trail['longitude'], "CONDITION STATUS", trail['conditionStatus'])
            print()
            print("          ", "FOR MORE DETAILED TRAIL INFORMATION, check out the URL below:")
            print()
            print("          ", trail['url'])

        cur.close()
        break
