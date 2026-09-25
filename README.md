# Library Management System

A console-based **Library Management System** developed using **Python, Object-Oriented Programming (OOP), and SQLite**. The project is designed to manage books, library members, book issue/return transactions, due dates, borrowing limits, and overdue fines through a simple command-line interface.

## Features

* Add, update, delete, and search books
* Register and manage library members
* Issue books to members
* Return issued books
* Track borrowing transactions
* Track book due dates
* Calculate overdue fines
* Apply borrowing limits
* Check book availability
* Search library records
* Generate basic library reports
* Store data persistently using SQLite
* Input validation and exception handling
* Console-based menu-driven interface

## Technologies Used

* **Python**
* **SQLite**
* **Object-Oriented Programming (OOP)**

## Project Structure

```text
library-management-system/
│
├── library_management_system.py
├── README.md
└── .gitignore
```

## Main Components

### Book

Manages book-related information such as book details, availability, and search operations.

### Member

Manages library member information and borrowing-related records.

### Transaction

Handles book issue and return operations, transaction records, due dates, and overdue fine calculations.

## Database

The application uses **SQLite** for persistent data storage.

The database is used to maintain records related to:

* Books
* Members
* Transactions
* Issue and return details
* Due dates
* Overdue fines

## How the System Works

The system provides a menu-driven console interface where users can perform different library operations.

Typical operations include:

```text
1. Add Book
2. Update Book
3. Delete Book
4. Search Book
5. Add Member
6. Issue Book
7. Return Book
8. View Transactions
9. Generate Reports
10. Exit
```

The available menu options may vary depending on the implementation of the Python program.

## How to Run

Make sure Python is installed on your system.

Run the following command from the project directory:

```bash
python library_management_system.py
```

The application will start in the terminal and display the available library management options.

## OOP Concepts Used

This project demonstrates important Object-Oriented Programming concepts, including:

* Classes and Objects
* Encapsulation
* Abstraction
* Methods and Constructors
* Object interaction
* Exception Handling

## Database Concepts

The project also demonstrates:

* SQLite database connectivity
* Creating database tables
* Inserting records
* Updating records
* Deleting records
* Retrieving records
* Persistent data storage
* CRUD operations

## Input Validation

The application validates user inputs to help prevent invalid operations such as:

* Invalid book information
* Invalid member information
* Invalid borrowing quantities
* Issuing unavailable books
* Returning books that were not issued

## Future Improvements

Possible future enhancements include:

* Graphical User Interface (GUI)
* Admin and librarian authentication
* Member login system
* Email notifications for due dates
* Advanced search and filtering
* Detailed analytics dashboard
* PDF report generation
* Web-based version

## Author

**Nirmal Singh**

B.Tech Computer Science & Engineering
