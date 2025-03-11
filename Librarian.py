import sqlite3

def add_book(title, author):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, status) VALUES (?, ?, 'Available')", (title, author))
    conn.commit()
    conn.close()
    print(f"Book '{title}' added successfully!")

def display_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()

    print("\nBooks in Library:")
    for book in books:
        print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | Issued To: {book[4]}")
