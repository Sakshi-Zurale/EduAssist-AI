# Machine Learning — Fundamentals

## 1. Introduction

Machine Learning (ML) is a branch of artificial intelligence that enables computers to learn patterns from data and make predictions or decisions without being explicitly programmed for every case.

A typical ML system involves:

```text
Data
 ↓
Preprocessing
 ↓
Feature Engineering
 ↓
Model Training
 ↓
Evaluation
 ↓
Prediction
```

## 2. Types of Machine Learning

### Supervised Learning

The model learns from labelled data.

Examples:

- Classification
- Regression

### Unsupervised Learning

The model discovers patterns in data without target labels.

Examples:

- Clustering
- Dimensionality reduction

### Reinforcement Learning

An agent learns through interaction with an environment using rewards and penalties.

## 3. Regression

Regression predicts a continuous numerical value.

Examples:

- Predicting marks
- Predicting house prices
- Predicting temperature

Common algorithms:

- Linear Regression
- Decision Tree Regression
- Random Forest Regression
- Gradient Boosting

## 4. Classification

Classification predicts categories.

Examples:

- Pass/Fail
- Spam/Not Spam
- High/Medium/Low risk

Algorithms include:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine
- K-Nearest Neighbors
- Naive Bayes

## 5. Clustering

Clustering groups similar data points.

A common algorithm is K-Means.

Applications include:

- Customer segmentation
- Document grouping
- Pattern discovery

## 6. Features and Target

Features are input variables used by a model.

The target is the value the model attempts to predict.

Example:

```text
Features:
previous marks
attendance
study hours

Target:
future marks
```

## 7. Training and Testing

A dataset is commonly divided into:

- Training data
- Validation data
- Testing data

Training data is used to learn model parameters.

Testing data is used to evaluate performance on unseen data.

## 8. Overfitting

Overfitting occurs when a model learns the training data too closely and performs poorly on unseen data.

Solutions include:

- More training data
- Regularization
- Simpler models
- Cross-validation
- Pruning
- Early stopping

## 9. Underfitting

Underfitting occurs when a model is too simple to capture important patterns.

## 10. Evaluation Metrics

### Regression

Common metrics:

- MAE
- MSE
- RMSE
- R²

### Classification

Common metrics:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

## 11. Feature Scaling

Feature scaling transforms numerical features to comparable ranges.

Common techniques:

- Standardization
- Min-Max normalization

Tree-based models generally require less scaling than distance-based algorithms.

## 12. Random Forest

Random Forest is an ensemble algorithm that combines multiple decision trees.

Advantages:

- Handles nonlinear relationships
- Works with many features
- Usually robust
- Can estimate feature importance

## 13. Gradient Boosting

Gradient Boosting builds models sequentially, where each new model attempts to improve previous errors.

It is useful for regression and classification problems.

## 14. Machine Learning Pipeline

A typical pipeline is:

```text
Raw Data
 ↓
Cleaning
 ↓
Feature Engineering
 ↓
Train/Test Split
 ↓
Preprocessing
 ↓
Model Training
 ↓
Evaluation
 ↓
Model Saving
 ↓
Prediction API
```

## 15. Important Questions

1. What is machine learning?
2. Explain supervised and unsupervised learning.
3. What is regression?
4. What is classification?
5. What is clustering?
6. What is overfitting?
7. What is underfitting?
8. Explain training and testing data.
9. Explain precision and recall.
10. What is Random Forest?
11. What is Gradient Boosting?
12. What is feature engineering?

## Quick Revision

```text
Machine Learning
├── Supervised
│   ├── Regression
│   └── Classification
├── Unsupervised
│   ├── Clustering
│   └── Dimensionality Reduction
├── Reinforcement Learning
├── Preprocessing
├── Feature Engineering
├── Model Training
├── Evaluation
└── Prediction
```