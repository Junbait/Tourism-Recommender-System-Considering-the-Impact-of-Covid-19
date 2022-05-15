# Tourism-Recommender-System-Considering-the-Impact-of-Covid-19
DESCRIPTION：

Our package (within the CODE folder) includes the following documents:
(1) recommendation_system.py	--- the application script
(2) city_data.py			    --- get the city information from api
(3) covid_data.py			    --- get the covid data from api
(4) static				        --- the css and svg documents	
(5) templates			        --- the html and javascript documents
(6) requirements.txt			--- Python environment requirements
(7) data_cleaning.ipynb         --- Data preprocessing steps
(8) user_data.csv               --- Proprocessed travel history dataset

The original Gowalla dataset is obtained from the following link:
https://snap.stanford.edu/data/loc-gowalla_totalCheckins.txt.gz

As the size of the preprocessed dataset is not very large, it is also included 
in the folder.

********************************************************************************

INSTALLATION:

run `pip install -r /path/to/requirements.txt` in terminal at current folder.

********************************************************************************

EXECUTION:

(1) Run `python recommendation_system.py` in the terminal.
(2) Open the local url prompted in the terminal.
(3) Enter five cities you have been visited before, then press "submit".
(4) The app will return five recommended cities for you to visit, 
    as well as information, picture, and rank of these cities.
