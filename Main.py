import librarian
import student

def librarian_menu():
    while True:
        print("\nLibrarian Menu:")
        print("1. Add Book")
        print("2. Display All Books")
        print("3. Delete Book")
        print("4. Issue Book")
        print("5. Submit Book")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            librarian.add_book(title, author)
        
        elif choice == "2":
            librarian.display_books()
        
        elif choice == "3":
            book_id = int(input("Enter book ID to delete: "))
            librarian.delete_book(book_id)
        
        elif choice == "4":
            book_id = int(input("Enter book ID to issue: "))
            student_name = input("Enter student's name: ")
            librarian.issue_book(book_id, student_name)
        
        elif choice == "5":
            book_id = int(input("Enter book ID to submit: "))
            librarian.submit_book(book_id)

        elif choice == "6":
            break

        else:
            print("Invalid choice! Try again.")

def student_menu():
    while True:
        print("\nStudent Menu:")
        print("1. Display All Books")
        print("2. Issue Book")
        print("3. Submit Book")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student.display_books()
        
        elif choice == "2":
            book_id = int(input("Enter book ID to issue: "))
            student_name = input("Enter your name: ")
            student.issue_book(book_id, student_name)

        elif choice == "3":
            book_id = int(input("Enter book ID to submit: "))
            student.submit_book(book_id)

        elif choice == "4":
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    while True:
        print("\nWelcome to Library Management System")
        print("1. Librarian")
        print("2. Student")
        print("3. Exit")

        user_type = input("Enter your role: ")

        if user_type == "1":
            librarian_menu()
        elif user_type == "2":
            student_menu()
        elif user_type == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")
