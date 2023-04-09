from fastapi import FastAPI, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import uuid


Base.metadata.create_all(engine)

app = FastAPI(title="Miko", description="An API for an e-commerce application",
              version="0.0.1", contact={"email": "abdulsalamfawaz4@gmail.com",
                                        "name": "Abdulsalam Fawaz Akolade", "url": "https://www.github.com/Fawaz441"
                                        }
              )


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def products_list(session: Session = Depends(get_session)):
    '''Endpoint to retreive all products in the system'''
    products = session.query(models.Product).all()
    return products


@app.post("/")
def add_product(product: schemas.Product, session: Session = Depends(get_session)):
    new_product = models.Product(
        name=product.name,
        price=product.price,
        id=uuid.uuid4()
    )
    session.add(new_product)
    session.commit()
    return new_product


@app.post("/products")
def add_products(products: schemas.ProductList, session: Session = Depends(get_session)):
    new_products = products.data
    for product in new_products:
        new_prod = models.Product(
            name=product.name,
            price=product.price,
            id=uuid.uuid4()
        )
        session.add(new_prod)
        session.commit()
    return new_products


@app.get("/{id}")
def get_single_product(id: uuid.UUID, session: Session = Depends(get_session)):
    product = session.query(models.Product).get({"id": id})
    return product


@app.put("/{id}")
def update_single_product(id: uuid.UUID, new_product: schemas.Product, session: Session = Depends(get_session)):
    product = session.query(models.Product).get(id)
    if product:
        product.name = new_product.name
        product.price = new_product.price
        session.commit()
        session.refresh(product)
    return product


@app.delete("/{id}")
def delete_single_product(id: uuid.UUID, session: Session = Depends(get_session)):
    product = session.query(models.Product).get(id)
    if product:
        session.delete(product)
        session.commit()
    return {"message": "Successful"}
