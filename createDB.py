from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, subCategories, Items, Inventory, Users, Sales, Reviews, Base

engine = create_engine('sqlite:///samplestore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# ================================================
# need to map relations as well.. see L8 from dbsetup.py.
# this is ridiculous.... should read from a list, file... anything else...
# and put in loop

# ================================================




# Create categories
# ======================================================================================
category = Categories(name="Women")
session.add(category)
session.commit()

category = Categories(name="Men")
session.add(category)
session.commit()

# Create sub Categories
subCat = subCategories(category_id=1, name="Tee & Tanks",
                       description="THE SUMMER STYLES YOU NEED RIGHT NOW.")
session.add(subCat)
session.commit()

subCat = subCategories(
    category_id=1, name="Jeans", description="IT'S ALL IN THE DETAILS")
session.add(subCat)
session.commit()

subCat = subCategories(category_id=1, name="Shoes",
                       description="THE PERFECT LATE SUMMER STYLE WITH SANDALS IN MUST-HAVE METALLICS.")
session.add(subCat)
session.commit()

subCat = subCategories(category_id=2, name="Tee & Tanks",
                       description="THE SUMMER STYLES YOU NEED RIGHT NOW.")
session.add(subCat)
session.commit()

subCat = subCategories(category_id=2, name="Shirts",
                       description="THESE SHORT SLEEVE BUTTON DOWNS ARE NEXT-LEVEL IN PRINTS, MADRAS AND MORE.")
session.add(subCat)
session.commit()

subCat = subCategories(
    category_id=2, name="Jeans", description="IT'S ALL IN THE DETAILS")
session.add(subCat)
session.commit()


# Create items
# ======================================================================================

# Womens Tees & tanks
item = Items(name="AEO SIGNATURE GRAPHIC T-SHIRT",
             description="Show off your signature #AEOSTYLE.", category=1, subCategory=1, price=12)
session.add(item)
session.commit()

item = Items(name="AEO SIGNATURE GRAPHIC TANK",
             description="The T you need.", category=1, subCategory=1, price=18)
session.add(item)
session.commit()

item = Items(name="AEO NYC DRAPEY MUSCLE TANK",
             description="Get inspired by the city that never sleeps.", category=1, subCategory=1, price=20)
session.add(item)
session.commit()

item = Items(name="AEO SIGNATURE FAVORITE T-SHIRT",
             description="Show off your signature #AEOSTYLE.", category=1, subCategory=1, price=12)
session.add(item)
session.commit()


item = Items(name="AEO SIGNATURE FAVORITE T-SHIRT",
             description="Show off your signature #AEOSTYLE.", category=1, subCategory=1, price=12)
session.add(item)
session.commit()

item = Items(name="AEO NYC GRAPHIC T-SHIRT", description="Get inspired by the city that never sleeps.",
             category=1, subCategory=1, price=15)
session.add(item)
session.commit()

# Womens Jeans
item = Items(name="AEO DENIM X4 JEGGING CROP",
             description="Our sexiest, skinniest fit. Looks like a jean, feels like a legging.", category=1, subCategory=2, price=30)
session.add(item)
session.commit()

item = Items(name="HI-RISE SKINNY JEAN",
             description="A super skinny fit thats great for going out. Now with a hi rise waist.", category=1, subCategory=2, price=25)
session.add(item)
session.commit()

item = Items(name="KICK BOOT JEAN", description="Classic fit with an added kick.",
             category=1, subCategory=2, price=45)
session.add(item)
session.commit()

item = Items(name="HI-RISE SKINNY JEAN",
             description="A super skinny fit thats great for going out. Now with a hi rise waist.", category=1, subCategory=2, price=30)
session.add(item)
session.commit()


item = Items(name="STRAIGHT JEAN", description="Our new & improved, favorite fit. The classic slim jean with a modern, sophisticated twist.",
             category=1, subCategory=2, price=45)
session.add(item)
session.commit()

item = Items(name="SUPER STRETCH STRAIGHT JEAN",
             description="Our new & improved, favorite fit. The classic slim jean with a modern, sophisticated twist.",  category=1, subCategory=2, price=45)
session.add(item)
session.commit()

# Womens Shoes
item = Items(name="AEO Double T-Strap Sandal",
             description="Your go-to sandal for every look.", category=1, subCategory=3, price=20)
session.add(item)
session.commit()

item = Items(name="AEO Double Strap Sandal",
             description="Walk on.", category=1, subCategory=3, price=35)
session.add(item)
session.commit()

item = Items(name="AEO Braided Leather Flip Flop",
             description="Walk on.", category=1, subCategory=3, price=25)
session.add(item)
session.commit()

item = Items(name="AEO Flip Flop", description="Beach to street.",
             category=1, subCategory=3, price=5)
session.add(item)
session.commit()


item = Items(name="Swedish Hasbeens Agneta",
             description="The Hasbeens toffels, bags and belts are based on original 70s models and are made of ecologically prepared natural grain leather.", category=1, subCategory=3, price=289)
session.add(item)
session.commit()

item = Items(name="AEO Side Fringe Heeled Bootie",
             description="Walk on. Fringe trim adds a standout pop to your go-to booties.",  category=1, subCategory=3, price=60)
session.add(item)
session.commit()


# ======================================================================================


# Mens Tees & tanks
item = Items(name="AEO TONAL CREW T-SHIRT",
             description="The T you need.", category=2, subCategory=4, price=20)
session.add(item)
session.commit()

item = Items(name="AEO STRIPED V-NECK T-SHIRT",
             description="The T you need.", category=2, subCategory=4, price=20)
session.add(item)
session.commit()

item = Items(name="AEO HERITAGE CREW T-SHIRT",
             description="Its iconic.", category=2, subCategory=4, price=20)
session.add(item)
session.commit()

item = Items(name="AEO COLORBLOCK CREW T-SHIRT",
             description="Rock the colorblock.", category=2, subCategory=4, price=20)
session.add(item)
session.commit()


item = Items(name="AEO COLORBLOCK POCKET T-SHIRT",
             description="Iconic style, reinvented.", category=2, subCategory=4, price=20)
session.add(item)
session.commit()

item = Items(name="AEO HERITAGE CREW T-SHIRT",
             description="Its iconic.", category=2, subCategory=4, price=20)
session.add(item)
session.commit()

# Mens Shirts
item = Items(name="AEO PINDOT POPLIN BUTTON DOWN SHIRT",
             description="The crisp, polished shirt you need in your closet.", category=2, subCategory=5, price=40)
session.add(item)
session.commit()

item = Items(name="AEO PRINTED BUTTON DOWN SHIRT",
             description="With a bold pattern and crisp cotton, this shirt was made for sunny days.", category=2, subCategory=5, price=40)
session.add(item)
session.commit()

item = Items(name="AEO MICROSTRIPE BUTTON DOWN SHIRT",
             description="The crisp, refined shirt you need in your closet.", category=2, subCategory=5, price=40)
session.add(item)
session.commit()

item = Items(name="AEO BUFFALO CHECK BUTTON DOWN SHIRT",
             description="Great #AEOSTYLE? Check.", category=2, subCategory=5, price=40)
session.add(item)
session.commit()


item = Items(name="AEO STRIPED OXFORD BUTTON DOWN SHIRT",
             description="Casual, yet polished.", category=2, subCategory=5, price=40)
session.add(item)
session.commit()

item = Items(name="AEO MADRAS PLAID BUTTON DOWN SHIRT",
             description="A bold new take on the timeless button down.", category=2, subCategory=5, price=40)
session.add(item)
session.commit()

# Mens Jeans
item = Items(name="SLIM STRAIGHT CORE FLEX JEAN",
             description="New Core Flex denim looks and feels like your favorite AEO denim, with just enough stretch for increased comfort & flexibility. Revolutionary comfort, retention & durability- made to move with you.", category=2, subCategory=6, price=50)
session.add(item)
session.commit()

item = Items(name="RELAXED STRAIGHT JEAN",
             description="Our most comfortable jean, now even better than ever.", category=2, subCategory=6, price=45)
session.add(item)
session.commit()

item = Items(name="ORIGINAL STRAIGHT JEAN",
             description="The every guy, every day jean. Sits low on waist. Straight leg. Perfect with your favorite T-shirt.", category=2, subCategory=6, price=45)
session.add(item)
session.commit()

item = Items(name="ORIGINAL BOOT JEAN",
             description="The classic bootcut jean you love, given a twist with a low rise. Designed with a thick signature stitch at the back pocket.", category=2, subCategory=6, price=50)
session.add(item)
session.commit()


item = Items(name="CLASSIC BOOTCUT JEAN",
             description="You cant go wrong with a classic.", category=2, subCategory=6, price=45)
session.add(item)
session.commit()

item = Items(name="LOOSE JEAN", description="Our most relaxed, ready for anything jean.",
             category=2, subCategory=6, price=45)
session.add(item)
session.commit()



'''
Add users
======================================================================================
Users need more details such as unique g+ ids, pics etc

user1 = Users(name_first="Rick", name_last='Dole')
session.add(user1)
session.commit()

user2 = Users(name_first="Jessie", name_last='French')
session.add(user2)
session.commit()

user3 = Users(name_first="Sara", name_last='White')
session.add(user3)
session.commit()


# Add inventory
inventory1 = Inventory(item_id= 1, quantity=3)
session.add(inventory1)
session.commit()

inventory2 = Inventory(item_id= 2, quantity=4)
session.add(inventory2)
session.commit()


inventory3 = Inventory(item_id= 3, quantity=5)
session.add(inventory3)
session.commit()


inventory4 = Inventory(item_id= 4, quantity=6)
session.add(inventory4)
session.commit()


inventory5 = Inventory(item_id= 5, quantity=2)
session.add(inventory5)
session.commit()


inventory6 = Inventory(item_id= 6, quantity=9)
session.add(inventory6)
session.commit()


inventory7 = Inventory(item_id= 7, quantity=2)
session.add(inventory7)
session.commit()


inventory8 = Inventory(item_id= 8, quantity=3)
session.add(inventory8)
session.commit()

inventory9 = Inventory(item_id= 9, quantity=2)
session.add(inventory9)
session.commit()


# Add sales
sale1 = Sales(custumer_id=1, item_id=1, quantity=3)
session.add(sale1)
session.commit()

sale2 = Sales(custumer_id=2, item_id=2, quantity=2)
session.add(sale2)
session.commit()

sale3 = Sales(custumer_id=3, item_id=5, quantity=1)
session.add(sale3)
session.commit()

sale4 = Sales(custumer_id=1, item_id=8, quantity=4)
session.add(sale4)
session.commit()

sale5 = Sales(custumer_id=2, item_id=3, quantity=4)
session.add(sale5)
session.commit()

sale6 = Sales(custumer_id=2, item_id=9, quantity=1)
session.add(sale6)
session.commit()


# Add reviews
review1 = Reviews(custumer_id= 1, item_id=1, review_text='This is sample review: Lorem ipsum dolor sit amet, consectetur adipisicing elit. Odit ex, cum quibusdam itaque consequuntur voluptate quidem sapiente delectus aperiam, nemo enim libero modi voluptatibus aspernatur doloremque rem eveniet vero a distinctio ad! Voluptatem, doloribus! At rem possimus quos laudantium minus hic, tempora animi ut dolorum repellat! Maxime quis, distinctio. Optio.')
session.add(review1)
session.commit()
'''

print "added DB items!"
