from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, subCategories, Items, Base
import json

engine = create_engine('sqlite:///samplestore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

data = json.loads(
    open('db_init.json', 'r').read())



try:
	for i in data['categories']:
	    c = Categories(name=i)
	    session.add(c)

	for i in data['subCategories']:
	    sc = subCategories(
	        category_id=i['category_id'], name=i['name'], description=i['description'])
	    session.add(sc)

	for i in data['items']:
	    item = Items(name=i['name'], description=i['description'], category=i[
	                 'category'], subCategory=i['subCategory'], price=i['price'])
	    session.add(item)
	
	session.commit()

except:
	session.rollback()
	raise RuntimeError('Database write failed.')


print '\nDatabase build successful!'
