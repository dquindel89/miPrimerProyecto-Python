from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        #Creating a Frame container
        frame = LabelFrame(self.wind, text = 'Register A new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button Add Product
        ttk.Button(frame, text = 'Save Product', command = self.add_products).grid(row = 3, columnspan = 2, sticky = W + E)

        #Output Messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)


        #Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column= 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)

        self.get_products()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):

        #Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # query data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        #filling data
        for row in db_rows:
            #print(row)
            self.tree.insert('', 0, text = row[1], values = row[2])
        
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_products(self):
        if self.validation():
            #print(self.name.get())
            #print(self.price.get())
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            #print('Data saved')
            self.message['text'] = 'Product {} added successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)

        else:
            #print('Name and price requiered')
            self.message['text'] = 'Name and price are Required'
        self.get_products()

if __name__ =='__main__':
    window = Tk()
    Application = Product(window)
    window.mainloop()