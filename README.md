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
4. Launch vagrant virtual machine 'vagrant up' command from the terminal
5. Log into vagrant virtual machine with 'vagrant ssh' command from terminal
5. Run databasesetup.py to create sqlite database
6. Run project.py in shell: python project.py
7. Check out app on http://localhost:5000 per default
