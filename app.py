from models import Base, session, engine, Brand, Product
from csv_readers import add_brands, add_products
from cleaners import clean_id, clean_date, clean_price, clean_quantity
from datetime import date

def view_product():
    product_options = []
    for product in session.query(Product):
        product_options.append(product.product_id)
    id_error = True
    while id_error:
        product_choice = input(f'''\nOptions:
            \r{product_options}
            \rSelect a product ID: ''')
        product_choice = clean_id(product_choice,product_options)
        if type(product_choice) == int:
            id_error = False
    the_product = session.query(Product).filter(Product.product_id==product_choice).first()
    product_brand = session.query(Brand).filter(Brand.brand_id == the_product.brand_id).first()
    print(f'''\nID:{the_product.product_id}
        \rProduct Name: {the_product.product_name}
        \rPrice: {the_product.product_price}
        \rQuantity: {the_product.product_quantity}
        \rLast Updated: {the_product.date_updated}
        \rBrand: {product_brand.brand_name}''')

    while True:
        print(f'''\nU) UPDATE PRODUCT DETAILS
        \rD) DELETE PRODUCT
        \rX) RETURN TO MAIN MENU''')
        choice = input('\nWhat would you like to do?')
        if choice.upper() == 'U':
            print(f'''\n***UPDATE PRODUCT DETAILS***
                \rPress enter to skip attributes you are not updating''')
            product_name = input('Product Name: ')
            product_price = input('Product Price: ')
            product_quantity = input('Product Quantity: ')
            session.query(Product).filter(Product.product_id == the_product.product_id).update({
                Product.product_name: product_name,
                Product.product_price: clean_price(product_price),
                Product.product_quantity: clean_quantity(product_quantity),
                Product.date_updated: date.today()
            })
            session.commit()

        elif choice.upper() == 'D':
            return
        else:
            return



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
            print('Add a product')
        elif choice.upper() == 'A':
            print('View Analysis')
        elif choice.upper() == 'B':
            print('Backup')
        else:
            print('Goodbye')
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_brands()
    add_products()
    app()