# Database Management Systems (DBMS) — Fundamentals

## 1. Introduction to DBMS

A Database Management System (DBMS) is software used to create, store, organize, retrieve, update, and manage data in a database.

A database is an organized collection of related data.

Examples of DBMS software include:

- MySQL
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- MongoDB

A DBMS provides an interface between users/applications and the database.

### Basic DBMS Architecture

```text
User / Application
        ↓
       DBMS
        ↓
    Database
```

---

## 2. Why DBMS is Needed

Traditional file systems can create problems such as:

- Data redundancy
- Data inconsistency
- Difficult data sharing
- Limited security
- Difficult backup and recovery
- Problems with concurrent access

A DBMS addresses many of these problems by providing structured data management.

---

## 3. Advantages of DBMS

Important advantages include:

- Reduced data redundancy
- Improved data consistency
- Data security
- Data sharing
- Data integrity
- Backup and recovery
- Concurrent access
- Centralized data management
- Controlled access to data

---

## 4. Database Models

A database model describes how data is organized.

Common models include:

### Hierarchical Model

Data is organized in a tree-like structure.

```text
        Root
       /    \
    Child  Child
     /
  Child
```

### Network Model

Data is represented using relationships that can form a network.

### Relational Model

Data is stored in tables consisting of rows and columns.

Example:

| Student_ID | Name | Score |
|---|---|---:|
| 101 | A | 85 |
| 102 | B | 90 |

The relational model is widely used in traditional database systems.

### NoSQL Model

NoSQL databases use models such as:

- Document
- Key-value
- Column-family
- Graph

MongoDB is an example of a document-oriented NoSQL database.

---

# 5. Relational Database

A relational database stores data in tables.

A table consists of:

- Rows
- Columns

Example:

```text
STUDENT
--------------------------------
ID     NAME       DEPARTMENT
--------------------------------
101    Sakshi     ECE
102    Rahul      CSE
103    Priya      AIML
```

A row represents a record.

A column represents an attribute.

---

# 6. Keys in DBMS

Keys are used to identify records and establish relationships between tables.

## Primary Key

A primary key uniquely identifies each record in a table.

Example:

```sql id="u0n0by"
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(50)
);
```

Each `student_id` must be unique and cannot normally be NULL.

---

## Foreign Key

A foreign key is a field that refers to a key in another table.

Example:

```sql id="h25t6w"
CREATE TABLE Department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_id INT,
    FOREIGN KEY (dept_id)
        REFERENCES Department(dept_id)
);
```

The foreign key establishes a relationship between the tables.

---

## Candidate Key

A candidate key is an attribute or combination of attributes that can uniquely identify a record.

A table can have multiple candidate keys, but one is selected as the primary key.

---

## Super Key

A super key is any set of attributes that can uniquely identify a record.

Every candidate key is a super key, but not every super key is a candidate key.

---

## Composite Key

A composite key consists of two or more attributes used together to uniquely identify a record.

Example:

```text
Student_ID + Course_ID
```

---

# 7. Constraints

Constraints are rules applied to table columns to maintain data integrity.

Common constraints include:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- NOT NULL
- CHECK
- DEFAULT

Example:

```sql id="d1aqhx"
CREATE TABLE Student (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT CHECK(age >= 18),
    city VARCHAR(50) DEFAULT 'Pune'
);
```

---

# 8. SQL

SQL stands for Structured Query Language.

It is used to communicate with relational databases.

SQL can be used to:

- Create databases and tables
- Insert data
- Retrieve data
- Update data
- Delete data
- Control access
- Manage transactions

---

# 9. SQL Command Categories

SQL commands are commonly divided into several categories.

## DDL — Data Definition Language

DDL is used to define database structures.

Commands:

```text
CREATE
ALTER
DROP
TRUNCATE
```

Example:

```sql id="j5emiy"
CREATE TABLE Student (
    id INT,
    name VARCHAR(50)
);
```

---

## DML — Data Manipulation Language

DML is used to modify data.

Commands include:

```text
INSERT
UPDATE
DELETE
```

Example:

```sql id="e0zv70"
INSERT INTO Student
VALUES (101, 'Sakshi');
```

---

## DQL — Data Query Language

DQL is primarily used to retrieve data.

The main command is:

```text
SELECT
```

Example:

```sql id="0txx5e"
SELECT * FROM Student;
```

---

## DCL — Data Control Language

DCL manages access permissions.

Commands include:

```text
GRANT
REVOKE
```

---

## TCL — Transaction Control Language

TCL manages database transactions.

Commands include:

```text
COMMIT
ROLLBACK
SAVEPOINT
```

---

# 10. SELECT Statement

The `SELECT` statement retrieves data.

```sql id="2qpru9"
SELECT name, score
FROM Student;
```

To retrieve all columns:

```sql id="19r3bh"
SELECT *
FROM Student;
```

---

# 11. WHERE Clause

`WHERE` filters records based on a condition.

```sql id="v4e0ij"
SELECT *
FROM Student
WHERE score > 80;
```

---

# 12. ORDER BY

`ORDER BY` sorts query results.

Ascending:

```sql id="k6jz4b"
SELECT *
FROM Student
ORDER BY score ASC;
```

Descending:

```sql id="txbr2f"
SELECT *
FROM Student
ORDER BY score DESC;
```

---

# 13. GROUP BY

`GROUP BY` groups rows with the same values.

Example:

```sql id="w1c6cb"
SELECT department, COUNT(*)
FROM Student
GROUP BY department;
```

It is commonly used with aggregate functions.

---

# 14. HAVING

`HAVING` filters groups created using `GROUP BY`.

Example:

```sql id="gq8z1a"
SELECT department, AVG(score)
FROM Student
GROUP BY department
HAVING AVG(score) > 75;
```

### WHERE vs HAVING

`WHERE` filters individual rows before grouping.

`HAVING` filters groups after grouping.

---

# 15. Aggregate Functions

Aggregate functions perform calculations on multiple rows.

Common aggregate functions:

```text
COUNT()
SUM()
AVG()
MIN()
MAX()
```

Example:

```sql id="f1q70f"
SELECT AVG(score)
FROM Student;
```

---

# 16. SQL Joins

Joins combine data from multiple tables.

Suppose we have:

```text
Student
----------------------
student_id
name
dept_id
```

and:

```text
Department
----------------------
dept_id
dept_name
```

## INNER JOIN

Returns matching records from both tables.

```sql id="7c9p0s"
SELECT s.name, d.dept_name
FROM Student s
INNER JOIN Department d
ON s.dept_id = d.dept_id;
```

---

## LEFT JOIN

Returns all records from the left table and matching records from the right table.

```sql id="t5t6c1"
SELECT s.name, d.dept_name
FROM Student s
LEFT JOIN Department d
ON s.dept_id = d.dept_id;
```

---

## RIGHT JOIN

Returns all records from the right table and matching records from the left table.

---

## FULL OUTER JOIN

Returns matching and non-matching records from both tables.

Note: Support for `FULL OUTER JOIN` varies between database systems.

---

# 17. Normalization

Normalization is the process of organizing data to reduce redundancy and improve data integrity.

Important normal forms include:

### First Normal Form — 1NF

A table is in 1NF when:

- Values are atomic.
- There are no repeating groups.
- Each field contains a single value.

### Second Normal Form — 2NF

A table is in 2NF when:

- It is already in 1NF.
- There is no partial dependency on a part of a composite key.

### Third Normal Form — 3NF

A table is in 3NF when:

- It is already in 2NF.
- There is no transitive dependency of non-key attributes on the primary key.

Normalization helps reduce data redundancy and update anomalies.

---

# 18. Denormalization

Denormalization intentionally introduces some redundancy to improve read performance or simplify queries.

It may be useful in systems where read performance is more important than minimizing redundancy.

---

# 19. Transactions

A transaction is a sequence of database operations treated as a single logical unit of work.

Example:

```text
Transfer ₹1000
      ↓
Debit Account A
      ↓
Credit Account B
```

Both operations should succeed together.

---

# 20. ACID Properties

Database transactions commonly follow ACID properties.

## Atomicity

A transaction is treated as an all-or-nothing operation.

## Consistency

A transaction should move the database from one valid state to another valid state.

## Isolation

Concurrent transactions should not incorrectly interfere with each other.

## Durability

Once a transaction is committed, its changes should persist even after system failures.

### Quick Memory Trick

```text
A → All or Nothing
C → Correct / Consistent State
I → Independent Transactions
D → Data Persists
```

---

# 21. Indexing

An index is a data structure that can improve the speed of data retrieval.

Example:

```sql id="4xv1ph"
CREATE INDEX idx_student_name
ON Student(name);
```

Indexes can improve read performance but may:

- Require additional storage
- Increase insert/update/delete overhead

Therefore, indexes should be used appropriately.

---

# 22. Views

A view is a virtual table based on a SQL query.

Example:

```sql id="t7yk9j"
CREATE VIEW high_scorers AS
SELECT name, score
FROM Student
WHERE score >= 80;
```

A view can simplify complex queries and restrict access to selected data.

---

# 23. Stored Procedures

A stored procedure is a set of SQL statements stored in the database and executed when required.

Stored procedures can help:

- Reuse database logic
- Centralize operations
- Reduce repeated SQL code
- Control access to database operations

Syntax varies between database systems.

---

# 24. Triggers

A trigger is a database operation that automatically executes when a specified event occurs.

Typical events include:

- INSERT
- UPDATE
- DELETE

Example use case:

```text
Student record updated
        ↓
Trigger executes
        ↓
Change recorded in audit table
```

---

# 25. Relational Database vs NoSQL

| Feature | Relational Database | NoSQL Database |
|---|---|---|
| Data model | Tables | Document/key-value/graph/etc. |
| Schema | Usually structured | Often flexible |
| Query | SQL commonly used | Database-specific APIs/query languages |
| Relationships | Strong support | Depends on database |
| Scaling | Often strong vertical scaling; horizontal scaling also possible | Often designed with horizontal scaling in mind |
| Examples | MySQL, PostgreSQL | MongoDB, Redis |

The choice depends on application requirements.

---

# 26. MySQL

MySQL is a popular relational database management system.

It uses SQL to create and manage relational databases.

Example:

```sql id="5kt9i4"
CREATE DATABASE college;

USE college;

CREATE TABLE Student (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    score DECIMAL(5,2)
);
```

Insert data:

```sql id="x1c9nd"
INSERT INTO Student
VALUES (1, 'Sakshi', 87.50);
```

Retrieve data:

```sql id="z6e5l0"
SELECT *
FROM Student;
```

---

# 27. DBMS Security

Database security protects data from unauthorized access and misuse.

Important techniques include:

- Authentication
- Authorization
- Access control
- Encryption
- Backup
- Auditing
- Secure query practices

Parameterized queries should be used to reduce the risk of SQL injection.

---

# 28. SQL Injection

SQL injection is a security vulnerability where malicious input can manipulate a SQL query.

Unsafe application code can allow user input to become part of a SQL statement.

A safer approach is to use parameterized queries or prepared statements.

Conceptually:

```text
User Input
    ↓
Parameterized Query
    ↓
Database
```

rather than directly concatenating untrusted input into SQL strings.

---

# 29. DBMS vs File System

| Feature | File System | DBMS |
|---|---|---|
| Data organization | Files | Structured database |
| Redundancy control | Limited | Better |
| Security | Basic | Advanced |
| Relationships | Difficult | Supported |
| Concurrent access | Limited | Supported |
| Backup/recovery | Usually manual or application-dependent | Built-in mechanisms available |
| Querying | Limited | Powerful query languages |

---

# 30. Important Exam Questions

### Basic Questions

1. What is DBMS?
2. What is a database?
3. Why is DBMS required?
4. Explain advantages of DBMS.
5. What is a relational database?
6. What is a primary key?
7. What is a foreign key?
8. What is a candidate key?
9. What is a composite key?
10. What are database constraints?

### SQL Questions

1. What is SQL?
2. Explain DDL, DML, DQL, DCL and TCL.
3. What is the difference between WHERE and HAVING?
4. Explain GROUP BY.
5. Explain aggregate functions.
6. What are SQL joins?
7. Explain INNER JOIN and LEFT JOIN.
8. What is a subquery?
9. What is a view?
10. What is an index?

### Advanced Questions

1. What is normalization?
2. Explain 1NF, 2NF and 3NF.
3. What is denormalization?
4. Explain ACID properties.
5. What is a transaction?
6. What is concurrency control?
7. What is database indexing?
8. What is a stored procedure?
9. What is a trigger?
10. What is SQL injection?

### Interview Questions

1. Difference between primary key and foreign key.
2. Difference between DELETE, DROP and TRUNCATE.
3. Difference between WHERE and HAVING.
4. Difference between UNION and UNION ALL.
5. Difference between INNER JOIN and LEFT JOIN.
6. What is normalization and why is it required?
7. What are ACID properties?
8. What is an index and what are its disadvantages?
9. What is a transaction?
10. How can SQL injection be prevented?

---

# Quick Revision

```text
DBMS
│
├── Database
├── Tables
│   ├── Rows
│   └── Columns
│
├── Keys
│   ├── Primary Key
│   ├── Foreign Key
│   ├── Candidate Key
│   ├── Super Key
│   └── Composite Key
│
├── SQL
│   ├── DDL
│   ├── DML
│   ├── DQL
│   ├── DCL
│   └── TCL
│
├── Queries
│   ├── SELECT
│   ├── WHERE
│   ├── GROUP BY
│   ├── HAVING
│   └── ORDER BY
│
├── Joins
├── Normalization
├── Transactions
├── ACID
├── Indexing
├── Views
├── Stored Procedures
├── Triggers
└── Database Security
```