from models import session, Brand, Product
from cleaners import clean_date, clean_price, clean_quantity
import csv 


def add_brands():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data) #skipping header row
        for row in data:
            brand_in_db = session.query(Brand).filter(Brand.brand_name ==row[0]).one_or_none()
            if brand_in_db == None:
                brand_name = row[0]
                new_brand = Brand(brand_name=brand_name)
                session.add(new_brand)
        session.commit()


def add_products():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data) #skipping header row
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
                date_updated =   clean_date(row[3])
                brand = session.query(Brand).filter(Brand.brand_name == row[4]).first()
                brand_id = brand.brand_id
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
        session.commit()