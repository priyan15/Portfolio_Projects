
# Supervised Learning  

Supervised learning is a core subfield of machine learning where a model is trained using labeled data. In this setup, each training example consists of a pair: input features (the data) and the corresponding output (the correct answer).

By analyzing these pairs, the model identifies underlying patterns and relationships, allowing it to make accurate predictions when presented with new, unseen information. This approach is generally divided into two main categories:

Classification: Predicting a discrete label or category (e.g., "Success" or "Failure").

Regression: Predicting a continuous, numerical value (e.g., a specific price or measurement).

## Model
A Model is a computer program that is trained on data to identify patterns, make predictions or classifications without explicit programming. 

## Regression  

Regression predicts continuous quantities like housing prices, some sort of measurements.
The goal of the regression model is to find the best fit line or curve that minimizes the difference between actual and predicted values.

### Linear Regression

Linear Regression is a supervised learning algorithm that assumes there is a linear or straight line relationship between the input and the output. Linear Model makes a prediction by simply computing a weighted sum of inputs plus a constant called as bias term.

Equation for Linear Regression model prediction:
<br>
$y = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \dots + \theta_n x_n$

where y is predicted value.
n is number of features.
$x_i$ is the ith input feature value.
$theta_0$ is the bias term.
$theta_j$ is the jth model parameter or the feature weight.
<br>
Bias is where the line starts.


<details>
<summary>Note on different Notations of the equation</summary>

A. The Summation (The Long Way)
$$y = \theta_0 + \theta_1x_1 + \theta_2x_2 + \dots + \theta_nx_n$$
This is intuitive but hard to write out if you have 1,000 features.

B. The Dot Product ($\theta \cdot x$)
In physics or basic math, you just multiply the corresponding elements of two lists and add them up. It turns the two vectors into a single number (a scalar).

C. The Vectorized Form ($\theta^T x$)
This is the standard "Machine Learning" way.In code (like NumPy or TensorFlow), $\theta$ and $x$ are usually stored as column vectors (tall and skinny).You cannot multiply two column vectors directly.By transposing $\theta$ ($\theta^T$), you flip it sideways into a row vector.Row vector $\times$ Column vector = a single value.

</details>


Most Common performance measure for regression:
* Root mean square error
* But minimizing RMSE is equivalent to minimizing MSE. So for practical purposes MSE can be considered as well.

**Cost Function/ Loss Function / Objective Function** is a mathematical formula that measures how wrong the model is.

<details>
<summary>Note on Cost Function</summary>

If the Supervised Learning process is like a student learning from a teacher, the Cost Function is the red pen the teacher uses to grade the exam. It quantifies the distance between the model's prediction and the actual correct answer.

</details>

<br>

**MSE cost function for a Linear Regression model**

$$
\text{MSE}(\mathbf{X}, h_\theta) = \frac{1}{m} \sum_{i=1}^{m} \left( \theta^T \mathbf{x}^{(i)} - y^{(i)} \right)^2
$$

<br>

<details>
<summary>Notation Summary</summary>

$MSE(X, h_{\theta})$: 
The Mean Squared Error calculated over your dataset $X$ using your model (hypothesis) $h_{\theta}$.
<br>
$\frac{1}{m}$: We divide by the number of instances ($m$) to get the average error.
<br>
$\sum_{i=1}^{m}$: The summation symbol, telling us to add up the results for every instance from $i=1$ to $m$.
<br>
$\theta^T x^{(i)}$: This is the prediction for the $i^{th}$ instance (using the vectorized form we discussed earlier).
<br>
$y^{(i)}$: This is the actual label (the true value) for the $i^{th}$ instance.
<br>
$^2$: Squaring the difference ensures that errors are always positive and that larger errors are penalized more significantly than smaller ones.
</details>


To find the value of θ that minimizes the cost function, there is a closed-form solution
—in other words, a mathematical equation that gives the result directly. This is called
the Normal Equation.

**Normal Equation**

$$
\hat{\theta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$
* $\hat{\theta}$ is the value of $\theta$ that minimizes the cost function.
* $\mathbf{y}$ is the vector of target values containing $y^{(1)}$ to $y^{(m)}$.


<details>
<summary>Derivation of Normal Equation</summary>
To understand how we reach the Normal Equation, we have to use a bit of calculus. In mathematics, if you want to find the minimum of a function (the "bottom of the valley"), you find the derivative and set it to zero.

Here is the step-by-step logic of how we get from the MSE to the Normal Equation.

### 1. Start with the Cost Function (Matrix Form)
First, we write the Mean Squared Error in matrix notation. Instead of using the summation ($\sum$), we use the property that the square of a vector's length is the vector transposed times itself:

$$
J(\theta) = \frac{1}{m} (\mathbf{X}\theta - \mathbf{y})^T (\mathbf{X}\theta - \mathbf{y})
$$

$(\mathbf{X}\theta - \mathbf{y})$ is the vector of all errors (predictions minus actuals). Multiplying it by its own transpose $(\dots)^T$ is just a fancy way of squaring all those errors and adding them up.

### 2. Expand the Equation
Using the rules of matrix algebra, we expand the terms:

$$
J(\theta) \propto \theta^T \mathbf{X}^T \mathbf{X} \theta - 2(\mathbf{X}\theta)^T \mathbf{y} + \mathbf{y}^T \mathbf{y}
$$

*(Note: We can ignore the $1/m$ for now because minimizing a function divided by a constant is the same as minimizing the function itself.)*

### 3. Take the Derivative
To find the minimum, we take the partial derivative of the cost function $J(\theta)$ with respect to the parameter vector $\theta$. This is called the Gradient:

$$
\frac{\partial}{\partial \theta} J(\theta) = 2\mathbf{X}^T \mathbf{X} \theta - 2\mathbf{X}^T \mathbf{y}
$$

* The derivative of $\theta^T \mathbf{X}^T \mathbf{X} \theta$ is $2\mathbf{X}^T \mathbf{X} \theta$ (similar to how the derivative of $ax^2$ is $2ax$).
* The derivative of $2\theta^T \mathbf{X}^T \mathbf{y}$ is $2\mathbf{X}^T \mathbf{y}$.

### 4. Set to Zero and Solve
To find the value of $\theta$ that minimizes the error, we set the gradient to zero:

$$
2\mathbf{X}^T \mathbf{X} \theta - 2\mathbf{X}^T \mathbf{y} = 0
$$

Now, we solve for $\theta$:
1. **Move the term over:** $2\mathbf{X}^T \mathbf{X} \theta = 2\mathbf{X}^T \mathbf{y}$
2. **Cancel the 2s:** $\mathbf{X}^T \mathbf{X} \theta = \mathbf{X}^T \mathbf{y}$
3. **Isolate $\theta$:** Since we cannot "divide" by a matrix, we multiply by the inverse of $(\mathbf{X}^T \mathbf{X})$:

$$
\hat{\theta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

</details>




### Polynomial Regression

Polynomial regression is used when the relationship between the independent variable (input) and dependent variable (output) is non-linear. Unlike linear regression which fits a straight line, it fits a polynomial equation to capture the curve in the data.

Polynomial regression is an extension of linear regression where higher-degree terms are added to model non-linear relationships. The general form of the equation for a polynomial regression of degree 
n is:

$$
y = \beta_0 + \beta_1 x + \beta_2 x^2 + \dots + \beta_n x^n + \epsilon
$$


Where:

- \( y \) is the dependent variable.  
- \( x \) is the independent variable.  
- $$ \beta_0, \beta_1, \dots, \beta_n $$
 are the coefficients of the polynomial terms.  
- \( n \) is the degree of the polynomial.  
- \( $$\epsilon $$\) represents the error term.  


<details>
<summary> Bias VS Variance Tradeoff </summary>
The bias-variance tradeoff is the balance between a model being too simple (high bias) and too complex (high variance), aiming to minimize total prediction error on unseen data.

Understanding Bias and Variance
Bias refers to errors caused by overly simplistic assumptions in a model. High-bias models fail to capture the underlying patterns in the data, leading to underfitting, where both training and test errors are high. For example, a linear regression model assuming a strictly linear relationship may perform poorly if the true relationship is more complex. 

Variance refers to errors caused by a model being too sensitive to fluctuations in the training data. High-variance models capture not only the underlying patterns but also the noise, leading to overfitting, where training error is low but test error is high. For instance, a very deep decision tree may perfectly fit training data but generalize poorly to new examples. 


The total prediction error can be expressed as:
Total Error = Bias² + Variance + Irreducible Error,
where irreducible error represents noise in the data that cannot be eliminated. 

The Tradeoff
The tradeoff arises because reducing bias typically increases variance and vice versa. Simple models (few parameters) have high bias and low variance, while complex models (many parameters) have low bias and high variance. The goal is to find an optimal model complexity that balances both, achieving low error on unseen data. 


</details>

### Support Vector Regression  


<br>


## Classification  

### Logistic Regression



### K- Nearest Neighbors

### Support Vector Machines

### Naive Bayes  
<br>


## Tree Based Models & Ensemble Learning  

### Decision Trees

### Random Forest

### Gradient Boosting (XGBoost, LightGBM)  

<br>


## Advanced Model Variants:  
### Multi-Class Classifcation
### Multi-Label Classification
### Kernel Models

<br>


## Regularization:  
### L1 Regularization (Lasso)
### L2 Regularization (Ridge)
### Elastic Net
### Dropout

<br>


## Optimization Algorithms:
### Gradient Descent
### Stochastic Gradient Descent
### Mini-Batch Gradient Descent
### Momentum
### NAG Optimizer
### Adagrad
### RMSProp
### Adam Optimizer
### AdamW
### Adafactor
### Shampoo
### Sophia
### LARS/ LAMB

<br>


## Loss Functions:  
### Mean Absolute Error
### Mean Squared Error
### Binary Cross-Entropy
### Hinge Loss

<br>


## Feature Engineering And Selection:  
### Dimensionality Reduction
### Scaling and Normalization

<br>


## Important Metrics:  

### Mean Absolute Error

### Mean Squared Error

### R^2 Score

### Accuracy

### Precision

### Recall

### F1- Score  




### ROC-AUC Curve



## Model Evaluation And Validation Strategies

### Cross-Validation

#### What is it?
Cross-validation (CV) is a statistical technique used to estimate the skill of a machine learning model on unseen data. It is a more robust alternative to a simple train/test split. In a simple split, you might get "lucky" or "unlucky" with the specific data points that end up in your test set; CV eliminates this bias by ensuring every data point is used for both training and testing.

####  Why Use It?
**Reduces Overfitting:** It provides a better estimate of how the model will perform in the real world.

**Data Efficiency:** It is especially useful when your dataset is small, as it maximizes the use of available data.

**Stability:** It provides a mean and standard deviation for your metrics, showing how sensitive the model is to different data inputs.

#### Common Types of Cross-Validation

1. **K-Fold Cross-Validation:** The most common approach.
The **Process**: The dataset is split into $k$ equal-sized "folds."

The **Loop**: The model is trained $k$ times. Each time, a different fold is used as the test set (the "holdout"), and the remaining $k-1$ folds are used for training.

The **Result**: The final performance score is the average of the scores from all $k$ iterations.

2. **Stratified K-Fold** Used primarily for Classification tasks where the classes are imbalanced.

The **Process**: It ensures that each fold contains roughly the same percentage of samples of each target class as the complete set.Example: If your dataset has 90% "No" and 10% "Yes," every fold will maintain that 90/10 ratio.

3. **Leave-One-Out (LOOCV)** 

The **Process**: $k$ is set to the total number of observations ($n$).

The **Loop**: For every single data point, the model trains on everything else and predicts that one point.

**Pros/Cons**: Very thorough, but computationally expensive and can lead to high variance in results.

#### The Workflow in Practice

Shuffle the dataset randomly.

Split into $k$ folds (usually $k=5$ or $k=10$).

For each fold:
Train the model on $k-1$ folds.
Validate on the remaining fold.
Record the metric (e.g., Accuracy or MSE).

Aggregate: Calculate the mean of the recorded metrics to get the "CV Score.

"Pro-Tip: When performing Feature Engineering (like Scaling), always perform it within the cross-validation loop (using a Pipeline). If you scale the whole dataset before CV, information from the "test" folds "leaks" into the "train" folds, leading to overly optimistic results. This is known as Data Leakage.


# Cross-Validation

## What is Cross-Validation?

Cross-validation is a resampling technique used to evaluate the performance of a machine learning model on a limited dataset. Instead of relying on a single train/test split, it systematically splits the data multiple times to ensure that every data point gets a chance to be used for both training and testing.

The most common version is **K-Fold Cross-Validation**, where the dataset is split into \(K\) equal-sized folds. The model is trained on \(K-1\) folds and tested on the remaining fold, repeating this process \(K\) times.

---

## Advantages of Cross-Validation

### 1. Robust and Reliable Performance Estimation

* **Reduces Evaluation Bias:** A single, random train/test split can result in a "lucky" or "unlucky" test set that doesn't accurately reflect how the model will perform on unseen data. Cross-validation averages the metrics across multiple runs, providing a more reliable estimate.
* **Full Data Utilization:** Every single observation in the dataset is used for both training and testing exactly once. This is highly beneficial when working with small datasets where you cannot afford to waste data on a permanent test split.

### 2. Better Prevention of Overfitting

* Overfitting occurs when a model learns the noise in the training data rather than the underlying pattern. Because cross-validation evaluates the model on multiple unseen folds, it highlights if a model performs exceptionally well on its training data but poorly on validation data.

### 3. Effective Hyperparameter Tuning

* It allows for safe grid searches or random searches when adjusting model settings (hyperparameters). You can confidently pick the parameters that yield the highest average cross-validation score, knowing it isn't an artifact of a single data split.

### 4. Ideal for Model Selection

* It provides a fair baseline to compare different algorithms (e.g., comparing a Linear Regression model against a Decision Tree on the exact same dataset splits) to see which architecture handles the data structure better.

---

## Disadvantages of Cross-Validation

### 1. High Computational Cost and Time

* **Multiplied Training Time:** If a model takes 2 hours to train, a 5-Fold cross-validation will take roughly 10 hours, and a 10-Fold will take 20 hours because the model must be completely retrained from scratch for every fold.
* **Resource Intensive:** For deep learning networks or massive datasets, this multiplication of training iterations is often computationally prohibitive.

### 2. Limitations with Time-Series Data

* **Breaks Temporal Order:** Standard cross-validation shuffles data randomly. For time-series data (e.g., stock prices, weather predictions), predicting past data using future data creates data leakage. Specialized techniques like *Time-Series Split (Forward Chaining)* must be used instead.

### 3. Data Leakage If Done Incorrectly

* A common pitfall is performing data preprocessing steps (like scaling data, normalizing, or selecting features) on the *entire* dataset *before* splitting it into folds. This allows information from the validation fold to leak into the training fold, leading to overly optimistic performance scores that fail in production.

### 4. Imbalance Issues without Stratification

* On heavily imbalanced datasets (e.g., fraud detection where only 0.1% of cases are fraudulent), a random split might result in some folds having zero fraud cases. To counter this, developers must use **Stratification** (Stratified K-Fold) to ensure each fold retains the correct percentage of each class.

---

## Summary Comparison


| Feature | Single Train/Test Split | K-Fold Cross-Validation |
| :--- | :--- | :--- |
| **Computation Speed** | Fast (Trains only once) | Slow (Trains \(K\) times) |
| **Variance in Score** | High (Highly dependent on the split) | Low (Averaged over multiple splits) |
| **Data Efficiency** | Poor (Chunks of data are locked away) | Excellent (All data is utilized) |
| **Best Used For** | Large datasets / Deep Learning | Small to medium datasets / Traditional ML |


Evaluating the performance of a machine learning model—especially for classification—requires more than just looking at "accuracy." If you have a dataset where 99% of people are healthy, a model that simply guesses "healthy" every time will be 99% accurate but completely useless at finding sick people. That’s where these metrics come in.



# The Confusion Matrix

The **Confusion Matrix** is the foundation for all other metrics. It is a $N \times N$ table (where $N$ is the number of classes) that summarizes how many predictions were correct and how many were "confused" with another class.

For binary classification, the matrix consists of four quadrants:


| | Predicted: Positive | Predicted: Negative |
| --- | --- | --- |
| **Actual: Positive** | **True Positive (TP)** | **False Negative (FN)** |
| **Actual: Negative** | **False Positive (FP)** | **True Negative (TN)** |

* **True Positive (TP):** You predicted positive, and it was actually positive (e.g., predicted "Cancer," patient has cancer).
* **True Negative (TN):** You predicted negative, and it was actually negative (e.g., predicted "Healthy," patient is healthy).
* **False Positive (FP):** You predicted positive, but it was negative. Also known as a **Type I Error** (e.g., "False Alarm").
* **False Negative (FN):** You predicted negative, but it was positive. Also known as a **Type II Error** (e.g., "Missed Detection").

---

## 2. Precision

**Precision** (also called Positive Predictive Value) answers the question: *“Of all the instances the model predicted as positive, how many were actually positive?”* It is a measure of **quality** and "exactness." High precision means you don't label many negative items as positive.

$$\text{Precision} = \frac{TP}{TP + FP}$$

* **When to use:** Use precision when the cost of a False Positive is high.
* **Example:** In **Spam Detection**, you want high precision. If a model has low precision, it will flag important work emails (False Positives) as spam.

---

## 3. Recall

**Recall** (also called Sensitivity or True Positive Rate) answers the question: *“Of all the actual positive instances that exist, how many did the model correctly identify?”* It is a measure of **quantity** and "completeness." High recall means you didn't miss many positive cases.

$$\text{Recall} = \frac{TP}{TP + FN}$$

* **When to use:** Use recall when the cost of a False Negative is high.
* **Example:** In **Cancer Diagnosis**, you want high recall. It is much worse to tell a sick person they are healthy (False Negative) than to put a healthy person through more tests (False Positive).

---

## 4. F1 Score

In the real world, there is usually a **Precision-Recall Trade-off**. As you try to improve one, the other often drops. The **F1 Score** is the harmonic mean of Precision and Recall, providing a single score that balances both.

$$\text{F1 Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

> **Note:** We use the harmonic mean instead of a simple average because the harmonic mean penalizes extreme values. If one metric is 1.0 and the other is 0.0, the F1 score will be 0, not 0.5.

* **When to use:** Use the F1 Score when you have an **imbalanced dataset** and you need a balance between Precision and Recall.

---

## Summary Comparison Table


| Metric | Focus | Key Question | Best For... |
| --- | --- | --- | --- |
| **Precision** | Reliability | How sure are we that a "positive" is actually positive? | Avoiding False Alarms (Spam filters) |
| **Recall** | Coverage | How many of the actual positives did we capture? | Avoiding Misses (Medical tests, Security) |
| **F1 Score** | Balance | Is there a good middle ground? | Imbalanced classes |

