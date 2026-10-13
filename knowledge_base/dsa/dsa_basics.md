# Data Structures and Algorithms — Fundamentals

## 1. Introduction

Data Structures and Algorithms (DSA) is the study of organizing data efficiently and designing procedures to solve computational problems.

A data structure determines how data is stored and accessed.

An algorithm defines the steps required to solve a problem.

## 2. Types of Data Structures

Data structures can broadly be divided into:

### Linear Data Structures

Elements are arranged sequentially.

Examples:

- Array
- Linked List
- Stack
- Queue

### Non-Linear Data Structures

Elements are organized hierarchically or as networks.

Examples:

- Tree
- Graph
- Heap

## 3. Array

An array stores elements in contiguous memory locations in many programming languages.

Advantages:

- Fast indexed access
- Simple structure

Limitations:

- Insertion/deletion can be expensive
- Fixed-size arrays have limited flexibility

## 4. Linked List

A linked list consists of nodes connected using references.

Types:

- Singly linked list
- Doubly linked list
- Circular linked list

Advantages:

- Dynamic size
- Efficient insertion/deletion at known positions

Limitations:

- Extra memory for links
- No direct random access

## 5. Stack

A stack follows:

**LIFO — Last In, First Out**

Operations:

- Push
- Pop
- Peek

Applications:

- Function calls
- Undo operations
- Expression evaluation
- Backtracking

## 6. Queue

A queue follows:

**FIFO — First In, First Out**

Operations:

- Enqueue
- Dequeue
- Front

Applications:

- Scheduling
- Buffering
- Breadth-first search

## 7. Hash Table

A hash table stores key-value pairs using a hash function.

Advantages:

- Fast average lookup
- Efficient insertion and deletion

Applications:

- Dictionaries
- Caches
- Symbol tables

## 8. Tree

A tree is a hierarchical data structure.

Common types:

- Binary Tree
- Binary Search Tree
- AVL Tree
- Heap
- Trie

## 9. Binary Search Tree

In a Binary Search Tree:

- Left subtree contains smaller values
- Right subtree contains larger values

Average search performance can be efficient when the tree is balanced.

## 10. Heap

A heap is a specialized tree-based structure.

Types:

- Min Heap
- Max Heap

Applications:

- Priority queues
- Scheduling
- Heap sort

## 11. Graph

A graph consists of vertices and edges.

Types:

- Directed graph
- Undirected graph
- Weighted graph
- Unweighted graph

Applications:

- Social networks
- Maps
- Computer networks
- Recommendation systems

## 12. Searching Algorithms

### Linear Search

Checks elements sequentially.

Time complexity:

```text
O(n)
```

### Binary Search

Works on sorted data by repeatedly dividing the search space.

Time complexity:

```text
O(log n)
```

## 13. Sorting Algorithms

Common sorting algorithms include:

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort

### Bubble Sort

Repeatedly compares adjacent elements.

Typical time complexity:

```text
O(n²)
```

### Merge Sort

Uses divide and conquer.

Time complexity:

```text
O(n log n)
```

### Quick Sort

Uses a pivot to partition data.

Average time complexity:

```text
O(n log n)
```

Worst-case complexity:

```text
O(n²)
```

## 14. Recursion

Recursion occurs when a function calls itself to solve smaller versions of a problem.

A recursive algorithm requires a base condition to terminate.

Applications:

- Tree traversal
- Divide and conquer
- Backtracking

## 15. Tree Traversal

Common traversal methods:

### Inorder

```text
Left → Root → Right
```

### Preorder

```text
Root → Left → Right
```

### Postorder

```text
Left → Right → Root
```

## 16. Graph Traversal

### BFS

Breadth-First Search explores nodes level by level.

It commonly uses a queue.

### DFS

Depth-First Search explores as deeply as possible before backtracking.

It can use recursion or a stack.

## 17. Algorithmic Complexity

Big-O notation describes how algorithm resource requirements grow with input size.

Common complexities:

```text
O(1)        Constant
O(log n)    Logarithmic
O(n)        Linear
O(n log n)  Linearithmic
O(n²)       Quadratic
O(2ⁿ)       Exponential
```

## 18. Dynamic Programming

Dynamic Programming solves problems by breaking them into overlapping subproblems and storing previously computed results.

Common techniques:

- Memoization
- Tabulation

## 19. Greedy Algorithms

Greedy algorithms make the locally best choice at each step.

They work correctly for problems where the greedy-choice property applies.

Examples:

- Activity selection
- Fractional knapsack
- Some scheduling problems

## 20. Divide and Conquer

Divide and conquer breaks a problem into smaller subproblems, solves them, and combines their results.

Examples:

- Merge Sort
- Quick Sort
- Binary Search

## 21. Important Questions

1. What is a data structure?
2. What is an algorithm?
3. Compare array and linked list.
4. Explain stack and queue.
5. What is a hash table?
6. Explain Binary Search Tree.
7. What is a heap?
8. What is a graph?
9. Explain BFS and DFS.
10. Explain linear and binary search.
11. Compare sorting algorithms.
12. What is recursion?
13. What is Big-O notation?
14. Explain dynamic programming.
15. What is a greedy algorithm?
16. Explain divide and conquer.

## Quick Revision

```text
DSA
├── Linear Structures
│   ├── Array
│   ├── Linked List
│   ├── Stack
│   └── Queue
├── Non-Linear Structures
│   ├── Tree
│   ├── Heap
│   └── Graph
├── Searching
│   ├── Linear Search
│   └── Binary Search
├── Sorting
├── Recursion
├── BFS / DFS
├── Dynamic Programming
├── Greedy
├── Divide and Conquer
└── Complexity Analysis
```