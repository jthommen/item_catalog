# Item Catalog Project
## Item Catalog for the Udacity Full Stack Web Developer Nanodegree


### Features
* Differentiates between visitors (not logged in) and users (logged in)
* Visitors can:
  * Use Google login
  * Use Facebook login
  * View restaurants
  * View menus
  * Access JSON data
* Users can:
  * Create new restaurants
  * Update their own restaurants
  * Delete their own restaurants
  * Add menus to their own restaurants
  * Edit their own menus
  * Delete their own menus

### WebTech used:
* Flask
* Sqlalchemy
* SQLite
* Oauth2
* Vagrant
* Httplib2
* Bootstrap3

### To run locally:
1. Download and install python 2.7
2. Download and install vagrant and virtual box
3. Clone repo
4. Open terminal and navigate to repo
5. Launch vagrant virtual machine 'vagrant up' command from the terminal
6. Log into vagrant virtual machine with 'vagrant ssh' command from terminal
7. For Google Oauth login, create your project at https://console.developers.google.com
8. For Facebook Oauth login, create your project at https://developers.facebook.com
9. Save the Oauth secrets in separate *.json files in repo folder
10. Change app IDs in login.html templates according to your Google & Facebook app IDs
11. Change user to postgres super user `sudo -u postgres -i`
12. Create vagrant role as superuser `createuser vagrant --superuser`
13. Logout as postgres superuser `logout`
14. Create project db with postgres `createdb restaurantmenuwithusers.db`
15. Run `python databasesetup.py`
16. Run project.py in terminal with `python project.py` command from the terminal
17. Check out app on http://localhost:5000 (vagrant default port)
