# Deep Learning — Fundamentals

## 1. Introduction

Deep Learning is a subfield of machine learning that uses neural networks with multiple layers to learn complex patterns from data.

It is widely used in:

- Computer vision
- Natural language processing
- Speech recognition
- Recommendation systems
- Generative AI

## 2. Artificial Neural Network

An artificial neural network consists of interconnected neurons.

Basic structure:

```text
Input Layer
     ↓
Hidden Layer(s)
     ↓
Output Layer
```

## 3. Neuron

A neuron receives inputs, applies weights and a bias, and passes the result through an activation function.

Conceptually:

```text
Inputs → Weighted Sum → Activation → Output
```

## 4. Activation Functions

Activation functions introduce non-linearity.

Common functions:

- ReLU
- Sigmoid
- Tanh
- Softmax

### ReLU

ReLU returns zero for negative values and approximately the input for positive values.

It is commonly used in hidden layers.

### Sigmoid

Produces values between 0 and 1 and is commonly used for binary classification outputs.

### Softmax

Converts multiple output values into a probability distribution.

## 5. Forward Propagation

During forward propagation, input data passes through the neural network to produce an output.

## 6. Loss Function

A loss function measures the difference between predicted and actual values.

Examples:

- Mean Squared Error
- Binary Cross Entropy
- Categorical Cross Entropy

## 7. Backpropagation

Backpropagation calculates how much each model parameter contributed to the error and uses this information to update the parameters.

## 8. Optimizers

Optimizers update model parameters to minimize the loss.

Common optimizers:

- SGD
- Adam
- RMSprop

## 9. Epoch and Batch

An epoch is one complete pass through the training dataset.

A batch is a smaller group of training samples processed together.

## 10. CNN

Convolutional Neural Networks are especially useful for image-related tasks.

A CNN commonly contains:

```text
Image
 ↓
Convolution
 ↓
Activation
 ↓
Pooling
 ↓
Fully Connected Layer
 ↓
Output
```

Applications:

- Image classification
- Face recognition
- Object detection
- Medical image analysis

## 11. RNN

Recurrent Neural Networks are designed for sequential data.

Applications include:

- Text processing
- Time-series analysis
- Speech-related tasks

Modern sequence applications often use architectures such as LSTM, GRU, and Transformer-based models.

## 12. Transfer Learning

Transfer learning uses knowledge learned by a pretrained model for a new task.

Benefits:

- Faster training
- Requires less data
- Often improves performance

## 13. Overfitting in Deep Learning

Common techniques to reduce overfitting:

- Dropout
- Data augmentation
- Regularization
- Early stopping
- More training data

## 14. Important Questions

1. What is deep learning?
2. What is an artificial neural network?
3. What is an activation function?
4. Explain ReLU.
5. What is backpropagation?
6. What is a loss function?
7. What is an optimizer?
8. What is CNN?
9. What is RNN?
10. What is transfer learning?
11. What is dropout?
12. What is an epoch?

## Quick Revision

```text
Deep Learning
├── Neural Networks
├── Neurons
├── Activation Functions
├── Forward Propagation
├── Loss Function
├── Backpropagation
├── Optimizers
├── CNN
├── RNN
├── LSTM / GRU
└── Transfer Learning
```