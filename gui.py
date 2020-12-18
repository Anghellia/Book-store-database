from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5 import uic

from database import User, Database


def show_error_message(error, icon=QMessageBox.Warning):
        error_message = QMessageBox()
        error_message.setWindowTitle("Error")
        error_message.setIcon(icon)
        error_message.setText(error)
        error_message.addButton(QMessageBox.Ok)
        error_message.exec()


class QuestionWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/QuestionWindow.ui", self)
        self.db = None
        self.query_status = False
        self.dialog_button.rejected.connect(self.close_window)
        self.dialog_button.accepted.connect(self.set_status)

    def close_window(self):
        self.close()

    def set_status(self):
        self.query_status = True
        self.close_window()

    def get_status(self):
        return self.query_status


class AddWindow(QDialog):
    def __init__(self, table_name):
        super().__init__()
        uic.loadUi("design/AddWindow.ui", self)
        self.db = None
        self.table_name = table_name

        if self.table_name == 'purchase':
            self.label1.setText('title')
            self.label2.setText('first_name')
            self.label3.setText('last_name')
            self.label4.setText('patronymic')
            self.label5.setText('dd')
            self.label6.setText('mm')
        else:
            self.label1.setVisible(False)
            self.label6.setVisible(False)
            self.text1.setVisible(False)
            self.text6.setVisible(False)

            if self.table_name == 'book':
                self.label2.setText('title')
                self.label3.setText('author')
                self.label4.setText('price')
                self.label5.setText('amount')

            elif self.table_name == 'person':
                self.label2.setText('first_name')
                self.label3.setText('last_name')
                self.label4.setText('patronymic')
                self.label5.setText('discount')

        self.dialog_button.accepted.connect(self.add_rec)

    def add_rec(self):
        if self.table_name == 'book':
            title = self.text2.text()
            author = self.text3.text()
            price = self.text4.text()
            amount = self.text5.text()
            if title and author and price and amount:
                try:
                    self.db.add_book((title, author, price, amount))
                except:
                    show_error_message("Error during adding the record!")
            else:
                show_error_message("The one of the fields is empty!") 
        elif self.table_name == 'person':
            first_name = self.text2.text()
            last_name = self.text3.text()
            patronymic = self.text4.text()
            discount = self.text5.text()
            if first_name and last_name and patronymic and discount:
                try:
                    self.db.add_person((first_name, last_name, patronymic, discount))
                except:
                    show_error_message("Error during adding the record!")
            else:
                show_error_message("The one of the fields is empty!") 
        elif self.table_name == 'purchase':
            title = self.text1.text()
            first_name = self.text2.text()
            last_name = self.text3.text()
            patronymic = self.text4.text()
            dd = self.text5.text()
            mm = self.text6.text()
            if title and first_name and last_name and patronymic and dd and mm:
                try:
                    self.db.add_purchase((title, first_name, last_name, patronymic, dd, mm))
                except:
                    show_error_message("Error during adding the record!")
            else:
                show_error_message("The one of the fields is empty!")


class SearchDeleteWindow(QDialog):
    def __init__(self, table_name):
        super().__init__()
        uic.loadUi("design/SearchDeleteWindow.ui", self)
        self.db = None
        self.table_name = table_name
        self.data = None
        self.status = False

        if self.table_name == 'purchase':
            self.label.setText('Book_id:')
        elif self.table_name == 'book':
            self.label.setText('Author:')
        elif self.table_name == 'person':
            self.label.setText('Last_name:')

        self.search_button.clicked.connect(lambda: self.search_by_index(self.table_name))
        self.delete_button.clicked.connect(lambda: self.delete_by_index(self.table_name))
        self.cancel_button.clicked.connect(self.close_window)

    def search_by_index(self, table_name):
        index = self.index.text()
        self.status = True
        if not index:
            show_error_message("The field is empty!")
        if self.table_name == 'book':
            try:
                self.data = self.db.search_by_author(index)
            except:
                show_error_message('The index is invalid!')
        elif self.table_name == 'person':
            try:
                self.data = self.db.search_by_lastname(index)
            except:
                show_error_message('The index is invalid!')
        elif self.table_name == 'purchase':
            try:
                self.data = self.db.search_by_book_id(index)
            except:
                show_error_message('The index is invalid!')
        self.close()

    def delete_by_index(self, table_name):
        index = self.index.text()
        self.status = True
        if not index:
            show_error_message("The field is empty!")
        if self.table_name == 'book':
            try:
                self.db.delete_by_author(index)
            except:
                show_error_message('The index is invalid!')
        elif self.table_name == 'person':
            try:
                self.db.delete_by_lastname(index)
            except:
                show_error_message('The index is invalid!')
        elif self.table_name == 'purchase':
            try:
                self.db.delete_by_book_id(index)
            except:
                show_error_message('The index is invalid!')
        self.close()

    def close_window(self):
        self.close()


class ConnectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/ConnectWindow.ui", self)
        self.connect_button.clicked.connect(self.connect_to_database)

        self.show()

    def connect_to_database(self):
        user = User(self.username.text(), self.password.text())
        db_name = self.database_name.text()
       
        try:
            database = Database(user, db_name)
            # show main window
            self.window = MainWindow()
            self.window.db = database
            self.window.show() 
            # close connect window
            self.close()
        except ValueError:
            show_error_message("Failed to log in")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = None
        uic.loadUi("design/MainWindow.ui", self)

        ## Book table
        self.book_columns = ['id', 'title', 'author', 'price', 'amount']
        self.book_table.setColumnCount(5)
        self.book_table.setHorizontalHeaderLabels(self.book_columns)
        self.book_buttons = [self.add_book_record, self.delete_book_record, self.clear_books_records,
                             self.search_delete_by_book, self.book_table]
        ### Person table
        self.person_columns = ['id', 'first_name', 'last_name', 'patronymic', 'discount']
        self.person_table.setColumnCount(5)
        self.person_table.setHorizontalHeaderLabels(self.person_columns)
        self.person_buttons = [self.add_person_record, self.delete_person_record, self.clear_people_records,
                               self.search_delete_by_person, self.person_table]
        ### Purchase table
        self.purchase_columns = ['id', 'book_id', 'person_id', 'dd', 'mm', 'purchase_price']
        self.purchase_table.setColumnCount(6)
        self.purchase_table.setHorizontalHeaderLabels(self.purchase_columns)
        self.purchase_buttons = [self.add_purchase_record, self.delete_purchase_record, self.clear_purchases_records,
                                 self.search_delete_by_purchase, self.purchase_table]

        for button in self.book_buttons + self.person_buttons + self.purchase_buttons:
            button.setVisible(False)

        ## table buttons
        self.book_button.clicked.connect(lambda: self.show_table('book'))
        self.book_button.pressed.connect(lambda: self.change_color('book'))

        self.person_button.clicked.connect(lambda: self.show_table('person'))
        self.person_button.pressed.connect(lambda: self.change_color('person'))

        self.purchase_button.clicked.connect(lambda: self.show_table('purchase'))
        self.purchase_button.pressed.connect(lambda: self.change_color('purchase'))

        ## add buttons
        self.add_book_record.clicked.connect(lambda: self.add_record('book'))
        self.add_person_record.clicked.connect(lambda: self.add_record('person'))
        self.add_purchase_record.clicked.connect(lambda: self.add_record('purchase'))

        ## delete database
        self.delete_database.clicked.connect(self.delete_db)

        ## clear all records
        self.clear_all_records.clicked.connect(self.clear_records)

        ## clear records buttons
        self.clear_books_records.clicked.connect(lambda: self.clear_table_records('book'))
        self.clear_people_records.clicked.connect(lambda: self.clear_table_records('person'))
        self.clear_purchases_records.clicked.connect(lambda: self.clear_table_records('purchase'))

        ## search/delete buttons
        self.search_delete_by_book.clicked.connect(lambda: self.query_by_index('book'))
        self.search_delete_by_person.clicked.connect(lambda: self.query_by_index('person'))
        self.search_delete_by_purchase.clicked.connect(lambda: self.query_by_index('purchase'))

        ## delete record buttons
        self.delete_book_record.clicked.connect(lambda: self.delete_record('book'))
        self.delete_person_record.clicked.connect(lambda: self.delete_record('person'))
        self.delete_purchase_record.clicked.connect(lambda: self.delete_record('purchase'))

        ## edit
        self.book_table.itemChanged.connect(self.edit_book_record)
        self.person_table.itemChanged.connect(self.edit_person_record)
        self.purchase_table.itemChanged.connect(self.edit_purchase_record)
        self.change_status = True

    def set_data(self, table, columns, data):
        self.change_status = False
        try:
            if data is not None:
                table.setRowCount(len(data))
                data = [x[0][1:-1] for x in data]
                data = [x.split(',') for x in data]
                for i, row in enumerate(data):
                    for j, col in enumerate(columns):
                        table.setItem(i, j, QTableWidgetItem(row[j]))
                if table.columnCount() == 6:
                    table.setColumnWidth(3, 60)
                    table.setColumnWidth(4, 60)
                    table.setColumnWidth(5, 200)
                else:
                    table.setColumnWidth(3, 150)
                table.setColumnWidth(0, 60)
                table.setColumnWidth(1, 150)
                table.setColumnWidth(2, 150)
            else:
                table.setRowCount(0)
        except:
            self.message("Error during setting data!")
        self.change_status = True

    def query_by_index(self, table_name):
        self.window = SearchDeleteWindow(table_name)
        self.window.db = self.db
        self.window.exec()
        data = self.window.data
        if not self.window.status:
            return
        if table_name == 'book':
            new_data = data if data else self.db.view_book()
            self.set_data(self.book_table, self.book_columns, new_data)
        elif table_name == 'person':
            new_data = data if data else self.db.view_person()
            self.set_data(self.person_table, self.person_columns, new_data)
        elif table_name == 'purchase':
            new_data = data if data else self.db.view_purchase()
            self.set_data(self.purchase_table, self.purchase_columns, new_data)

    def add_record(self, table_name):
        self.window = AddWindow(table_name)
        self.window.db = self.db
        self.window.exec()
        if table_name == 'book':
            self.set_data(self.book_table, self.book_columns, self.db.view_book())
        elif table_name == 'person':
            self.set_data(self.person_table, self.person_columns, self.db.view_person())
        elif table_name == 'purchase':
            self.set_data(self.purchase_table, self.purchase_columns, self.db.view_purchase())

    def delete_record(self, table_name):
        if table_name == 'book':
            items = self.book_table.selectedItems()
            if len(items) != 5:
                show_error_message("Select the record to delete!")
            else:
                row_id = items[0].text()
                self.db.delete_book_record(row_id)
                self.set_data(self.book_table, self.book_columns, self.db.view_book())
        elif table_name == 'person':
            items = self.person_table.selectedItems()
            if len(items) != 5:
                show_error_message("Select the record to delete!")
            else:
                row_id = items[0].text()
                self.db.delete_person_record(row_id)
                self.set_data(self.person_table, self.person_columns, self.db.view_person())
        elif table_name == 'purchase':
            items = self.purchase_table.selectedItems()
            if len(items) != 6:
                show_error_message("Select the record to delete!")
            else:
                row_id = items[0].text()
                self.db.delete_purchase_record(row_id)
                self.set_data(self.purchase_table, self.purchase_columns, self.db.view_purchase())

    def edit_book_record(self, item):
        if not self.change_status:
            return
        if item.column() == 1:
            try:
                self.db.edit_book_by_title((item.text(), self.book_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 2:
            try:
                self.db.edit_book_by_author((item.text(), self.book_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 3:
            try:
                self.db.edit_book_by_price((item.text(), self.book_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 4:
            try:
                self.db.edit_book_by_amount((item.text(), self.book_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        self.set_data(self.book_table, self.book_columns, self.db.view_book())

    def edit_person_record(self, item):
        if not self.change_status:
            return
        if item.column() == 1:
            try:
                self.db.edit_person_by_firstname((item.text(), self.person_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 2:
            try:
                self.db.edit_person_by_lastname((item.text(), self.person_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 3:
            try:
                self.db.edit_person_by_patronymic((item.text(), self.person_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 4:
            try:
                self.db.edit_person_by_discount((item.text(), self.person_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        self.set_data(self.person_table, self.person_columns, self.db.view_person())

    def edit_purchase_record(self, item):
        if not self.change_status:
            return
        if item.column() == 3:
            try:
                self.db.edit_purchase_by_day((item.text(), self.purchase_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        elif item.column() == 4:
            try:
                self.db.edit_purchase_by_month((item.text(), self.purchase_table.item(item.row(), 0).text()))
            except:
                show_error_message('The value is invalid!')
        self.set_data(self.purchase_table, self.purchase_columns, self.db.view_purchase())

    def call_question_window(self):
        self.window = QuestionWindow()
        self.window.exec()
        return self.window.get_status()

    def delete_db(self):
        if self.call_question_window():
            self.db.delete_database()
            self.close()

    def clear_table_records(self, table_name):
        if self.call_question_window():
            if table_name == 'book':
                self.db.clear_book_table()
                self.set_data(self.book_table, self.book_columns, self.db.view_book())
            elif table_name == 'person':
                self.db.clear_person_table()
                self.set_data(self.person_table, self.person_columns, self.db.view_person())
            elif table_name == 'purchase':
                self.db.clear_purchase_table()
                self.set_data(self.purchase_table, self.purchase_columns, self.db.view_purchase())

    def clear_records(self):
        if self.call_question_window():
            self.db.clear_all_tables()
            self.set_data(self.book_table, self.book_columns, None)
            self.set_data(self.person_table, self.person_columns, None)
            self.set_data(self.purchase_table, self.purchase_columns, None)

    def show_table(self, table_name):
        if table_name == 'book':
            self.set_data(self.book_table, self.book_columns, self.db.view_book())
            for button in self.book_buttons:
                button.setVisible(True)
            for button in self.person_buttons + self.purchase_buttons:
                button.setVisible(False)
        elif table_name == 'person':
            self.set_data(self.person_table, self.person_columns, self.db.view_person())
            for button in self.person_buttons:
                button.setVisible(True)
            for button in self.book_buttons + self.purchase_buttons:
                button.setVisible(False)
        elif table_name == 'purchase':
            self.set_data(self.purchase_table, self.purchase_columns, self.db.view_purchase())
            for button in self.purchase_buttons:
                button.setVisible(True)
            for button in self.book_buttons + self.person_buttons:
                button.setVisible(False)

    def change_color(self, table_name):
        pressed_style = "QPushButton{color:#333; border-radius:15px; background-color:rgb(197, 255, 250)}"
        not_pressed_style = """QPushButton{border-radius:60px; background-color:#e0aa9d}
                               QPushButton:hover{color:#333; border-radius:15px;
                                background-color:rgb(197, 255, 250)}"""
        if table_name == 'book':
            self.book_button.setStyleSheet(pressed_style)
            self.person_button.setStyleSheet(not_pressed_style)
            self.purchase_button.setStyleSheet(not_pressed_style)
        elif table_name == 'person':
            self.person_button.setStyleSheet(pressed_style)
            self.book_button.setStyleSheet(not_pressed_style)
            self.purchase_button.setStyleSheet(not_pressed_style)
        elif table_name == 'purchase':
            self.purchase_button.setStyleSheet(pressed_style)
            self.book_button.setStyleSheet(not_pressed_style)
            self.person_button.setStyleSheet(not_pressed_style)
