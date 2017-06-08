# Item Catalog Project

An application that analyzes database data and produces a report that tells
us the most popular articles, the most popular artists, and days where there
are lots of 404 errors 


## How to run the application

1. download the files
2. change the directory in your terminal to the downloaded folder
3. Run the `python catalog.py` command in your terminal to populate the database
4. Run the `python project.py` command in your terminal
5. go to `http://localhost:5000` in your browser and browse the catalog

## How it works

### Database structure

There are 3 tables in the database
 - user
   - stores all the users
 - category
   - stores all the categories
 - item
   - stores all the items 

### Routes

All the important routes exist in the `project.py` file

The routes are
  - '/login'
  - '/gonnect'
  - '/fbconnect'
  - '/gdisconnect'
  - '/fbdisconnect'
  - '/'
  - '/catalog/<int:category_id>/'
  - '/catalog/<int:category_id>/<string:item_name>/'
  - '/catalog/new/'
  - '/catalog/<string:item_name>/edit/'
  - '/catalog/<string:item_name>/delete/'
  - '/catalog.json/'

'/login'
This route renders a page that allows users to login via Google or Facebook

'/gconnect'
This route allows the application to log in and authenticate with their Google account

'/fbconnect'
This route allows the application to log in and authenticate with their Facebook account

'/gdisconnect'
This route calls a helper method that allows the users who use their Google account to log in to log out of the application 

'/fbdisconnect'
This route calls a helper method that allows the users who use their Facebook account to log in to log out of the application 

'/disconnect'
This route calls a helper method based on whether or not the user logged in with their Facebook or Google account, and then takes steps to log the user completely out of the app


'/'
This route renders the homepage that produces a list of all the categories along with the latest items

'/catalog/<int:category_id>/'
This route renders a page that produces a list of items within a category, along with the list of all the categories

'/catalog/<int:category_id>/<string:item_name>/'
This route renders a page that produces an item and its description along with the ability to edit or delete the item if the user created the item

'/catalog/new/'
This route renders a page with a form that allows for the user to create a new item if they are logged in

'/catalog/<string:item_name>/edit/'
This route renders a page with a form that allows for the user to edit an item if they are logged in and created the item

'/catalog/<string:item_name>/delete/'
This route renders a page with a form that allows for the user to delete an item if they are logged in and created the item

'/catalog/<string:item_name>/json/'
This endpoint produces a JSON object of the item that is specified in the path
