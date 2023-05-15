from app import db
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean

class CCategory(db.Model):
    __tablename__ = 'category'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    item = db.relationship("CItem",back_populates='category')

class CItem(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = db.relationship('CCategory', back_populates='item')
    weight = Column(Float,default=None)
    count = Column(Integer,default=None)
    active = Column(Boolean,default=True)
    added = Column(Date)
    removed = Column(Date)


