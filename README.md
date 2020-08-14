# Capstone Project - University of Michigan - Coursera PYFE Specialization
## US Hiking Trails and Peak Elevations - Interactive Visualization with Maps using Bokeh

Designed as a Capstone project for the *Python for Everybody Specialization* course series, this project sought to create a series of applications for data retrieval, processing, and visualization that highlighted many of the techniques and programming strategies learned throughout these courses.  Specifically, this project developed  programs to collect data on *United States Mainland hiking trails* and *Peak Elevations by State*.

This suite of programs enables users to search for *Top Ten* trails as user-defined coordinates and distance parameters. These programs collect data from the *hikingproject.com* API, store them in an SQLite Database, clean and index the database, perform a basic analysis of the data , and provide an *interactive visualization map* of the data collected using *Bokeh*.

<sup>Interactive Map</sup>
![ScreenShot](https://github.com/edeneault/pyfe_capstone_hikingtrails/blob/master/README.assets/README-Visual_screenshot_loadup.PNG)


[View visualization here](https://edeneault.github.io/pyfe_capstone_hikingtrails/Hiking_project_dbvisual_4.html)


### Prerequisites

**Software:**
* Python 3
* DB Browser (SQLite)

**Python Environment:**
* json
* shapely
* pandas
* geopandas
* Bokeh
* sqlite3
* requests

### Installing

For the scope of this project, I will not prepare installation instructions for the dependencies.

*important*:  your  own api key replaces 'your_api_key' to run the programs.

['api_key = 'your_api_key'']



  *Note: If you are using anaconda, it will make it easier to install the environment needed.  My development environment for this project is on windows 10, the dependencies were somewhat difficult to install.  Geopandas and bokeh gave me a bit of a struggle but all the information you need is easily googled. Knowledge of basic command line is helpful.*  

### Contents and Details

#### Programs:

  * Hiking_project_trailscraper.py
  * Hiking_project_dbmodel.py
  * Hiking_project_basic.py
  * Hiking_project_API.py
  * Hiking_project_dbvisual.py
  * Hiking_project_API_novisual.py
  * visualpass.py

#### Folders and Files

  * Data Folder
  * Index Folders
  * README file

#### Data Collection
*Hiking_project_trailscraper.py*  

This program initiates a connection to the *hikingproject.com API*. The *hikingproject.com API* is open to everyone, just register for a free account and an API key is assigned automatically. The API key is sent to you by email.  Easy beans!  The program calculates all of the coordinate points within the mainland US using the polygon boundaries as reference. Coordinates returned are in a list of tuples. The values are integer values. The program makes a GET request to the *hikingproject API*.  The API returns a maximum of 500 trails for a range of up to 200 miles from each point per request (max 200 requests per hour, max 800 request per day).  The program iterates through the json response, creates a SQLite database *trails.sqlite* and inserts the data.

#### Data Cleaning and Indexing
*Hiking_project_dbmodel.py*  

This program cleans and indexes the data to a new database, data file: *index.sqlite*. The new database is free of the unnecessary data and creates an index for columns with repeating data.  

#### Data Analysis
*Hiking_project_basic.py*

This program is to analyze the data collected.  A few data points are identified using the data. This section could be developed much further in the scope of a larger project.

#### Mini Application
*Hiking_project_API.py*

*Hiking_project_API_novisual.py*

This program is an application that prompts the user to input COORDINATE values and SEARCH AREA RANGE values, checks that the coordinates are within the US Boundary Box, and makes a GET request to the *hikingproject.com API*.  The API responds with the TOP 10 hiking trails in the SEARCH AREA requested. The trails are displayed to the user.  The user is then prompted to know if they would like to see a interactive visualization of the database they have searched. The visualization is built with *Bokeh*.

#### Bokeh Visualization
*Hiking_project_dbvisual.py*

This program is an interactive visualization of the US Mainland Hiking Trails.  The Hiking Trails are represented by *Dots* on the a map of the mainland US. The visualization displays the Highest Peak of each state upon mouse hover.  The trail Location *Dots* are hover sensitive, providing basic hiking trail information. The trail location *Dots* are also sensitive to *Tap/Click*. Clicking will direct the user to the trails specific URL on the Hikingproject.com website.

<sup>Interactive Map - State Hover and Trail Hover</sup>
![ScreenShot](https://github.com/edeneault/pyfe_capstone_hikingtrails/blob/master/README.assets/Screenshot_hp_trail.png)



#### Additional Files/Folders
* *visualpass.py* is a program to pass through a function with the Bokeh visualization to the Hiking_project_API.py program.
* *Data* folder contains the data files needed in Bokeh to draw the map and provide data for the highest elevations by state.
* *SQL_data* folder contains *trails.sqlite* and *index.sqlite*.

#### Additional Notes

* disclosure:  the database file *trail.sqlite* has  currently collected approximately 15000 of the US trails.  

On a personal note, this project was very educational.   I enjoyed working on it and learning how to solve the inevitable problems that come up in the process.  Every small measure of success bolstered my resolve to complete it as best as my newfound knowledge would allowed.  
Certainly, in a larger scope of project, there are many areas that could be developed further, structured in a more elegant and economical manner.
The code is available to download, if anyone wishes to make contributions, improvements, recommendations or any comment, I look forward to read/reply.



#### Authors

* **Etienne Deneault** - *Initial work* - [edeneault](https://github.com/edeneault)

#### Acknowledgments and Resources

* A big **THANK YOU** to the teachers and assistant teachers from the *University of Michigan* in the Coursera, *Python for Everybody* Specialization. The courses were laid out well, instructive and easy to follow.

* Reference: The Hiking Project CLI by Will Carter
https://medium.com/@will.carter/the-hiking-project-cli-812b486332f
The original inspiration for my project was another project from a student who built a CLI app using the hikingproject API, my curiosity was peaked as I am an avid hiker/backpacker. Thank you *Will Carter* for the inspiration.
* Reference: Walkthrough: Mapping Basics with bokeh and GeoPandas in Python by Rebecca Weng
https://towardsdatascience.com/walkthrough-mapping-basics-with-bokeh-and-geopandas-in-python-43f40aa5b7e9
This step-by-step was very instructive to learn how to use bokeh, thank you *Rebecca Weng*.

* Reference: https://towardsdatascience.com/walkthrough-mapping-basics-with-bokeh-and-geopandas-in-python-43f40aa5b7e9

* Data: API - https://www.hikingproject.com/data

* Data: cb_2018_us_state_20m.sgv https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

* Data: https://www.infoplease.com/us/geography/highest-lowest-and-mean-elevations-united-states


##### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
