from models import Base, session, engine, Brand, Product
from csv_readers import add_brands, add_products
from cleaners import clean_id, clean_date, clean_price, clean_quantity
from datetime import date
from sqlalchemy import func, desc
import csv

def view_product():
    ###Create a list of product IDs
    product_options = []
    for product in session.query(Product):
        product_options.append(product.product_id)

    ###Prompt the user for an ID until a valid entry is provided   
    id_error = True
    while id_error:
        product_choice = input(f'''\nOptions:
            \r{product_options}
            \rSelect a product ID: ''')
        product_choice = clean_id(product_choice,product_options)
        if type(product_choice) == int:
            id_error = False

    ##fetch the product and brand from DB
    the_product = session.query(Product).filter(Product.product_id==product_choice).first()
    product_brand = session.query(Brand).filter(Brand.brand_id == the_product.brand_id).first()

    ##display product and options menu
    while True:
        print(f'''\nID:{the_product.product_id}
        \rProduct Name: {the_product.product_name}
        \r{f"Price: {the_product.product_price / 100}"}
        \rQuantity: {the_product.product_quantity}
        \rLast Updated: {the_product.date_updated}
        \rBrand: {product_brand.brand_name}''')
        print(f'''\nU) UPDATE PRODUCT DETAILS
        \rD) DELETE PRODUCT
        \rX) RETURN TO MAIN MENU''')
        choice = input('\nWhat would you like to do? ')
        if choice.upper() == 'U':
            print(f'''\n***UPDATE PRODUCT DETAILS***
                \rPress enter to skip attributes you are not updating''')
            product_name = input('Product Name: ')
            # Loop for price input
            while True:
                product_price = input('Product Price: ')
                if product_price:
                    cleaned_price = clean_price(product_price)
                    if cleaned_price is not None:
                        break
                else:
                    cleaned_price = Product.product_price
                    break

            # Loop for quantity input
            while True:
                product_quantity = input('Product Quantity: ')
                if product_quantity:
                    cleaned_quantity = clean_quantity(product_quantity)
                    if cleaned_quantity is not None:
                        break
                else:
                    cleaned_quantity = Product.product_quantity
                    break

            # Update the database
            session.query(Product).filter(Product.product_id == the_product.product_id).update({
                Product.product_name: product_name if product_name else Product.product_name,
                Product.product_price: cleaned_price,
                Product.product_quantity: cleaned_quantity,
                Product.date_updated: date.today()
            })
            session.commit()
            print(f'''\n********
                \rProduct details updated successfully
                \r********''')
        elif choice.upper() == 'D':
            confirm_delete = input(f'''\n{'*' * 20}
            \rDELETE WARNING
            \rAre you sure you want to delete "{the_product.product_name}" with product ID#: {the_product.product_id}?
            \rThis cannot be undone
            \r{'*' * 20}
            \r[Y/N]: ''')
            if confirm_delete.upper() == 'Y':
                session.delete(the_product)
                session.commit()
                print(f"\n{the_product.product_name} with ID {the_product.product_id} has been deleted.")
                break
            else:
                continue
        else:
            return


def add_product():
    print(f'''\n***ADD A PRODUCT TO INVENTORY***''')
    product_name = input('Product Name: ')
    date_updated = date.today()
    # Loop for price input
    while True:
        product_price = input('Product Price: ')
        if product_price:
            cleaned_price = clean_price(product_price)
            if cleaned_price is not None:
                break
        else:
            cleaned_price = Product.product_price
            break
    # Loop for quantity input
    while True:
        product_quantity = input('Product Quantity: ')
        if product_quantity:
            cleaned_quantity = clean_quantity(product_quantity)
            if cleaned_quantity is not None:
                break
        else:
            cleaned_quantity = Product.product_quantity
            break
    
    brand_name = input("Brand Name: ")
    ## Insert Brand in DB if it does not currently exist
    brand_id = None
    brand_in_db = session.query(Brand).filter(Brand.brand_name == brand_name).one_or_none()
    if brand_in_db == None:
        brand_name = brand_name
        new_brand = Brand(brand_name=brand_name)
        session.add(new_brand)
        session.commit()
        brand_id = new_brand.brand_id
    else:
        brand_id = brand_in_db.brand_id

    product_in_db = session.query(Product).filter(Product.product_name == product_name).one_or_none()
    if product_in_db is None:
        new_product = Product(product_name=product_name, product_price=cleaned_price, product_quantity=cleaned_quantity, date_updated=date_updated, brand_id=brand_id)
        session.add(new_product)
    else:
        product_in_db.product_price = product_price
        product_in_db.product_quantity = product_quantity
        product_in_db.date_updated = date_updated
        product_in_db.brand_id = brand_id
    session.commit()

def inventory_analysis():
    total_inventory = sum(product.product_quantity for product in session.query(Product.product_quantity).all())
    total_products = session.query(Product).count()
    most_expensive_product = session.query(Product).order_by(Product.product_price.desc()).first()
    least_expensive_product = session.query(Product).order_by(Product.product_price.asc()).first()
    brand_with_most_inventory = session.query(
        Brand.brand_name, 
        func.sum(Product.product_quantity).label('total_quantity')
        ).join(Brand, Brand.brand_id == Product.brand_id) \
        .group_by(Brand.brand_name) \
        .order_by(desc('total_quantity')) \
        .first()
    print(f'''\n{'-'*40}\nINVENTORY ANALYSIS
        \nMost Expensive Product: {most_expensive_product.product_name} - ${most_expensive_product.product_price}
        \rLeast Expensive Product: {least_expensive_product.product_name} - ${least_expensive_product.product_price}
        \rBrand With Most Inventory: {brand_with_most_inventory[0]} - Total Qty: {brand_with_most_inventory[1]}
        \rTotal Inventory Across All Brands: {total_inventory})
        \rAverage Price Across All Products: 
        \n{'-'*40}''')
    
def backup_database_to_csv():
    # Backup Brands
    brands = session.query(Brand).all()
    with open('brands_backup.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['brand_name'])  # Header
        for brand in brands:
            writer.writerow([brand.brand_name])

    # Backup Products
    products = session.query(Product).all()
    with open('inventory_backup.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['product_name','product_price', 'product_quantity', 'date_updated', 'brand_name'])  # Header
        for product in products:
            brand_name = session.query(Brand).filter(Brand.brand_id == product.brand_id).first()
            formatted_price = f'${product.product_price}'
            writer.writerow([product.product_name, formatted_price, product.product_quantity, product.date_updated, brand_name.brand_name])

    print("Backups saved to 'brands_backup.csv' and 'products_backup.csv'")


def menu():
    while True:
        print(f'''\n***Grocery Inventory V1***
            \r
            \rV) VIEW PRODUCT DETAILS
            \rN) ADD A PRODUCT 
            \rA) VIEW ANALYSIS  
            \rB) BACKUP 
            \rX) EXIT  ''')
        choice = input('\nWhat would you like to do? ')
        if choice.upper() in ['V', 'N', 'A', 'B', 'X']:
            return(choice)
        else:
            input(f'''\n********
                \rTry again. Please enter a valid option: [V, N, A, B , X]
                \rPress enter to try again.
                \r********''')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.upper() == 'V':
            view_product()
        elif choice.upper() == 'N':
            add_product()
        elif choice.upper() == 'A':
            inventory_analysis()
        elif choice.upper() == 'B':
            backup_database_to_csv()
        else:
            print('Goodbye')
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_brands()
    add_products()
    app()