import datetime

def clean_price(price_string):
    try:
        split_price = price_string.split('$')
        price_float = float(split_price[1])
    except ValueError:
        input('''
            \n***** PRICE ERROR *****
            \r The price should be a number with a currency symbol.
            \r Ex: $21.99
            \n Press Enter to try again
            \r*********************''')
    else:
        return price_float
    
def clean_date(date_string):
    try:
        split_date = date_string.split('/')
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year,month,day)
    except ValueError:
        input('''
            \n***** DATE ERROR *****
            \r The date format should include a valid Month Day and Year from the past.
            \r Ex: 02/01/2015
            \n Press Enter to try again
            \r*********************
            \r''')
        return
    else:
        return return_date

def clean_quantity(qty_string):
    try:
        qty = int(qty_string)
    except ValueError:
        input(f'''
            \n***** QUANTITY ERROR *****
            \r The Quantity should be a an integer
            \r Ex: 5
            \rPress Enter to try again
            \r*********************''')
    else:
        return  qty

    