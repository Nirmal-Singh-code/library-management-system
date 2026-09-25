"""
Library Management System
--------------------------
A console-based Library Management System built with core Python + SQLite.

Concepts used (all beginner/intermediate, explainable in an interview):
- Classes and Objects (OOP)
- SQLite database (CRUD operations)
- Basic input validation
- datetime for due-date and fine calculation
- Simple menu-driven console app

Author: Nirmal Singh
"""

import sqlite3
from datetime import datetime, timedelta

DB_NAME = "library.db"
MAX_BOOKS_PER_MEMBER = 3
LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = 5  # in rupees


class Database:
    """Handles all direct interaction with the SQLite database."""

    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                is_available INTEGER DEFAULT 1
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                books_issued INTEGER DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                issue_date TEXT,
                due_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class Book:
    """Represents a single book and its database operations."""

    def __init__(self, db: Database):
        self.db = db

    def add_book(self, title, author):
        self.db.cursor.execute(
            "INSERT INTO books (title, author, is_available) VALUES (?, ?, 1)",
            (title, author)
        )
        self.db.commit()
        print(f"Book '{title}' added successfully.")

    def list_books(self):
        self.db.cursor.execute("SELECT book_id, title, author, is_available FROM books")
        rows = self.db.cursor.fetchall()
        print("\n--- All Books ---")
        for row in rows:
            status = "Available" if row[3] == 1 else "Issued"
            print(f"ID: {row[0]} | {row[1]} by {row[2]} | Status: {status}")

    def is_available(self, book_id):
        self.db.cursor.execute("SELECT is_available FROM books WHERE book_id = ?", (book_id,))
        result = self.db.cursor.fetchone()
        return result is not None and result[0] == 1

    def set_availability(self, book_id, available: bool):
        self.db.cursor.execute(
            "UPDATE books SET is_available = ? WHERE book_id = ?",
            (1 if available else 0, book_id)
        )
        self.db.commit()


class Member:
    """Represents a library member and their database operations."""

    def __init__(self, db: Database):
        self.db = db

    def add_member(self, name):
        self.db.cursor.execute(
            "INSERT INTO members (name, books_issued) VALUES (?, 0)", (name,)
        )
        self.db.commit()
        print(f"Member '{name}' registered successfully.")

    def list_members(self):
        self.db.cursor.execute("SELECT member_id, name, books_issued FROM members")
        rows = self.db.cursor.fetchall()
        print("\n--- All Members ---")
        for row in rows:
            print(f"ID: {row[0]} | {row[1]} | Books currently issued: {row[2]}")

    def get_books_issued(self, member_id):
        self.db.cursor.execute("SELECT books_issued FROM members WHERE member_id = ?", (member_id,))
        result = self.db.cursor.fetchone()
        return result[0] if result else None

    def change_issued_count(self, member_id, delta):
        self.db.cursor.execute(
            "UPDATE members SET books_issued = books_issued + ? WHERE member_id = ?",
            (delta, member_id)
        )
        self.db.commit()


class Transaction:
    """Handles issuing and returning books, including fine calculation."""

    def __init__(self, db: Database, book: Book, member: Member):
        self.db = db
        self.book = book
        self.member = member

    def issue_book(self, book_id, member_id):
        if not self.book.is_available(book_id):
            print("This book is not available right now.")
            return

        issued_count = self.member.get_books_issued(member_id)
        if issued_count is None:
            print("Member not found.")
            return
        if issued_count >= MAX_BOOKS_PER_MEMBER:
            print(f"Member has already reached the borrowing limit of {MAX_BOOKS_PER_MEMBER} books.")
            return

        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=LOAN_PERIOD_DAYS)

        self.db.cursor.execute(
            """INSERT INTO transactions (book_id, member_id, issue_date, due_date, return_date)
               VALUES (?, ?, ?, ?, NULL)""",
            (book_id, member_id, issue_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"))
        )
        self.db.commit()

        self.book.set_availability(book_id, False)
        self.member.change_issued_count(member_id, 1)

        print(f"Book issued. Due date: {due_date.strftime('%Y-%m-%d')}")

    def return_book(self, book_id, member_id):
        self.db.cursor.execute(
            """SELECT transaction_id, due_date FROM transactions
               WHERE book_id = ? AND member_id = ? AND return_date IS NULL""",
            (book_id, member_id)
        )
        result = self.db.cursor.fetchone()

        if result is None:
            print("No active transaction found for this book and member.")
            return

        transaction_id, due_date_str = result
        return_date = datetime.now()
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

        fine = 0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * FINE_PER_DAY

        self.db.cursor.execute(
            "UPDATE transactions SET return_date = ? WHERE transaction_id = ?",
            (return_date.strftime("%Y-%m-%d"), transaction_id)
        )
        self.db.commit()

        self.book.set_availability(book_id, True)
        self.member.change_issued_count(member_id, -1)

        if fine > 0:
            print(f"Book returned late. Fine: Rs.{fine}")
        else:
            print("Book returned on time. No fine.")


def print_menu():
    print("""
========== Library Management System ==========
1. Add Book
2. Add Member
3. List Books
4. List Members
5. Issue Book
6. Return Book
7. Exit
=================================================
""")


def main():
    db = Database()
    book = Book(db)
    member = Member(db)
    transaction = Transaction(db, book, member)

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Book title: ").strip()
            author = input("Author: ").strip()
            book.add_book(title, author)

        elif choice == "2":
            name = input("Member name: ").strip()
            member.add_member(name)

        elif choice == "3":
            book.list_books()

        elif choice == "4":
            member.list_members()

        elif choice == "5":
            book_id = input("Book ID to issue: ").strip()
            member_id = input("Member ID: ").strip()
            if book_id.isdigit() and member_id.isdigit():
                transaction.issue_book(int(book_id), int(member_id))
            else:
                print("Invalid ID entered.")

        elif choice == "6":
            book_id = input("Book ID to return: ").strip()
            member_id = input("Member ID: ").strip()
            if book_id.isdigit() and member_id.isdigit():
                transaction.return_book(int(book_id), int(member_id))
            else:
                print("Invalid ID entered.")

        elif choice == "7":
            print("Exiting. Goodbye!")
            db.close()
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
