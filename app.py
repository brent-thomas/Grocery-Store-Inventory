from models import Base, session, engine, Brand, Product
import csv 


def clean_price(price_string):
    try:
        price_float = float(price_string)
    except ValueError:
        input('''
            \n***** PRICE ERROR *****
            \r The price should be a number without a currency symbol.
            \r Ex: 21.99
            \n Press Enter to try again
            \r*********************''')
    else:
        return int(price_float * 100)
    

def add_brands():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
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
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = row[2]
                date_updated =  row[3]
                brand = session.query(Brand).filter(Brand.brand_name == row[4]).first()
                brand_id = brand.brand_id

if __name__ == '__main__':
    #Base.metadata.create_all(engine)
    add_brands()
    add_products()
    