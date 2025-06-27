import sqlite3

conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
''')
conn.commit()


def add_book(title, author, price, quantity):
    cursor.execute('INSERT INTO books (title, author, price, quantity) VALUES (?, ?, ?, ?)',
                   (title, author, price, quantity))
    conn.commit()
    print("Book added successfully!")


def view_books():
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    print("\n Available Books:")
    for book in books:
        print(book)

def sell_book(book_id, qty_sold):
    cursor.execute('SELECT quantity FROM books WHERE id=?', (book_id,))
    result = cursor.fetchone()
    if result:
        current_qty = result[0]
        if qty_sold <= current_qty:
            cursor.execute('UPDATE books SET quantity = quantity - ? WHERE id = ?', (qty_sold, book_id))
            conn.commit()
            print(" Book sold!")
        else:
            print(" Not enough stock!")
    else:
        print(" Book not found!")

def search_book(title):
    cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
    results = cursor.fetchall()
    for book in results:
        print(book)

def delete_book(book_id):
    cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
    conn.commit()
    print("🗑 Book deleted.")

def menu():
    while True:
        print("\n Bookstore Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Sell Book")
        print("4. Search Book")
        print("5. Delete Book")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            title = input("Title: ")
            author = input("Author: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            add_book(title, author, price, quantity)
        elif choice == '2':
            view_books()
        elif choice == '3':
            book_id = int(input("Book ID to sell: "))
            qty_sold = int(input("Quantity sold: "))
            sell_book(book_id, qty_sold)
        elif choice == '4':
            title = input("Enter title to search: ")
            search_book(title)
        elif choice == '5':
            book_id = int(input("Book ID to delete: "))
            delete_book(book_id)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

menu()

conn.close()