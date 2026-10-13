# Python Programming — Fundamentals

## 1. Introduction to Python

Python is a high-level, interpreted, general-purpose programming language known for its simple syntax and readability. It is widely used in software development, data science, artificial intelligence, machine learning, automation, web development, and scripting.

Python programs are generally easy to write and understand because the language uses indentation to define blocks of code.

### Example

```python
name = "Sakshi"
print("Hello", name)
```

Output:

```text
Hello Sakshi
```

---

## 2. Features of Python

Important features of Python include:

- Simple and easy-to-read syntax
- High-level programming language
- Interpreted language
- Dynamically typed
- Object-oriented programming support
- Large standard library
- Cross-platform support
- Open-source
- Supports functional and procedural programming
- Large ecosystem of third-party libraries

Python is particularly popular in AI, machine learning, data science, and automation because of libraries such as NumPy, Pandas, Matplotlib, and scikit-learn.

---

## 3. Variables

A variable is a name used to store a value.

Python does not require explicit declaration of the variable type.

```python
age = 21
name = "Sakshi"
percentage = 87.7
```

Python determines the type automatically.

```python
x = 10
print(type(x))
```

Output:

```text
<class 'int'>
```

---

## 4. Python Data Types

Common built-in data types include:

### Integer

Used for whole numbers.

```python
age = 21
```

### Float

Used for decimal numbers.

```python
price = 99.50
```

### String

Used for text.

```python
name = "EduAssist"
```

### Boolean

Represents either `True` or `False`.

```python
is_student = True
```

### List

An ordered and mutable collection.

```python
subjects = ["Python", "DBMS", "Cloud"]
```

### Tuple

An ordered and immutable collection.

```python
coordinates = (10, 20)
```

### Set

An unordered collection of unique elements.

```python
numbers = {1, 2, 3, 4}
```

### Dictionary

Stores data as key-value pairs.

```python
student = {
    "name": "Sakshi",
    "score": 87
}
```

---

## 5. Operators

Python provides several types of operators.

### Arithmetic Operators

```text
+    Addition
-    Subtraction
*    Multiplication
/    Division
%    Modulus
//   Floor division
**   Exponentiation
```

Example:

```python
a = 10
b = 3

print(a + b)
print(a % b)
print(a ** b)
```

### Comparison Operators

```text
==   Equal
!=   Not equal
>    Greater than
<    Less than
>=   Greater than or equal
<=   Less than or equal
```

### Logical Operators

```text
and
or
not
```

Example:

```python
age = 20

if age >= 18 and age <= 60:
    print("Eligible")
```

---

## 6. Conditional Statements

Conditional statements allow a program to make decisions.

### if

```python
marks = 80

if marks >= 40:
    print("Pass")
```

### if-else

```python
marks = 35

if marks >= 40:
    print("Pass")
else:
    print("Fail")
```

### if-elif-else

```python
marks = 85

if marks >= 90:
    grade = "A+"
elif marks >= 75:
    grade = "A"
elif marks >= 60:
    grade = "B"
else:
    grade = "C"

print(grade)
```

---

## 7. Loops

Loops are used to execute a block of code repeatedly.

### for Loop

```python
for i in range(5):
    print(i)
```

Output:

```text
0
1
2
3
4
```

### while Loop

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

### break

Terminates the loop.

```python
for i in range(10):
    if i == 5:
        break
    print(i)
```

### continue

Skips the current iteration.

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
```

---

## 8. Functions

A function is a reusable block of code designed to perform a specific task.

### Defining a Function

```python
def greet(name):
    return "Hello " + name

message = greet("Sakshi")
print(message)
```

### Function with Multiple Parameters

```python
def add(a, b):
    return a + b

result = add(10, 20)
print(result)
```

### Default Arguments

```python
def greet(name="Student"):
    print("Hello", name)

greet()
greet("Sakshi")
```

Functions improve code:

- Reusability
- Readability
- Maintainability
- Modularity

---

## 9. Lists

A list is an ordered and mutable collection.

```python
subjects = [
    "Python",
    "DBMS",
    "Cloud Computing"
]
```

### Common List Operations

```python
subjects.append("Machine Learning")
subjects.remove("DBMS")

print(subjects)
```

Accessing an element:

```python
print(subjects[0])
```

List slicing:

```python
print(subjects[0:2])
```

---

## 10. Tuples

A tuple is an ordered but immutable collection.

```python
student = ("Sakshi", 21, 87.7)
```

Accessing values:

```python
print(student[0])
```

Because tuples are immutable, their elements cannot be changed after creation.

---

## 11. Sets

A set stores unique values.

```python
numbers = {1, 2, 3, 3, 4}

print(numbers)
```

The duplicate value is automatically removed.

Sets are useful for:

- Removing duplicates
- Membership testing
- Mathematical set operations

Example:

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a.union(b))
print(a.intersection(b))
```

---

## 12. Dictionaries

A dictionary stores information using key-value pairs.

```python
student = {
    "name": "Sakshi",
    "age": 21,
    "score": 87
}
```

Accessing a value:

```python
print(student["name"])
```

Adding a new value:

```python
student["course"] = "B.Tech"
```

Dictionaries are commonly used when structured information needs to be represented.

---

## 13. Exception Handling

Exception handling allows a program to handle runtime errors without unexpectedly terminating.

Python provides:

```text
try
except
else
finally
```

Example:

```python
try:
    a = 10
    b = 0
    result = a / b
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### finally

The `finally` block executes whether an exception occurs or not.

```python
try:
    print("Processing")
except Exception:
    print("Error")
finally:
    print("Execution completed")
```

---

## 14. Object-Oriented Programming

Object-Oriented Programming (OOP) is a programming approach based on classes and objects.

Important OOP concepts include:

- Class
- Object
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction

### Class and Object

```python
class Student:

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def display(self):
        print(self.name, self.score)


student1 = Student("Sakshi", 87)

student1.display()
```

Here:

- `Student` is a class.
- `student1` is an object.
- `__init__()` is the constructor.
- `self` refers to the current object.

---

## 15. Inheritance

Inheritance allows one class to acquire properties and methods from another class.

```python
class Person:

    def display(self):
        print("This is a person")


class Student(Person):

    def study(self):
        print("Student is studying")


s = Student()

s.display()
s.study()
```

`Student` inherits the `display()` method from `Person`.

---

## 16. Modules

A module is a Python file containing reusable code.

Example:

```python
import math

print(math.sqrt(25))
```

Python provides many built-in modules such as:

- `math`
- `os`
- `sys`
- `datetime`
- `random`

---

## 17. Packages

A package is a collection of related Python modules organized in a directory.

Popular external Python packages include:

- NumPy
- Pandas
- Matplotlib
- scikit-learn
- Requests
- FastAPI
- Streamlit

---

## 18. Python for Data Science and AI

Python is widely used in data science and artificial intelligence.

### NumPy

Used for numerical computing and arrays.

```python
import numpy as np

numbers = np.array([1, 2, 3, 4])
print(numbers.mean())
```

### Pandas

Used for data manipulation and analysis.

```python
import pandas as pd

data = {
    "Name": ["A", "B"],
    "Score": [80, 90]
}

df = pd.DataFrame(data)

print(df)
```

### Matplotlib

Used for data visualization.

```python
import matplotlib.pyplot as plt

x = [1, 2, 3]
y = [10, 20, 30]

plt.plot(x, y)
plt.show()
```

### Scikit-learn

Used for machine learning tasks such as:

- Classification
- Regression
- Clustering
- Model evaluation
- Data preprocessing

---

## 19. Advantages of Python

- Easy to learn
- Simple syntax
- Large community
- Extensive libraries
- Cross-platform
- Suitable for rapid development
- Strong support for AI and data science
- Useful for automation and scripting

---

## 20. Limitations of Python

- Generally slower than compiled languages such as C or C++
- Higher memory consumption in some workloads
- Not always ideal for low-level system programming
- Dynamic typing can allow certain errors to appear only at runtime

---

# Important Exam Questions

### Basic Questions

1. What is Python?
2. Explain the features of Python.
3. What are Python's built-in data types?
4. What is the difference between a list and a tuple?
5. What is a dictionary?
6. What is a set?
7. Explain conditional statements.
8. Explain `for` and `while` loops.
9. What is a function?
10. What is exception handling?

### OOP Questions

1. What is OOP?
2. What is a class?
3. What is an object?
4. Explain inheritance.
5. Explain encapsulation.
6. What is polymorphism?
7. What is abstraction?
8. What is the purpose of `self`?
9. What is the purpose of `__init__()`?

### Interview Questions

1. What is the difference between interpreted and compiled languages?
2. What is dynamic typing?
3. What is the difference between `==` and `is`?
4. What is the difference between mutable and immutable objects?
5. What are `*args` and `**kwargs`?
6. What is a lambda function?
7. What are list comprehensions?
8. What is the difference between shallow copy and deep copy?
9. What are modules and packages?
10. Why is Python widely used in AI and data science?

---

# Quick Revision

```text
Python
│
├── Variables
├── Data Types
│   ├── int
│   ├── float
│   ├── str
│   ├── bool
│   ├── list
│   ├── tuple
│   ├── set
│   └── dictionary
│
├── Operators
├── Conditions
├── Loops
├── Functions
├── Exception Handling
├── OOP
│   ├── Class
│   ├── Object
│   ├── Inheritance
│   ├── Encapsulation
│   ├── Polymorphism
│   └── Abstraction
│
├── Modules
├── Packages
└── AI/Data Science Libraries
    ├── NumPy
    ├── Pandas
    ├── Matplotlib
    └── Scikit-learn
```