---
title: pandas basic
date: 2021-12-12 09:55:24
tags: data
---

# Pandas

```python
import pandas as pd
```

## cat

### basic

```python
df.loc['a'], df['a'], df.at() ,df[['a']](as dataframe)
# iloc series df.iloc[-1,] too many index
df.iloc[1] , df[[1,2]], df.iat()
df.head() , df.tail(), df.sample(n=1)
df.shape(), len(df.columns),
# 最近n天
df.rolling()
# 至今 	
df.expanding()
# -a 下a行
df.shift()
#type
df.dtypes()

def show_basic(df):
    print(df.columns)
    # type and nums
    print(df.info())
    # unique of type
    print(df.describe(include='O'))
    # 查看最常见的值
    print(df.mode())
    # series -> 增加25-75
    print(df.describe())
    
# 分别查看每一列的数据
def cat_df(df):
    for column in list(df.columns):
        print(df[column].head(5))

# 查看相关系数矩阵
def cat_cov(df):
    fig,ax = plt.subplots()
    matrix = df.corr()
    ax = sns.heatmap(matrix)
    plt.show()   

def show_unique(df):
# 沿着axis查看有多少unique
# 查看每列的类型数
    df.nunique(axis=0)
    len(pd.unique(series))

# equal
df.equals(exactly_equal)
```

### print option

```python
pd.set_option('max_rows', 100)
pd.set_option("max_columns", 50)
# 一直延申
pd.set_option("expand_frame_repr", False)
```

### condition

```python
# dict 
dp['wts'][dict_.keys()] = dict_.values()
# 保留非nan 
dp = dp[~np.isnan(dp['wts'])]
# select column 
df.filter(regex=("d.*"))
# loc 
df.loc[mask,'column']
# mask
# 查看(notnull)
mask_1 = df.isnull()
# 不等式
mask_2 = train_df.PassengerId < 7
# regex
mask_3 = Series.str.contains(pat, case=True, flags=re.I, na=None, regex=True)
# 合并
mask = mask_1 & mask_2 & mask_3
# 取值
null_df = df[mask].loc[:,[column_list]]
# 根据index
df.loc[date:]
```

### extract

```python
dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
```

### group

```python
# create group
# function (index)
def func(idx):
    # df global value
    if df.loc[idx] > 0:
        return 'bar'
    else:
        return 'A'
grouped = df.groupby(func,axis=1,dropna=False)
# dict name -> group
grouped.groups
# 命名
grouped = ts.groupby(lambda x: x.year)
grouped.get_group("bar") 	
# apply calculate
# aggregate
grouped.aggregate([np.sum,np.mean,lambda x : x.sum() - x.mean()])

grouped.agg(
     # name = column + function
     min_height=("height", "min"),
     max_height=("height", "max"),
     average_weight=("weight", np.mean),
)
# using a dict on a Series for aggregation is deprecated and will be removed in a future version
# 对于series
grouped.agg(dict{column:func})
# apply
def get_mas(x):
    d = {}
    d['ma_5'] = x.iloc[-5:].mean()
    d['ma_10'] = x.iloc[-10:].mean()
    d['ma_20'] = x.mean()
    return pd.Series(d, index=['ma_5', 'ma_10', 'ma_20'])

target = price_df.close.groupby(price_df.index).apply(get_mas)
# multi-index 
# 根据等级
s.unstack(level=1)
# transform
grouped.transform(func)
```

### cross_tab

```python
pd.crosstab(
	df['Title'], df[label]
).apply(
	lambda r: r/r.sum(), axis=1
)
```

### count

```python
# count_by_value
# frequency
s.value_counts(normalize=True)
# 区间统计 
s.value_counts(bins=3)
# 包括nan
s.value_counts(dropna=False)
# count 统计
df.groupby('a').count()
```

### cut

```python
# cut by quantity
df[new_column_name] = pd.qcut(df[num_column[index]],bins)

# cut by section
df[new_column_name] = pd.cut(df[num_column[index]],bins)
```

### quantile

```python
# 获取数据的分位点
# quartile - quantile - percentile
df.quantile(ratio_list)

```

## change

### copy

df[] 用于查看, 改变值使用df.loc
df.loc[:, columns]的改变无法直接inplace
应该使用df.loc[:, columns]接收
！！！赋值使用df.values

```python
# default deep=True
df.copy()
# 全部由numpy形成的pd则无需深拷贝
# loc条件
```

### Concat

```python
# 默认用nan填充
pd.concat(list, axis)
# 用自定义的值定义
pd.reindex(df1.index,columns=list,fill_value = 'None')
#只在有交集的部分导入
pd.concat(list, axis, join="inner")
#shortcat df.join , df.append
df = df1.join(df2)

# merge by index
new_df = pd.merge(
    a,b,
    how='inner',
    # on = 'column'
    left_index=True,
    right_index=True
)
```

### update

```python
#Modify in place using non-NA values from another DataFrame.
df.update(new_df)
# Update null elements with value in the same location in other.
df1.combine_first(df2)
```

### resample

```python
# date_range 设置index
index = pd.date_range('1/1/2000', periods=9, freq='T')
# 转换类型
pd.to_datetime()

# resample 根据freq处理数据
# label选择右标题
series.resample(freq, label='right').sum()
# 不包括右标题本身 
series.resample('3T', label='right', closed='right').sum()

# as_freq 重新设置freq留出NAN
df.asfreq(freq='30S', fill_value=9.0, method=fill_method)

# 设置index
df.resample('M', on='week_starting').mean()

# 标准日期
pd.offsets.timedelta(days=-6)
# 调整index
delta = pd.timedelta(days=-6)
df.index = df.index + delta

# 调整数据
logic = {'Open'  : 'first',
         'High'  : 'max',
         'Low'   : 'min',
         'Close' : 'last',
         'Volume': 'sum'}

# 调整至周一...
print(df_index.index[0].weekday())
df_sales.resample('2H', base=1).sum()

new_df = df.resample('W',label='left').apply(logic)
delta = pd.Timedelta(days=1)
new_df.index = new_df.index + delta
```

<a href=https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases>freqlist</a>

### fill

```python

from scipy.interpolate import interp1d
from sklearn.metrics import mean_squared_error

df.interpolate(method='cubicspline')

def fill_matrix(df,target_col,origin_df=None):
    fig, axes = plt.subplots(7, 1, sharex=True, figsize=(10, 12))
    plt.rcParams.update({'xtick.bottom' : False})

    df.plot(title='Actual', ax=axes[0], label='Actual', color='green', style=".-")    
    axes[0].legend(["Missing Data", "Available Data"])
    
    df_ffill = df.ffill()
    df_ffill[target_col].plot(title='Forward Fill', ax=axes[1], label='Forward Fill', style=".-")
    
    df_bfill = df.bfill()
    df_bfill[target_col].plot(title="Backward Fill", ax=axes[2], label='Back Fill', color='firebrick', style=".-")
    
    df['rownum'] = np.arange(df.shape[0])
    df_nona = df.dropna(subset = [target_col])
    f = interp1d(df_nona['rownum'], df_nona[target_col])
    df['linear_fill'] = f(df['rownum'])
    df['linear_fill'].plot(title="Linear Fill", ax=axes[3], label='Linear Fill', color='brown', style=".-")

    f2 = interp1d(df_nona['rownum'], df_nona[target_col], kind='cubic')
    df['cubic_fill'] = f2(df['rownum'])
    df['cubic_fill'].plot(title="Cubic Fill", ax=axes[4], label='Cubic Fill', color='red', style=".-")

    def knn_mean(ts, n):
        out = np.copy(ts)
        for i, val in enumerate(ts):
            if np.isnan(val):
                n_by_2 = np.ceil(n/2)
                lower = np.max([0, int(i-n_by_2)])
                upper = np.min([len(ts)+1, int(i+n_by_2)])
                ts_near = np.concatenate([ts[lower:i], ts[i:upper]])
                out[i] = np.nanmean(ts_near)
        return out
    
    df['knn_mean'] = knn_mean(df[target_col].values, 8)
    df['knn_mean'].plot(title="KNN Mean", ax=axes[5], label='KNN Mean', color='tomato', alpha=0.5, style=".-")

    def seasonal_mean(ts, n, lr=0.7):
        out = np.copy(ts)
        for i, val in enumerate(ts):
            if np.isnan(val):
                ts_seas = ts[i-1::-n]  # previous seasons only
                if np.isnan(np.nanmean(ts_seas)):
                    ts_seas = np.concatenate([ts[i-1::-n], ts[i::n]])  # previous and forward
                out[i] = np.nanmean(ts_seas) * lr
        return out

    df['seasonal_mean'] = seasonal_mean(df[target_col], n=12, lr=1.25)
    df['seasonal_mean'].plot(title="Seasonal Mean", ax=axes[6], label='Seasonal Mean', color='blue', alpha=0.5, style=".-")
    
    plt.show()

def GM11(x0): # 自定义灰色预测函数
    import numpy as np
    x1 = x0.cumsum() #1-AGO序列
    z1 = (x1[:len(x1)-1] + x1[1:])/2.0 #紧邻均值（MEAN）生成序列
    z1 = z1.reshape((len(z1),1))
    B = np.append(-z1, np.ones_like(z1), axis = 1)
    Yn = x0[1:].reshape((len(x0)-1, 1))
    [[a],[b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Yn) #计算参数
    f = lambda k: (x0[0]-b/a)*np.exp(-a*(k-1))-(x0[0]-b/a)*np.exp(-a*(k-2)) #还原值
    delta = np.abs(x0 - np.array([f(i) for i in range(1,len(x0)+1)]))
    C = delta.std()/x0.std()
    P = 1.0*(np.abs(delta - delta.mean()) < 0.6745*x0.std()).sum()/len(x0)
    return f, a, b, x0[0], C, P #返回灰色预测函数、a、b、首项、方差比、小残差概率
    
index = pd.date_range('2020-03-09','2021-02-01', freq='B')
t_df = pd.DataFrame(range(len(index)),index=index,columns=['target'])
t_df = t_df.resample('D').asfreq()
fill_matrix(t_df,'target')
```

### calculate

```python
# !!! 计算之前fil
# statistic
df['Age'].mean() 
df['Age'].var()
# shift
df.pct_change(periods=)
df.diff(periods=)
# cumulative
df.cumsum(),df.cumprod()

df[basic[-1]] = df[basic[-1]]/100

final_df[name] = df.close.values/df.open.values - 1
# final_df.loc[:,'']
# get min of id
idxmin()
df.idxmax(axis = 1, skipna = True)

# ema
exp = df.ewm(	
    span=period,
    # 是否使用递推式
    adjust=False
).mean()

# cma
df = df.expanding().mean()

# sma
df = df.rolling(
    window=period
).mean()

# subtract series
# 默认axis = 1 -> 调整角度 .T
df.sub(sr, axis = 1)
# 沿着轴线

# numpy
numpy.dot
np.log(target)
```

### col/index

```python
df.index = list
df.columns = list
df.rename(columns={'c_per':'result'},inplace=True)
df.T 
# new sequential index is used
df.reset_index(drop=False)
# reindex -> 填充逻辑
mask = mask.reindex(price_df.index.values)

# change index
as_list = df.index.tolist()
idx = as_list.index('Republic of Korea')
as_list[idx] = 'South Korea'
df.index = as_list
```

### add/drop

**为了保证数据类型的一致 通过 df2.values 来添加新列**

```python
# columns
# dict map to existing value
# mask column
mask = df.isnull().sum(axis=0) / len(df) < 0.2
df = df.T[mask].T
mask = df.isnull().sum(axis=1)/len(df.columns) < 0.2
df = df[mask]

# mask 
df[len(df.columns)] = list/dict
df.loc[:,column_name] = list
 
df.insert(position,column_name,val,True)
#rows
#若没有该index,默认为在最后插入
df.loc[index] = list

# drop
df.drop(['a'], axis=1, inplace=True)
# 只所有
df = df.dropna(axis = 0, how = 'all')
```

### replace

3-dimension 

```python
# a. column_name(默认为空) 
# b. to_replace
# c. value
# 针对部分类
columns = ['A', 'B']
new_df = df.loc[:, columns]
new_df.replace(3,1,inplace=True)
df.loc[:, columns] = new_df
# pandas dtypes 并非严格规定 可以用其他数据类型填充
# 默认并不插入 df为引用 在函数内inplace可直接改变
df.replace(b, value=c,inplace=True)
# regex r'\1'
df.replace({a : b}, {a : c},regex=True)
df.replace(regex={b:c})
df.replace(a:b:c,regex=True)
# fillna -> type np.nan regex并不会影响nan	
df.fillna(value=,inplace=True)
```

### sort

```python
# 1顺序 0逆序
df.sort_values(by=['a', 'b'], ascending=[1, 1])
df.sort_index()
# rank
df.rank(ascending,pct)
```

## datatype

### muti-index

多索引

```python
# multi-index 
# 根据等级 level 代表标题的层次
# show name
s.index.names
# series to df
s.unstack(level=1)

# set-multi
multi = df.set_index(['Film', 'Chapter', 'Race', 'Character'])

# sort_index
multi = df.set_index([‘Film’, ‘Chapter’, ‘Race’, ‘Character’]).sort_index()

# remove
multi.reset_index()

# loc
multi.loc[('The Fellowship Of The Ring', '01: Prologue'), :]
# 跳过
multi.loc[(‘The Fellowship Of The Ring’,slice(None),’Elf’), :].head(3)

# cross-section get_datas
multi.xs('Isildur', level='Character').sum()

# pivot_table
# word 为统计的目标
# 需要的分类: film，race，charactor 
# 需要计算: film
pivoted = df.pivot_table(
    index = ['Race','Character'],
	columns = 'Film',
    # 针对所有的分出类来的word（包含了其他标签 chaper...）
	aggfunc = 'sum',
    # 设置一个针对所有列的量
	margins = True, # total column
	margins_name = 'All Films',
	# 填充
    fill_value = 0
).sort_index()
# 对列进行排序
order = [('Words', 'The Fellowship Of The Ring'),
         ('Words', 'The Two Towers'),
         ('Words', 'The Return Of The King'), 
         ('Words', 'All Films')]
pivoted = pivoted.sort_values(by=('Words', 'All Films'), ascending=False)
pivoted = pivoted.reindex(order, axis=1)
# 需要的值：words
# 简易获取列
pivoted.loc['Hobbit']
```

### category

```python
# create
pd.Series(list('abbccc')).astype('category')

# get_category
s.cat.categories

# description -> like string
# rename 
s.cat.categories = ["Group %s" % g for g in s.cat.categories]
s = s.cat.rename_categories({1: "x", 2: "y", 3: "z"})

# ordered
s.sort_values(inplace=True)
s = s.cat.as_ordered()
s = s.cat.set_categories([2, 3, 1], ordered=True)

```

### encode

```python
# convert type
new_date = series.astype('datetime64[ns, US/Eastern]')

# hot encode
cabin_df = pd.get_dummies(
    df[['Cabin']], columns=["Cabin"], prefix=["Cabin_Type"] 
)
df=df.join(cabin_df)

# lable encode
df.loc[:,"Pclass"] = df["Pclass"].astype('category')
df['Pclass_cat'] = df["Pclass"].cat.codes
```

### null 

```python
df.fillna(value=,inplace=True)
# 向上找非空
df.fillna(method='ffill') 
# notnull
df['name'].notnull()
# 判断
pd.isnull()
```
插值

### datetime

```python
# str to datatime
pd.to_datetime(format)
datetime.strptime(str,"%d%m%y,%H%M%S") 
# generate datatimes
dt.now()
dt.date(2005,2,14)
# standard
start_date = date + ' 09:00:00'
end_date = date + ' 15:00:00'
# get weekday
df_index.index[0].weekday()
# time to str
datetime.now().strftime("%H:%M:%S")
# time delta
delta.days
pd.Timedelta(1, unit="d")
pd.Timedelta(pd.offsets.Day(2))
pd.Timedelta(days=1)
# datestamp 对于单一的日期而言 生产 timestamp
pd.to_datetime('2020-08-01')
# 需加入转换成日期
start_date = pd.to_datetime('2020-08-01').date()
# 运算
start_date - pd.Timedelta(days=10)

# filter by year
final_df['report_date'] = pd.to_datetime(final_df['report_date'])
final_df['year'] = final_df.report_date.dt.year
```

### str

```python
df.str.upper()
```

### apply

```python
df.loc[:, 'A'] = df.loc[:, 'A'].apply(
    lambda x: 2 if np.isnan(x) else np.random.randint(2,8)
)
```

### I/O

```python
import os
base_path = os.path.abspath(os.path.join(__file__, os.pardir))

df = pd.read_excel(
    'a.xlsx',
    # index_col=None,
    # col
    header = None,
    # 数据类型
    converters={
        'names':str,
    }
)

pd.read_csv()
# set index as an independent column
df.to_csv(
    'a.csv',
    index=None,
    index_col=0,
)
# csv encoding 

# to_excel_sheet
with pd.ExcelWriter('a.xlsx') as writer:
    for i in a_list:
        df.to_excel(writer, sheet_name=i)

# read_sheet

xls = pd.ExcelFile(data_path)
for val in xls.sheet_names:
    df = pd.read_excel(xls,val)

```

## notice

### axis

1. 根据访问的顺序 一维 axis = 0 二维 先列后行
2. calculate(axis) -> 沿着axis进行运算/插入

### view/replace

```python
# view 只代表copy
df[df.a > 5]['b']
# 赋值
df.loc[df.a > 5, 'b'] = 4
# 分成两段不改变原来的df
# join 不需要 inplace=true
```

### storage

在函数中调用所做的改变影响全局
等号只改变引用
在循环的调用中应使用df.copy()

```python
# series to df
a.to_frame()
pd.series(,index=df.columns,name=df.index)
df.append(list)
# list/numpy/dict to series/dataframe
series = pd.series(list)
df = pd.dataframe(dict,columns=[])
```
