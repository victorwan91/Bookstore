# Import module "sqlite3"
import sqlite3

# Creates or opens a file called "ebookstore" with a SQLite3 DB.
db = sqlite3.connect(":memory")

# Create a table called "books" with headings id, Title, Author and Qty where id as the primary key.
cursor = db.cursor()
cursor.execute("""
CREATE TABLE books
(id INTEGER PRIMARY KEY, 
Title TEXT, 
Author TEXT,
Qty INTEGER)
""")

# Save changes to the database.
db.commit()

# Put all data in "books_list" and insert into the table in the database.
book_list = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
             (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
             (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
             (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
             (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]
cursor.executemany("""INSERT INTO books(id, title, author, qty)
                                VALUES (?, ?, ?, ?)"""
                   , book_list)

# Save changes to the database.
db.commit()


# Define "display_updated_table()" function to display the updated table on the terminal.
def display_updated_table():
    cursor.execute(""" SELECT * FROM books""")
    print("\nUpdated Books Table")

    # Use for loop to print each row of the table.
    for row in cursor:
        print("{0} : {1} : {2}: {3}".format(row[0], row[1], row[2], row[3]))


# Define "add_book()" function that allows users to add new book detail to the database.
def add_book():
    # Request input of book ID and check if the ID is already existed in the database by using fetchall().
    # Print error message if it already exists.
    while True:
        try:
            add_id = int(input("Enter book ID: "))
            cursor.execute("""SELECT * FROM books 
                                       WHERE id = ?""",
                           (add_id,))
            if cursor.fetchall():
                print("This ID already exists, please enter a different ID")
                continue
            break

        # Except ValueError, print error message.
        except ValueError:
            print("Invalid input, please try again using numbers!")

    # Request input of new book title and author.
    add_title = input("Enter book title: ")
    add_author = input("Enter book author: ")

    # Request input of new quantity number.
    # Except ValueError, print error message.
    while True:
        try:
            add_qty = int(input("Enter book quantity: "))
            break
        except ValueError:
            print("Invalid input, please enter a number!")

    # Insert data into the table, save and display updated table.
    cursor.execute("""INSERT INTO books(id, Title, Author, Qty) 
                                 VALUES(?,?,?,?)""",
                   (add_id, add_title, add_author, add_qty))
    db.commit()
    display_updated_table()


# Define "update_book()" function allows users to update book details in the database.
def update_book():
    # Request input for the book ID and use fetchall function to check if the book exists,
    # If the book ID doesn't match to the database, print error message telling user the book doesn't exist.
    while True:
        try:
            update_id = int(input("Enter the book's ID you want to update: "))
            cursor.execute("""SELECT * FROM books 
                                       WHERE id = ?""",
                           (update_id,))
            if not cursor.fetchall():
                print("This book doesn't exist, please try again.")
                continue

            # Else, present the book update menu to the user.
            else:
                while True:
                    update_book_menu = input("""
Book Update Options:
1. Update book title.
2. Update book author.
3. Update book quantity.
0. Back to main menu.
Please enter a number to select an option: """)
                    
                    # If user chooses "1", request input for a new title and update the book title in the table.
                    # Print the updated table and break.
                    if update_book_menu == "1":
                        while True:
                            update_title = input("Enter the new title: ")
                            cursor.execute("""UPDATE books 
                                              SET Title = ? 
                                              WHERE id = ?""",
                                           (update_title, update_id))
                            db.commit()
                            display_updated_table()
                            break

                    # Elif, user chooses "2", request input for a new author and update the book author in the table.
                    # Print the updated table and break.
                    elif update_book_menu == "2":
                        while True:
                            update_author = input("Enter the new author: ")
                            cursor.execute("""UPDATE books 
                                              SET Author = ? 
                                              WHERE id = ?""",
                                           (update_author, update_id))
                            db.commit()
                            display_updated_table()
                            break

                    # Elif, user chooses "3", request input for a new quantity and update the book author in the table.
                    # Print the updated table and break.
                    elif update_book_menu == "3":
                        while True:
                            try:
                                update_qty = int(input("Enter the new quantity: "))
                                cursor.execute("""UPDATE books 
                                                  SET Qty = ? 
                                                  WHERE id = ?""",
                                               (update_qty, update_id))
                                db.commit()
                                display_updated_table()
                                break

                            # Except ValueError, then print error message
                            except ValueError:
                                print("Please try again using numbers!")

                    # Elif, if user chooses "0", return to the main menu.
                    elif update_book_menu == "0":
                        bookstore_clerk_menu()

                    # Else, print error message.
                    else:
                        print("Invalid input, please try again.")

        # Except ValueError, print error message.
        except ValueError:
            print("Invalid input. Please enter numbers.")


# Define "delete_book()" function that allows users to delete a book from the database.
def delete_book():
    # Request input for the book ID and use fetchall function to check if the book exists,
    # print error message if it doesn't.
    while True:
        try:
            delete_id = int(input("Enter the book ID that you want to delete: "))
            cursor.execute("""SELECT * FROM books 
                                       WHERE id = ?""",
                           (delete_id,))
            if not cursor.fetchall():
                print("This book doesn't exist, please try again.")
                continue

            # Else, delete the selected book from the database, save and break.
            else:
                cursor.execute("""DELETE FROM books
                                  WHERE id = ?""",
                               (delete_id,))
                db.commit()
                break

        # Except ValueError, print error message.
        except ValueError:
            print("Invalid input, please try again.")

    # Display the updated table by implementing "display_updated_table()" function.
    display_updated_table()


# Define "search_book()" function that allows user to search a specific book from the database.
def search_book():
    # Request input for the book ID and use fetchall function to check if the book exists,
    # print error message if it doesn't.
    while True:
        try:
            search_id = int(input("Enter the book ID that you want to search: "))
            cursor.execute("""SELECT * FROM books 
                                       WHERE id = ?""",
                           (search_id,))
            if not cursor.fetchall():
                print("This book doesn't exist, please try again.")
                continue

            # Else, select the book from the table and print the details of the selected book.
            else:
                cursor.execute('''SELECT * FROM books
                                           WHERE id = ?''',
                               (search_id,))
                view_book = cursor.fetchone()
                print("\nThe book you have selected:")
                print("{0} : {1} : {2}: {3}".format(view_book[0], view_book[1], view_book[2], view_book[3]))
                db.commit()
                break

        # Except ValueError, print error message.
        except ValueError:
            print("Invalid input, please try again.")


# Define "bookstore_clerk_menu()" function.
# Present the user with the menu for them to choose what action to take and store the menu in variable "menu".
def bookstore_clerk_menu():
    while True:
        menu = input("""
Bookstore Clerk Menu:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit 
Please enter a number to select an option: """)

        # If user chooses "0", close the connection with the DB, print goodbye message and exit the programme.
        if menu == "0":
            db.close()
            print("Goodbye!")
            exit()

        # If user chooses "1", call and implement "add_book()" function.
        elif menu == "1":
            add_book()

        # If user chooses "2", call and implement "update_book()" function
        elif menu == "2":
            update_book()

        # If user chooses "3", call and implement "delete_book()" function
        elif menu == "3":
            delete_book()

        # If user chooses "4", call and implement "search_book()" function
        elif menu == "4":
            search_book()

        # Else, if user enters something else, print error message.
        else:
            print("Invalid input, please try again!")


# Call and implement the "bookstore_clerk_menu()" function
bookstore_clerk_menu()
