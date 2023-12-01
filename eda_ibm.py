# -*- coding: utf-8 -*-
"""eda_ibm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17IRgSbhatXccK2FhCnFmG9hjid7Y0NZs
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

import warnings
warnings.filterwarnings("ignore")

# import data modelling libraries
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.combine import SMOTETomek
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from google.colab import files
uploaded = files.upload()

data = pd.read_csv('new_train.csv')

# check shape of dataset
print("shape of the data:", data.shape)
data.head()

# check data types of all columns
data.dtypes

#check missing data
data.isnull().sum()

#check for class imbalance
#target class count
data["y"].value_counts()

sns.countplot(x="y", data=data)
plt.title("Target Variable")
plt.show()

data["y"].unique()

# percentage of class present in target variable(y)
print("percentage of NO and YES\n",data["y"].value_counts()/len(data)*100)

#exploratory data analysis
# indentifying the categorical variables
cat_var= data.select_dtypes(include= ["object"]).columns
print(cat_var)

# plotting bar chart for each categorical variable
plt.style.use("ggplot")

for column in cat_var:
    plt.figure(figsize=(20,4))
    plt.subplot(121)
    data[column].value_counts().plot(kind="bar")
    plt.xlabel(column)
    plt.ylabel("number of customers")
    plt.title(column)

# replacing "unknown" with the mode
for column in cat_var:
    mode= data[column].mode()[0]
    data[column]= data[column].replace("unknown", mode)

#Univariate analysis of Numerical columns
# identifying the numerical variables
num_var= data.select_dtypes(include=np.number)
num_var.head()

# plotting histogram for each numerical variable
plt.style.use("ggplot")
for column in ["age", "duration", "campaign"]:
    plt.figure(figsize=(20,4))
    plt.subplot(121)
    sns.distplot(data[column], kde=True)
    plt.title(column)

#Since pdays and previous consist majorly only of a single value, their variance is quite less and hence we can drop them since technically will be of no help in prediction.
data.drop(columns=["pdays", "previous"], axis=1, inplace=True)

#handling outliers
data.describe()
#age duration and campaign are skewed towards right, we will compute the IQR and replace the outliers with the lower and upper boundaries

# compute interquantile range to calculate the boundaries
lower_boundries= []
upper_boundries= []
for i in ["age", "duration", "campaign"]:
    IQR= data[i].quantile(0.75) - data[i].quantile(0.25)
    lower_bound= data[i].quantile(0.25) - (1.5*IQR)
    upper_bound= data[i].quantile(0.75) + (1.5*IQR)

    print(i, ":", lower_bound, ",",  upper_bound)

    lower_boundries.append(lower_bound)
    upper_boundries.append(upper_bound)

lower_boundries

upper_boundries

# replace the all the outliers which is greater then upper boundary by upper boundary
j = 0
for i in ["age", "duration", "campaign"]:
    data.loc[data[i] > upper_boundries[j], i] = int(upper_boundries[j])
    j = j + 1

# without outliers
data.describe()

