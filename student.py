import sqlite3

def display_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()

    print("\nBooks in Library:")
    for book in books:
        print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | Issued To: {book[4]}")

def issue_book(book_id, student_name):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    
    cur.execute("SELECT status FROM books WHERE id=?", (book_id,))
    book = cur.fetchone()
    
    if book and book[0] == "Available":
        cur.execute("UPDATE books SET status='Issued', issued_to=? WHERE id=?", (student_name, book_id))
        conn.commit()
        print(f"Book {book_id} issued to {student_name}.")
    else:
        print("Book is not available for issuing.")
    
    conn.close()

def submit_book(book_id):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    
    cur.execute("UPDATE books SET status='Available', issued_to=NULL WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    print(f"Book {book_id} submitted successfully!")
