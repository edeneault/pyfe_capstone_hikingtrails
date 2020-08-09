################################################################################
#                  #### Hiking_project_trailsraper.py #####                    #
#                 #### written by: Etienne Deneault #####                      #
#  In the context of the Coursera Capstone project in the Python for Evenybody #
#  Specialization provided by the University of Michigan.  This program        #
#  connects to the Hikingproject.com API. The Hikingproject.com API is open to #
#  everyone, just register for a free account and an API key is assigned       #
#  automatically. It is also sent to you by email.  Easy beans!  The program   #
#  calculates all of the coordinates points within the mainland US using       #
#  the polygon boundaries as reference. Coordinates are integer values         #
#  (approx 69 miles per degree). The program makes a get request to the        #
#  Hikingproject API for a return of a maximum of 500 trails for a range of up #
#  to 200 miles from each point per request (max 200 requests per hour, max    #
#  800 request per day).  The program iterates through the json response,      #
#  creates the necessary table and retrieves the data with SQLite.             #
#  Crawling acheives large results quicklyis if maximum paramteres are entered.#
################################################################################

# Environment-import
import json
import requests
import sqlite3
import random
from shapely.geometry import Point, Polygon

# initalize coordinates at the center of mainland US
def get_all_point_in_polygon(coords):
    (minx, miny, maxx, maxy) = poly.bounds
    minx = int(minx)
    miny = int(miny)
    maxx = int(maxx)
    maxy = int(maxy)
    # print("poly.bounds:", poly.bounds)

    #define list of tuples
    a = []

    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            p = Point(x, y)
            if poly.contains(p):
                a.append([x, y])

    return a

# Enter Hiking Project API key here. Further Dev needed for encrytion through env variable external program.
api_key = 'your_api_key'

# Base URL for getTrail_datas method
url = 'https://www.hikingproject.com/data/get-trails?'

# Bounding Box Coordinates for the Mainland US obtained on
coords = [(-82.4423472248,25.062761981), (-85.6719092689,29.570088284), (-89.362854179,29.650311372), (-97.9443083368,26.5579317639), (-117.2294984422,32.2612294633), (-125.072755035,41.8816215194), (-124.2423002086,48.2581198196), (-121.566356834,49.3519856698), (-96.4679400287,48.808034488), (-92.0388082824,48.5643678729), (-84.6569184623,46.8886898289), (-81.7964176498,42.8361752569), (-76.3522736392,43.7095457837), (-70.2622322402,46.3181308653), (-68.1399397216,47.014662257), (-66.4790086112,44.7016972202), (-69.7085706554,43.3080101182), (-76.1677269302,38.7876636101), (-75.7986335121,35.6284188995), (-80.7814268432,30.8459373794), (-79.5818678699,26.4753651459), (-82.4423472248,25.062761981)]
poly = Polygon(coords)

point_in_poly = get_all_point_in_polygon(poly)

print("Number of coordinate points to check:", len(point_in_poly))
# print(point_in_poly)

# Randomize list of coordinates
random.shuffle(point_in_poly)

##### Main Loop #####
if __name__ == "__main__":

    while True:
        try:
            maxDistance = input('Enter your search area (0-200 miles): ')
            maxDistance = int(maxDistance)
        except ValueError:
            print("I did not understand the input, please try again using a distance numeric value in miles.")
            continue

        try:
            maxResults = input('Enter your search area - Maximum bumber of trail results (0-500): ')
            maxResults = int(maxResults)
        except ValueError:
            print("I did not understand the input, please try again using a numeric value.")
            continue
        try:
            userReq_count = input('Enter the number of requests to the API (0-199): ')
            userReq_count = int(userReq_count)
        except ValueError:
            print("I did not understand the input, please try again using a numeric value.")
            continue

        req_count = 0
        # Note:  Reverse cordinates to input (lat,lon) == (y,x)
        for (x,y) in point_in_poly:
            req_count = req_count + 1
            print('Query Count', req_count)
            maxDistance = 100
            maxResults = 400

            parameters = {"lat": y, "lon": x , "maxDistance": maxDistance, "maxResults": maxResults, "key": api_key}

            # Make a get request with the parameters.
            response = requests.get(url, params=parameters)
            print(response.url)
            print(response.headers)
            print(response.status_code)


            # print(response.text)
            # print(response.headers)
            # print(response.json())

            db = sqlite3.connect("SQL_data/trails.sqlite")
            cur = db.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS Trailsdb (id INTEGER NOT NULL PRIMARY KEY UNIQUE, name TEXT,
                type TEXT, summary TEXT UNIQUE, difficulty TEXT, stars INTEGER, starVotes INTEGER,
                location TEXT, url TEXT UNIQUE, length INTEGER, ascent INTEGER, descent INTEGER, high INTEGER,
                low INTEGER, longitude INTEGER, latitude INTEGER, conditionStatus TEXT, conditionDetails TEXT,
                conditionDate TEXT)''')

            str_data = response.text
            json_data = json.loads(str_data)


            # for entry in json_data:
            #     print(entry)
            for trail in json_data['trails']:
                #print(child)
                cur.execute("Insert or replace into trailsdb values ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (trail['id'], trail['name'], trail['type'], trail['summary'], trail['difficulty'],
                                trail['stars'], trail['starVotes'], trail['location'], trail['url'], trail['length'],
                                trail['ascent'], trail['descent'], trail['high'], trail['low'],trail['longitude'],
                                trail['latitude'], trail['conditionStatus'], trail['conditionDetails'],
                                trail['conditionDate']))
                db.commit()
            if req_count == userReq_count:
                break
            db.commit()
        print("all done")
        break
