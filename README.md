# Capstone Project - University of Michigan - Coursera PYFE Specialization
## US Hiking Trails and Peak Elevations - Interactive Visualization with Maps using Bokeh

In the context of the Capstone project in the *Python for Everybody Specialization*, this project is a practical application of the technologies learned through the specialization content. The project parameters are to design and create your own applications for data retrieval, processing, and visualization.

My applications are a suite of programs that serve to collect data of the United States Mainland *hiking trails* and *Peak Elevations by State*, provide the user with the ability to search for the *Top Ten* trails defined by the entry of coordinates and search distance parameters. My applications are designed to give the user the ability to collect data for the hikingproject.com API, store them in an SQLite Database, clean and index the database, perform basic calculations based on the data and finally provide an *interactive map visualization* of the data collected using *Bokeh*.

<sup>Interactive Map</sup>
<iframe><img alt="README-Hiking_project_dbvisual_4.html" src="README.assets/README-Hiking_project_dbvisual_4.html" width="" height="" ></iframe>

 <!-- <img alt="README-README-Visual_screenshot_loadup.PNG" src="README.assets/README-README-Visual_screenshot_loadup.PNG" width="" height="" > -->


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

*Note: If you are using anaconda, it will make it easier to install the environment needed.  My development environment for this project is on windows 10, the dependencies were somewhat difficult to install.  Geopandas and bokeh gave me a bit of a struggle but all the information you need is easily googled. Knowledge of basic command line is helpful.*  

## Contents and details

#### Programs:

* Hiking_project_trailscraper.py
* Hiking_project_dbmodel.py
* Hiking_project_basic.py
* Hiking_project_API.py
* Hiking_project_API_novisual.py
* Hiking_project_dbvisual.py
* visualpass.py

#### Folders and Files

* Data Folder
* Index Folders
* Hiking_project_dbvisual.html

#### Data Collection
*Hiking_project_trailscraper.py*  

This program connects to the *Hikingproject.com API*. The *Hikingproject.com API* is open to everyone, just register for a free account and an API key is assigned automatically. It is also  be sent to you by email.  Easy beans!  The program calculates all of the coordinates points within the mainland US using the polygon boundaries as reference. Coordinates are integer values (approx. 69 miles per degree). The program makes a get request to the *Hikingproject API* for a return of a maximum of 500 trails for a range of up to 200 miles from each point per request (max 200 requests per hour, max 800 request per day).  The program iterates through the json response, creates the necessary table, and retrieves the data with SQLite.

#### Data Cleaning and Indexing
*Hiking_project_dbmodel.py*  

This program is meant to clean and index the data to a new database *index.sqlite*. The new database is cleaned of the columns of unnecessary columns and creates an index for columns with repeating data.  

#### Data Analysis

This program is meant to analyze the data collected.  A few self-posed questions and answers with the use of the data. This section could be developed much further in the scope of a larger project.

#### Mini application

This program is a program that request the user to input COORDINATES and SEARCH AREA RANGE and returns the TOP 10 hiking trails in the  SEARCH AREA. The program also produces a interactive data visualization. The program also produces a interactive data visualization using Bokeh. 



## Authors

* **Etienne Deneault** - *Initial work* - [edeneault](https://github.com/edeneault)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
