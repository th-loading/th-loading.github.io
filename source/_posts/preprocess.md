---
title: preprocess
date: 2022-01-07 17:14:04
tags: machine learning
---

# Preprocess

## read_file

```python
base_path = os.path.abspath(__file__ + "/../")
path = os.path.join(base_path,'data')
train_path = os.path.join(path,'train.csv')
test_path = os.path.join(path,'test.csv')
result_path = os.path.join(path,'submission.csv')

train_df = pd.read_csv(train_path)    
test_df = pd.read_csv(test_path)    
result_df = pd.read_csv(result_path)   
```

## 头文件

```python
# basic
import os
import re
import time
import pandas as pd
import numpy as np

# plot
import seaborn as sns
from matplotlib import gridspec
from matplotlib import pyplot as plt

# preprocess
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler

# cross_validation
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import cross_validate

# models
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier

# estimate
from sklearn.model_selection import validation_curve
from sklearn.model_selection import learning_curve
from sklearn.metrics import confusion_matrix
```

## 随机数

```python
def generate_randn(mean=0, std=0, max_val=np.inf, min_val=-np.inf):
    num = std * np.random.randn() + mean
    if num > max_val:
        return max_val
    elif num < min_val:
        return min_val
    else:
        return num
```

## log

```python
def show_log():
    print('param:')
    
    cur = []
    basic = "Step "
    len_key = len(basic)
    key_ind = 4
    
    for log_str in log[::-1]:
        if int(log_str[len_key]) == key_ind:
            cur.append(log_str)            
            key_ind -= 1
        if key_ind == 0:
            break
        
    print('\n'.join(cur[::-1]))
    print()
```

## 观察数据

### 预设

```python
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100
pd.set_option('max_rows', 100)
pd.set_option("max_columns", 50)
pd.set_option("expand_frame_repr", False)

# global 
max_score = 0
log = []
np.random.seed(2)
i = 0
cat_df = train_df.copy()

#split
X_train,X_test,y_train,y_test = train_test_split(X,y)
```

### 分类

离散标签 连续数值 字符串

```python
def show_basic(df):
    print(df.columns)
    # type and nums
    print(df.info())
    # unique of type
    print(df.describe(include='O'))
    # series -> 增加25-75
    print(df.describe())
    
# 分别查看每一列的数据
def cat_columns(df):
    for column in list(df.columns):
        print(df[column].head(5))

# 查看相关系数矩阵
def cat_cov(df):
    fig,ax = plt.subplots()
    matrix = df.corr()
    ax = sns.heatmap(matrix)
    plt.show()   
```

### 离散标签

```python
# 单个标签与结果
def show_label_distributions(df,labels,target):
    length = int(np.sqrt(len(labels))) + 1
    fig = plt.figure()
    grid = gridspec.GridSpec(length,length,fig)
    for a_len in range(length):
        for a_width in range(length):
            ax = fig.add_subplot(grid[a_width,a_len])
            index = a_len * length + a_width
            if index < len(labels):
                label = labels[index]
                result = df[[label,target]].groupby(
                    label,
                    as_index=False
                ).mean().sort_values(
                    by=target, ascending=False
                )
                print(result)
                sns.lineplot(ax=ax,x=result[label], y=result.Survived)
    plt.tight_layout()
    plt.show()

# 多个标签与结果

# x代表离散点,y值代表分布,hue为两条曲线的对比 col为多个标签
def show_label_pointplot(df, col=None, row=None, x=None, y=None, hue=None,change_x=False):
    grid = sns.FacetGrid(df, col=col,row=row)
    # 长度表示标准差，点表示均值
    grid.map(sns.pointplot, x, y, hue=hue, palette='deep',dodge=True)
    grid.add_legend()
    plt.tight_layout()
    if change_x == True:
        for ax in grid.axes.flat:
            plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.show()
```

### 连续数值

```python
# 枚举行和列的标签下目标数值的分布
def show_num_hist(df, targets, col=None, row=None):
    for target in targets:
        g = sns.FacetGrid(df, col=col, row=row)
        g.map(plt.hist,target, bins=20)
        plt.show()

# 方式一 观察不同标签下目标的分布情况
# 方式二 观察不同目标（band)下标签的分布情况 -> 转换为label plot
def show_num_barplot(df, col=None, row=None, x=None, y=None, hue=None,ci=None):
    grid = sns.FacetGrid(df,col=col,row=row)
    # ci = False 不显示标准差
    grid.map(sns.barplot,x,y,hue=hue,ci=ci)
    grid.add_legend()
    plt.show()

# 表示密度
def show_num_violinplot(df, col=None, row=None, x=None, y=None, hue=None,ci=None):
    grid = sns.FacetGrid(df,col=col,row=row)
    grid.map(sns.violinplot,x,y,hue=hue)
    grid.add_legend()
    plt.show()

def num_to_label(df,num_column,bins=5):
    length = int(np.sqrt(len(num_column))) + 1
    fig = plt.figure()
    grid = gridspec.GridSpec(length,length,fig)
    for a_len in range(length):
        for a_width in range(length):
            ax = fig.add_subplot(grid[a_width,a_len])
            index = a_len * length + a_width
            if index < len(num_column):
                new_column_name = num_column[index] + 'Band'
                df[new_column_name] = pd.qcut(df[num_column[index]],bins)
                sns.pointplot(data=df,ax=ax, x=new_column_name, y='Survived')
                plt.setp(
                    ax.get_xticklabels(),
                    rotation=30,
                    horizontalalignment='right',
                    fontsize='x-small'
                )
    plt.tight_layout()
    plt.show()
```

### String

```python
# 根据pattern提取特征
def show_str_labels(df,column,labels):
    for label in labels:
    # 求frequency
        print(
            pd.crosstab(
                df[column], df[label]
            ).apply(
                lambda r: r/r.sum(), axis=1
            )
        )        
        
def show_str_dist(df,str_columns,patterns,labels):
    for str_column,pattern in zip(str_columns,patterns):
        new_column = str_column + 'Type'
        df.loc[:,new_column] = df[str_column].str.extract(
            pattern,
            expand=False
        )
        print(df[new_column].value_counts(normalize=True))
        show_str_labels(df,new_column,labels)
        
# 将nan与其他分开
def show_str_nan(df,str_columns):
    for column in str_columns:
        new_column = column + 'Type'
        df[new_column] = df[column]
        df.loc[
            df[new_column].notnull(),new_column
        ] = 'cabin'
        df[new_column].fillna('None',inplace=True)
        show_str_labels(df,'CabinType',['Survived'])
```

### Process

```python
# 查看特征

# 确定数据类型
show_basic(cat_df)

cat_columns(cat_df)

label_column = [
    'Pclass', 'Embarked','SibSp',
    'Parch', 'Sex',
]

num_column = [
    'Fare', 'PassengerId', 'Age'
]

band_column = [
    'FareBand', 'PassengerIdBand', 'AgeBand'
]

str_column = [
    'Name','Cabin'
]

type_column = [
    'NameType','CabinType'            
]

# 确定标签分布
show_label_distributions(cat_df,label_column,'Survived')

# 数值分布特点（补nan）
show_num_hist(cat_df,num_column)
show_num_hist(cat_df,['Age'],col='Pclass',row='Survived')

# 添加新标签
cat_df['family'] = cat_df['SibSp'] + cat_df['Parch']
new_column = label_column + ['family']
show_label_distributions(cat_df,new_column,'Survived')
cat_df.drop('family',axis=1,inplace=True)

# 查看数值与目标的关系
show_num_violinplot(cat_df,x='Survived',y='Age')
show_num_violinplot(cat_df,x='Survived',y='Fare')
show_num_violinplot(cat_df,x='Survived',y='PassengerId')

# 转标签
num_to_label(cat_df,['Age','Fare','PassengerId'])

# 字符串匹配
patterns = [' ([A-Za-z]+)\.']
columns = label_column + band_column
show_str_dist(cat_df,['Name'],patterns,columns)

# 字符串0-1
show_str_nan(cat_df,['Cabin'])
columns = ['Survived']
show_label_pointplot(cat_df,x='CabinType',y='Survived')
```

## 改进数据

### data-mismatch

只需要判断模糊数据 但大部分数据是清晰的 
语音识别中的特定的应用场景
dev 和 test 采用模糊数据 训练集大部分清晰 小部分模糊
增加train-dev set 查看造成variance的原因

人工分析dev数据与train数据的 
添加噪音...(artificial data synthesis)
问题 反复的重复导致对噪音的过拟合

### 填充

```python
# 填充 
# 根据正态分布
# 填充年龄        
def fill_age_mean(df):
    # fig,axs = plt.subplots(1,2,sharey=True)
    # show_hist(axs[0],df['Age'])
    mean_age = df['Age'].mean()
    std_age = df['Age'].std()
    max_age = df.Age.max()
    min_age = df.Age.min()
    np.random.seed(seed=1)
    # print(len(df.loc[df.Age == 0, 'Age']))
    df.loc[:, 'Age'] = df.loc[:, 'Age'].apply(
        lambda x: int(generate_randn(
            mean_age,
            std_age,
            max_age,
            min_age
        )) if np.isnan(x) else x
    )
    # show_hist(axs[1], df['Age'])
    # plt.show()
    return df

def fill_age_split(df):
    df.loc[:,'Sex_cat'].replace({'female':1,'male':0},inplace=True)
    for i in range(0, 2):
        for j in range(0, 3):
            part_df = df.loc[(df['Sex_cat'] == i) & \
                            (df['Pclass'] == j+1),['Age']]
            part_df = fill_age_mean(part_df)
            df.update(part_df)
    return df

# 根据频率
def fill_embarked(df):
    freq_port = df.Embarked.dropna().mode()[0]
    df['Embarked'] = df['Embarked'].fillna(freq_port)
    return df 
    
# 根据中位数
def fill_fare(df):
    df['Fare'].fillna(df['Fare'].dropna().median(), inplace=True)
    return df
```

### 平方项

```python
# 增加平方或交互项
# 顺序 1，x,y,z,x^2,xy,xz,y^2,yz...
from sklearn.preprocessing import PolynomialFeatures
def add_polynomial(df):
    columns = [
        'Age', 'SibSp', 'Parch', 'Fare',
    ]
    poly = PolynomialFeatures(2)
    t = poly.fit_transform(df[columns])
    new_columns = [
        'A_2', 'A_S', 'A_P', 'A_F', 'S_2',
        'S_P', 'S_F', 'P_2', 'P_F', 'F_2'
    ]
    for i in range(5,15):
        df.loc[:,new_columns[i-5]] = t[:,i]
    return df
```

### 编码

```python
# label encoder
from sklearn.preprocessing import LabelEncoder

def code_label_columns(df,columns):
    for column in columns:
        column_name = f"{column}_cat"
        df.loc[:,column] = df[column].astype('category')
        df[column_name] = df[column].cat.codes    
    return df

def code_hot_columns(df,columns):
    for column in columns:
        prefix = f"{column}_Type"
        code_df = pd.get_dummies(
            df[[column]], columns=[column], prefix=[prefix] 
        )
        df=df.join(code_df)
    return df
```

### 忽略

```python
# 忽略部分列
def ignore_columns(df,columns):
    df.drop(columns, axis=1, inplace=True)
    return df
```

### 标准/归一

不标准化导致学习率不好确定 -> 不利于梯度下降 

```python
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
def normal(df,column_list):
    column_list = [column for column in column_list if column in df.columns]
    df.loc[:,column_list] = Normalizer().fit_transform(df.loc[:,column_list])
    return df
```

