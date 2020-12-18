import psycopg2 as ps
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get_user_info(self):
        return self.username, self.password


class Database(object):
    def __init__(self, user, dbname):
        self.user = user
        self.dbname = dbname
        self.connection = None

        status = self.connect()
        if not status:
            raise ValueError("Failed to log in")
        
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
        self.cursor = self.connection.cursor()
        with open("sql/database.sql", 'r') as file:
            self.cursor.execute(file.read())

        status = self.connect(self.dbname)
        if not status:
            self.create_database(self.dbname)

        with open("sql/functions.sql", 'r') as file:
            self.cursor.execute(file.read())

    def connect(self, name='postgres'):
        username, password = self.user.get_user_info()
        try:
            self.connection = ps.connect(
                host='localhost', 
                port='5432',
                database=name,
                user=username,
                password=password
                )
            return True
        except ps.OperationalError:
            return False
    
    def create_database(self, name):
        user = self.user.get_user_info() 
        self.cursor.callproc("create_database", (name, *user))

    def delete_database(self):
        self.cursor.close()
        self.connection.close()
        self.connect()
        self.cursor = self.connection.cursor()
        with open("database.sql", 'r') as file:
            self.cursor.execute(file.read())
        user = self.user.get_user_info() 
        self.cursor.callproc("delete_database", (self.dbname, *user))

    def edit_book_by_title(self, *args):
        self.cursor.execute("SELECT edit_book_by_title{}".format(*args))
    
    def edit_book_by_author(self, *args):
        self.cursor.execute("SELECT edit_book_by_author{}".format(*args))
    
    def edit_book_by_price(self, *args):
        self.cursor.execute("SELECT edit_book_by_price{}".format(*args))

    def edit_book_by_amount(self, *args):
        self.cursor.execute("SELECT edit_book_by_amount{}".format(*args))

    def edit_person_by_firstname(self, *args):
        self.cursor.execute("SELECT edit_person_by_firstname{}".format(*args))
    
    def edit_person_by_lastname(self, *args):
        self.cursor.execute("SELECT edit_person_by_lastname{}".format(*args))

    def edit_person_by_patronymic(self, *args):
        self.cursor.execute("SELECT edit_person_by_patronymic{}".format(*args))

    def edit_person_by_discount(self, *args):
        self.cursor.execute("SELECT edit_person_by_discount{}".format(*args))

    def edit_purchase_by_day(self, *args):
        self.cursor.execute("SELECT edit_purchase_by_day{}".format(*args))

    def edit_purchase_by_month(self, *args):
        self.cursor.execute("SELECT edit_purchase_by_month{}".format(*args))

    def add_person(self, *args):
        self.cursor.execute("SELECT add_new_person{}".format(*args))

    def add_book(self,*args):
        self.cursor.execute("SELECT add_new_book{}".format(*args))

    def add_purchase(self, *args):
        self.cursor.execute("SELECT add_new_purchase{}".format(*args))

    def delete_by_author(self, author):
        self.cursor.execute("SELECT delete_by_author('{}')".format(author))

    def delete_by_lastname(self, last_name):
        self.cursor.execute("SELECT delete_by_lastname('{}')".format(last_name))

    def delete_by_book_id(self, book_id):
        self.cursor.execute("SELECT delete_by_book_id('{}')".format(book_id))

    def clear_purchase_table(self):
        self.cursor.execute("SELECT clear_purchase_records()")

    def clear_person_table(self):
        self.cursor.execute("SELECT clear_person_records()")

    def clear_book_table(self):
        self.cursor.execute("SELECT clear_book_records()")

    def clear_all_tables(self):
        self.cursor.execute("SELECT clear_all_records()")

    def delete_book_record(self, id):
        self.cursor.execute("SELECT delete_book_record('{}')".format(id))

    def delete_person_record(self, id):
        self.cursor.execute("SELECT delete_person_record('{}')".format(id))

    def delete_purchase_record(self, id):
        self.cursor.execute("SELECT delete_purchase_record('{}')".format(id))

    def search_by_author(self, author):
        self.cursor.execute("SELECT search_by_author('{}')".format(author))
        return self.cursor.fetchall()

    def search_by_lastname(self, last_name):
        self.cursor.execute("SELECT search_by_lastname('{}')".format(last_name))
        return self.cursor.fetchall()

    def search_by_book_id(self, book_id):
        self.cursor.execute("SELECT search_by_book_id('{}')".format(book_id))
        return self.cursor.fetchall()

    def view_book(self):
        self.cursor.execute("SELECT view_book()")
        return self.cursor.fetchall()

    def view_person(self):
        self.cursor.execute("SELECT view_person()")
        return self.cursor.fetchall()

    def view_purchase(self):
        self.cursor.execute("SELECT view_purchase()")
        return self.cursor.fetchall()
