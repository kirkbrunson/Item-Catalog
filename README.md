# FSND-P3

### Description
Project 3 for Udacity's FSND program:
CRUD webapp that is a simple store.

### Setup
- Clone the vagrant machine setup for the oauth class, ssh into it and cd to FSND-P3
- Install Flask-seasurf: Run pip install flask-seasurf
- Run python createDB.py. _Note: rm samplestore.db before reinitializing._
- Run python project.py
- Navigate to 127.0.0.1:5000

### API Use:
- GET req on /[category]/[json, xml] returns json or xml of current subcategories for given category
- GET req on /category/[subcategory]/[json, xml] returns json or xml of current items for given subcategory

### Requirements:
- [Flask](http://flask.pocoo.org/) v0.9 and up
- [Flask-seasurf](https://github.com/maxcountryman/flask-seasurf/) v0.2.0
- [SQLAlechemy](http://docs.sqlalchemy.org/en/rel_0_8/) v0.8.4
- [oauth2client](https://github.com/google/oauth2client) v1.4.11

### Notes:
- User profile and reviews coming soon. 
- Known issue of occasional login/logout issue. Try toggling.

### Credits:
- Sample items from AE.