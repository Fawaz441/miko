from sqlalchemy import Column, Integer, String, Float, Uuid
from database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Uuid, primary_key=True)
    name = Column(String(256))
    price = Column(Float(precision=2))
