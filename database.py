import sqlite3 as sql
from contextlib import contextmanager

@contextmanager
def get_connection():
    connect = sql.connect("prices.db")
    try:
        yield connect
        connect.commit()
        
    finally:
        connect.close()
        
        
def create_table():
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS prices (product TEXT, price INTEGER, url TEXT UNIQUE)")


def add_product(product, price, url):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("INSERT INTO prices (product, price, url) VALUES(?, ?, ?)", (product, price, url))



def get_all_products():
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM prices")
        return cursor.fetchall()


def get_products_by_url(url):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM prices WHERE url = ?", (url,))
        return cursor.fetchone()


def update_price(url, new_price):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("UPDATE prices SET price = ? WHERE url = ?", (new_price, url))

if __name__ == '__main__':
    create_table()
    