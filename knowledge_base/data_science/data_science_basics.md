# Data Science — Fundamentals

## 1. Introduction

Data Science is an interdisciplinary field that uses statistics, programming, machine learning, and domain knowledge to extract useful information and insights from data.

A typical data science workflow is:

```text
Problem Definition
       ↓
Data Collection
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Feature Engineering
       ↓
Modeling
       ↓
Evaluation
       ↓
Visualization
       ↓
Decision Making
```

## 2. Types of Data

### Structured Data

Data organized in rows and columns.

Example:

- Database tables
- CSV files

### Unstructured Data

Data without a fixed tabular structure.

Examples:

- Images
- Videos
- Audio
- Text documents

### Semi-structured Data

Data that contains organizational information but does not follow a strict table format.

Example:

- JSON
- XML

## 3. Data Collection

Data can be collected from:

- Databases
- APIs
- Sensors
- Surveys
- Websites
- Applications
- Public datasets

## 4. Data Cleaning

Data cleaning improves data quality.

Common operations:

- Handling missing values
- Removing duplicates
- Correcting data types
- Detecting outliers
- Standardizing values

## 5. Exploratory Data Analysis

EDA is used to understand the structure and patterns in a dataset.

Common techniques:

- Summary statistics
- Histograms
- Box plots
- Scatter plots
- Correlation analysis
- Grouping and aggregation

## 6. Statistics

Important statistical concepts include:

### Mean

Average value of observations.

### Median

Middle value after sorting observations.

### Mode

Most frequently occurring value.

### Standard Deviation

Measures the spread of values around the mean.

### Correlation

Measures the relationship between variables.

## 7. NumPy

NumPy is a Python library for numerical computing.

It provides:

- Arrays
- Mathematical operations
- Linear algebra
- Statistical functions

## 8. Pandas

Pandas is a Python library for data manipulation and analysis.

Important structures:

- Series
- DataFrame

Common operations:

```python
df.head()
df.info()
df.describe()
df.dropna()
df.fillna()
df.groupby()
```

## 9. Data Visualization

Visualization helps communicate patterns in data.

Popular libraries:

- Matplotlib
- Seaborn
- Plotly

Common charts:

- Bar chart
- Line chart
- Histogram
- Scatter plot
- Box plot
- Heatmap

## 10. Feature Engineering

Feature engineering creates or transforms input variables to improve machine learning models.

Examples:

- Extracting month from date
- Creating total score
- Normalizing values
- Creating interaction features

## 11. Machine Learning in Data Science

Machine learning can be used for:

- Prediction
- Classification
- Clustering
- Recommendation
- Anomaly detection

## 12. Data Pipeline

A data pipeline automates movement and processing of data.

```text
Source
 ↓
Ingestion
 ↓
Cleaning
 ↓
Transformation
 ↓
Storage
 ↓
Analysis
 ↓
Model / Dashboard
```

## 13. Data Ethics

Important principles include:

- Privacy
- Security
- Fairness
- Transparency
- Responsible data usage

Sensitive information should be protected and used only when necessary.

## 14. Common Applications

Data science is used in:

- Healthcare
- Finance
- Education
- Agriculture
- Retail
- Cyber security
- Manufacturing
- Transportation

## 15. Data Science vs Data Analytics

### Data Science

Broader field involving:

- Data processing
- Statistics
- Machine learning
- Prediction
- Advanced analytics

### Data Analytics

Focuses more on examining existing data to understand trends and support decisions.

## 16. Important Questions

1. What is data science?
2. Explain structured and unstructured data.
3. What is data cleaning?
4. What is EDA?
5. Explain mean, median and mode.
6. What is standard deviation?
7. What is correlation?
8. What is Pandas?
9. What is NumPy?
10. What is feature engineering?
11. What is data visualization?
12. Explain a data science pipeline.
13. What are data ethics?

## Quick Revision

```text
Data Science
├── Data Collection
├── Data Cleaning
├── EDA
├── Statistics
├── Visualization
├── Feature Engineering
├── Machine Learning
├── Data Pipelines
├── Data Ethics
└── Decision Making
```