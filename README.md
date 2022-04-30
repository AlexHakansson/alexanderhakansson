# Professor Finder Dashboard

## Purpose:
The purpose of this application is to help students find professors who they share research interests with. This can help students find proffessors whos research they want to follow, participate in or who they would like as an adivsor as a Phd candidate.

## Demo:
A video demonstration of the tool can be found here:

## Installation:
To install the tool download from git hub. Edit the db_info.txt file with the usernames, host ips, and passwords required for your local database copy.

## Usage
The "Publications by Faculty" gets the number of publications for the top 10 professors at a given university. Simply select the university and keyword from the 2 drop down menus to perform you search.

The "Faculty Spotlight" allows you to get the contact info of a professor as well as there most cited article. Simply select the professor's name you are interested in from the drop down menu to perform your search.

The "Top Faculty Anywhere for Keyword" allows you to look up the top 10 faculty for a given keyword across the whole database. Simply select the keyword from the drop down menu to complete your search

The "Top 10 Keywords for Faculty" is the opposite of the previous function and allows you to find the top keywords a faculty member is interested in. Simply select the faculty member from the drop down menu to complete your search.

The "Favorites Table" allows you to keep track of your favorite professors that you may want to save. It contains their contact information, the university they work at and there position at that university. To add a professor selct a professor from the drop down menu. To remove a professor select there name from the drop down menu.

The "Favorite Faculty by Keyword" table looks compares professors in the favorites table by interest. Simply select a keyword you want to compare the professors by to complete your search.

## Design:
The "Publications by Faculty" gets the number of publications for the top 10 professors at a given university for a given keyword using neo4j. This uses 2 drop down widgets that contain all the keywords and universities present in the database in order to query the database. The login information for neo4j, keywords and universites are stored in a neo4j_handler object.

The "Faculty Spotlight" allows you to get the contact info of a professor as well as there most cited article. This widget uses mongo_db to query the faculty database and connects it to the publication database using the lookup function to find the publication with the most citations. Mongodb accessession information is stored in a mongo_db handler object

The "Top Faculty Anywhere for Keyword" allows you to look up the top 10 faculty for a given keyword across the whole database. This is implemented in SQL and once again uses a drop down widget to ensure a valid input. To expediate this search, the keyword table and faculty table in the database are each indexed by their name. This is done at the start of the application when creating the sql handler object which checks for the indexes and creates them if they are not there. This indexing process can take a bit of time so if this is the first time you are starting the application you might need to wait a while. This usese the faculty, keyword and keyword_faculty tables to complete this query.

The "Top 10 Keywords for Faculty" is the opposite of the previous function. It also uses a dropdown widget to select query and also benefits from the indexing of the faculty and keyword tables. This uses the faculty, keyword and keyword_faculty tables to complete this query.

The "Favorites Table" contains 2 widgets. One dropdown allows you to add professors to the table. The second widget allows you to remove professors from the table. This is implemented in SQL and the favorites table is stored as a view. It contains the main contact information of the professor from the faculty table and does a query of the university table to find the university of the professor from the university_id.

The "Favorite Faculty by Keyword" table looks compares professors in the favorites table by interest. This uses the view previously made to query the keyword score of the professors in the favorites table. This uses the keyword and keyword_faculty tables to complete this query.

## Database Techniques

Indexing was used to index the faculty and keyword tables by there name to speed up query time as most often users are interested in the name element of these tables. This was done using SQL's CREATE INDEX function.
Views were used to create a favorites table and store information about users favorite faculty in this table. This was done using SQL's CREATE VIEW function.

## Contribuitions

Good and bad, the entire work of this dashboard was done by Alexander Hakansson
