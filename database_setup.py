from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# ================================================

# restaurant = relationship(Restaurant)   (imp from frm menu class)
# Create views for orders, other dynamic things....

# may want to change cust_id to user_id
# change price from int to float
#
# add a star/ rating to reviews
# ================================================

class Categories(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class subCategories(Base):
    __tablename__ = 'subCategories'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('Categories.id'))
    name = Column(String(80), nullable=False)
    description = Column(String(140), nullable=False
)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
        }


class Items(Base):
    __tablename__ = 'Items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category = Column(Integer, ForeignKey('Categories.id'))
    subCategory = Column(Integer, ForeignKey('subCategories.id'))
    description = Column(String(250))
    price = Column(Integer)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'category': self.category,
            'subCategory': self.subCategory,
            'description': self.description,
            'price': self.price,
        }

# class Product_Images(Base):
#     __tablename__ = 'Product_Images'

#     id = Column(Integer, primary_key=True)
#     item_id = Column(Integer, ForeignKey('Items.id'))
#     image = Column(Blob)

#     @property
#     def serialize(self):
#         return {
#             'id' : self.id,
#             'item_id' : self.item_id, 
#         }
    


# class subCategory_Images(Base):
#     __tablename__ = 'subCategory_Images'

#     id = Column(Integer, primary_key=True)
#     subCategory_id = Column(Integer, ForeignKey('subCategories.id'))

#     @property
#     def serialize(self):
#         return {
#             'id' : self.id,
#             'subCategory_id' : self.subCategory_id,
#         }
    


class Users(Base):
    __tablename__ = 'Users'

    name_first = Column(String(40), nullable=False)
    name_last = Column(String(40), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name_first': self.firstname,
            'name_last': self.lastname,
            'description': self.description,
            'id': self.id,
        }


class Inventory(Base):
    __tablename__ = 'Inventory'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Items.id'))
    quantity = Column(Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'quantity': self.quantity,
        }


class Sales(Base):
    __tablename__ = 'Sales'

    id = Column(Integer, primary_key=True)
    custumer_id = Column(Integer, ForeignKey('Users.id'))
    item_id = Column(Integer, ForeignKey('Items.id'))
    quantity = Column(Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'custumer_id': self.custumer,
            'item_id': self.item,
            'quantity': self.quantity,
        }


class Reviews(Base):
    __tablename__ = 'Reviews'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Items.id'))
    custumer_id = Column(Integer, ForeignKey('Users.id'))
    review_text = Column(String(750), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'custumer_id': self.user,
            'review_text': self.review,
        }


engine = create_engine('sqlite:///samplestore.db')


Base.metadata.create_all(engine)
