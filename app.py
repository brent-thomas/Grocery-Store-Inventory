from models import Base, session, engine, Brand, Product
from csv_readers import add_brands, add_products

def clean_id(id_string, options):
    try:
        product_id = int(id_string)
    except ValueError:
        input('''
            \n***** ID ERROR *****
            \r The ID should be a number
            \r Press Enter to try again
            \r*********************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
            \n***** ID ERROR *****
            \r Options: {options}
            \rPress Enter to try again
            \r*********************''')
            return

def view_product():
    product_options = []
    for product in session.query(Product):
        product_options.append(product.product_id)
    id_error = True
    while id_error:
        product_choce = input(f'''\nOptions:
            \r{product_options}
            \rSelect a product ID: ''')
        product_choce = clean_id(product_choce,product_options)
        if type(product_choce) == int:
            id_error = False
    the_product = session.query(Product).filter(Product.product_id==product_choce).first()
    product_brand = session.query(Brand).filter(Brand.brand_id == the_product.brand_id).first()
    print(f'''\nID:{the_product.product_id}
        \rProduct Name: {the_product.product_name}
        \rPrice: {the_product.product_price}
        \rQuantity: {the_product.product_quantity}
        \rLast Updated: {the_product.date_updated}
        \rBrand: {product_brand.brand_name}''')
    input('\n\nPRESS ENTER TO RETURN TO THE MAIN MENU')



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