---
title: 算法基本模板
date: 2022-07-04 11:51:49
tags: algorithm
---

# 模板

## 位置关系

### 相对位置

```c++
vi id(n), rid(n);

// 当前数组的id对应的变换数组的id
// id[x] = T_x;
// id[x]返回当前id对应的原id 1. 可用于改变原数列的值 2. 访问原序列的值 
rep (i, 0, n) id[i] = i;

// 变换数组当前的id对应的原数组的id
// rid[id[x]] = x (rid[T_x] = x) 
// 通常直接使用原数组 + id 表示 Tarr 所以通常不需要

// 记录T变换后id的映射 后 - 前
rotate(id.begin(), id.begin() + x, id.end());
// sort 
sort(all(id), [](auto &a, auto &b) {
    return g[a] < g[b];
});
// 0 -> pos + i
rep (i, 0, n) {
	id[i] = (pos + i) % 3;    
}

// 按原id输出
vv[id[0]] = v[id[0]];
vv[id[2]] = v[id[2]] + v[id[0]];
vv[id[1]] = accumulate(all(v), 0);
```

### 排列

```c++
// 若只能交换一次
// 1 2 2 3 4 5 6
// 直接比较原来的排列
// 1 3 2 2 4 5 6
// 一定代表着不同的部分
```

### 判断个数/距离

转换区间: (i, n) 的个数 -> [i + 1, n - 1]  == b - a + 1

转换坐标 逆序坐标 x -> 正序坐标 n - x + 1

while if (match) j++ : (i, j)

注意 for(;;j++) x for(;;)

## Sort

topk 问题

```c++
// c++ greater means different sort 从大到小， priority 小顶堆
struct btmp{
    bool operator()(const pis &a, const pis &b){
        if(a.first < b.first) return true;
        else if(a.first > b.first) return false;
        else{
            if(a.second > b.second) return true;
            else return false;
        }
    }
};
```

### quicksort 

```c++
int partition(int arr[], int low, int high)
{
	int pivot = arr[high];
	int i = (low - 1);

	for (int j = low; j <= high - 1; j++)
	{
		if (arr[j] <= pivot) {
			i++;
			swap(arr[i], arr[j]);
		}
	}
    // 替换到交界的位置 
	swap(arr[i + 1], arr[high]);
	return (i + 1);
}

int partition_r(int arr[], int low, int high)
{
	srand(time(NULL));
	int random = low + rand() % (high - low);
    // 与最高位交换即可
	swap(arr[random], arr[high]);
	return partition(arr, low, high);
}

void quickSort(int arr[], int low, int high)
{
    // 拆分问题
	if (low < high) {
		// 排序
        int pi = partition_r(arr, low, high);
		quickSort(arr, low, pi - 1);
		quickSort(arr, pi + 1, high);
	}
}

```

### midsort

逆序对问题

```c++
// 归并 
// low + (high - low + 1) / 2
void mergeSort(int arr[], int L, int R) {
	if (L == R){
		return;
	} else {
		int M = (L + R) / 2;
		mergeSort(arr, L, M);
		mergeSort(arr, M + 1, R);
		merge(arr, L, M + 1, R);
    }
}
// create left arr 
const int l = mid - left + 1;
const int r = right - mid;
// Create temp arrays
int *left = new int[l],
	*right = new int[r];
// combine arrs
int ll = 0, rr = 0;
while (ll < l && rr < r);
// 防止遗漏
while (ll < l) while(rr < r);
```

### heapsort

```c++
void heapify(int size, int i){
	// 最后一个非叶子节点的位置 2x -> 左节点 2x+1 -> 右节点
	int l = 2 * i + 1; 
    int r = 2 * i + 2;
    int largest = i;
    if (l < size && hT[l] > hT[largest])
		largest = l;
	if (r < size && hT[r] > hT[largest])
		largest = r;
	if (largest != i) {
        // 自顶而下调整
        swap(&hT[i], &hT[largest]);
		heapify(size, largest);
  	}
}
// heap sort 堆顶替换，重建堆
void heapSort(int size)
{
    // 建堆（从最后一个非叶子节点向上）
    // size 2n + 2 / 2n + 3
    for(int i = size / 2 - 1; i >= 0; i--) {
        heapify(size, i);
    }
    // 堆排序
    for(int i = size - 1; i >= 1; i--) {
        // 将当前最大的放置到数组末尾
        swap(arr[0], arr[i]);
        // 将未完成排序的部分继续进行堆排序
        heapify(i, 0);             
    }
}
```

### 插入排序

```c++
// 部分sort
// 注意n - 1次
```



### 基数排序

radix sort

```c++
// 先解决子问题 个位数的排序问题
void countSort(int arr[], int n, int exp) {
    int output[n]; 
    int i, count[10] = {0};
 
    // 基于每个位数的分布
    for (i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;
 	
    // 真实的位置映射
    for (i = 1; i < 10; i++)
        count[i] += count[i - 1];

    // 按顺序赋值
    for (i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }

    for (i = 0; i < n; i++)
        arr[i] = output[i];
}

// Radix Sort
void radixsort(int arr[], int n) {
	int m = *max_element(arr, arr + n);
    // 枚举每一位的顺序
    for (int exp = 1; m / exp > 0; exp *= 10)
        countSort(arr, n, exp);
} 
```

### bubble sort

number of inversion pairs
排序过程，每次纠正逆序对 in-place 原地排序 直到没有
线段树计算逆序对，贪心构造最大逆序对 

```c++
vi bubbleSort(vi &arr) {
     if (sz(arr) <= 1) {
          return arr;
     }
    
    //记录最后一次交换的位置
    int lastExchangeIndex = 0;
    // 无序数列的边界，每次比较只需要比到这里为止
    int sortBorder = sz(arr) - 1;
    
    for (int i = 0; i < arr.length - 1; i++) {
         bool isSorted  = true; //有序标记，每一轮的初始是true
         for (int j = 0; j < sortBorder; j++) {
             if (arr[j + 1] < arr[j]) {
                 isSorted  = false; //有元素交换，所以不是有序，标记变为false
                 int t = arr[j];
                 swap(arr[j], arr[j + 1]);
                 lastExchangeIndex = j;
             }
         }
		 sortBorder = lastExchangeIndex;
         //一趟下来是否发生位置交换，如果没有交换直接跳出大循环
         if(isSorted)
              break;
     }
     return arr;
}
```

### 选择排序

每次遍历选择一位，最大位 swap

### cycle sort

swap cycle

[交换次数](https://blog.csdn.net/yunxiaoqinghe/article/details/113153795)

<img src="/images/swap-1.png" alt="swap" style="zoom: 67%;" />

若存在一个圈有两个相同的值，可以通关交换增加环的个数
[圈排序](https://www.cnblogs.com/kkun/archive/2011/11/28/2266559.html) 不断寻找直到遇到需要替换到原来位置的元素

补充说明： ？是否一定成环 - ? 可能提前成环 a->b->c->b 随便搜索可能找不到一个可以回到A的回路 b->c->b 作为一个子环。a->b->d->a 才是真实的环 -> 至多搜索6次 -> 不能直接删除, 找到环后结束搜索。 链越短越好? 

<img src="/images/swap-2.png" alt="image-20220426173644799" style="zoom:67%;" />

### 计数排序

利用大空间，直接存储到值对应的位置，顺序输出。

## 结构

### 双向链表

```c++
// 直接调用
class TextEditor {
    list<char> lst;
    list<char>::iterator cur;

    string print() {
        string ret;
        auto it = cur;
        for (int i = 0; i < 10; i++) {
            if (it == lst.begin()) break;
            it = prev(it);
            ret.push_back(*it);
        }
        reverse(ret.begin(), ret.end());
        return ret;
    }

public:
    TextEditor() {
        cur = lst.begin();
    }
    
    void addText(string text) {
        for (char c : text) lst.insert(cur, c);
    }
    
    int deleteText(int k) {
        int ret = 0;
        while (k && cur != lst.begin()) {
            cur = prev(cur);
            cur = lst.erase(cur);
            k--; ret++;
        }
        return ret;
    }
    
    string cursorLeft(int k) {
        while (k && cur != lst.begin()) {
            cur = prev(cur);
            k--;
        }
        return print();
    }
    
    string cursorRight(int k) {
        while (k && cur != lst.end()) {
            cur = next(cur);
            k--;
        }
        return print();
    }
};


struct node {
    node *nxt = nullptr;
    node *pre = nullptr;
    char v;
    node(char _v) {
        v = _v;
    }
};

class TextEditor {
public:
    node *head, *cur;
    TextEditor() {
        // 设置哨兵
        head = new node('*');
        cur = head;
    }
    
    void addText(string text) {
        node *tmp = nullptr;
        if (cur && cur->nxt) tmp = cur->nxt; 
        for (int i = 0; i < text.size(); i++) {
            cur->nxt = new node(text[i]);
            cur->nxt->pre = cur;
            cur = cur->nxt;
        }
        if (tmp) {
            cur->nxt = tmp;
            tmp->pre = cur;
        }
    }
    
    int deleteText(int k) {
        node *f = 0;
        node* nn = nullptr;
        if (cur->nxt) {
            nn = cur->nxt;
        }
        int lk = k;
        while (cur->v != '*' && k) {
            cur->pre->nxt = nn;
            if (nn) {
                nn->pre = cur->pre;
            }
            cur = cur->pre;
            k--;
        }
        return lk - k;
    }

    string cursorLeft(int k) {
        int mm = 10;
        while (cur->v != '*' && k) {
            cur = cur->pre;
            k--;
        }
        string s = "";
        node *tmp = cur;
        while (tmp->v != '*' && mm) {
            s += tmp->v;
            tmp = tmp->pre;
            mm--;
        }
        reverse(s.begin(), s.end());
        return s;
    }
    
    string cursorRight(int k) {
        int mm = 10;
        while (cur->nxt != nullptr && k) {
            cur = cur->nxt;
            k--;
        }
        string s = "";
        node *tmp = cur;
        while (tmp->v != '*' && mm) {
            s += tmp->v;
            tmp = tmp->pre;
            mm--;
        }
        reverse(s.begin(), s.end());
        return s;
    }
};
```

### 十字链表 LFU

```c++
// LFU 缓存 frequency

// LRU least recentl
```



### 对顶栈

```c++
class TextEditor {
public: 
    stack<char> left, right;
    TextEditor() {}
    
    void addText(string text) {
        for (char c:text) left.push(c);
    }
    
    int deleteText(int k) {
        k = min(k, (int)left.size());
        for (int i = 0; i < k; i++) left.pop();
        return k;
    }

    string text() {
        string res;
        for (int i = 0, k = min((int)left.size(), 10); i < k; i++) {
            res.insert(res.begin(), left.top());
            left.pop();
        }
        addText(res);
        return res;
    }
    
    string cursorLeft(int k) {
        k = min(k, (int)left.size());
        while (k--) {
            right.push(left.top());
            left.pop();
        }
        return text();
    }
    
    string cursorRight(int k) {
        k = min(k, (int)right.size());
        while (k--) {
            left.push(right.top());
            right.pop();
        }
        return text();
    }
};
```

### set

```c++
auto p1 = prev(s1.lb(x));
if (arr[*p1] > arr[x]) {
    s1.insert(x); 
    for (auto p = next(s1.find(x)); p != s1.end(); p++) {
        int id = *p;
        if (arr[x] <= arr[id]) {
            dd.pub(id);      
        }
        else break;
    }
    rep (i, 0, sz(dd)) s1.erase(dd[i]);                      
}
```



### hash

1. ! hash collision, 也可通过设置两组哈希的trick实现
   生日悖论：365的空间装23组数据，出现哈希碰撞的概率超过1/2
   因此 MOD通常要远大于储存数据数的平方，且多采用质数。
2. 线性探测 / 两组哈希综合判断。
3. O(n^2) - 若允许n*log - 使用红黑树，较为稳定。

[string](#string_hash)

```c++
// is guaranteed to be at least 32767 %...

ll codec(ll x, ll y) {
    x += 1e9 + 5;
    y += 1e9 + 5;
    return (x << 32) + y;
}

void decode(const ll &v, ll &x, ll &y) {
    x = v >> 32;
    y = v & ((1ll << 32) - 1);
    x -= 1e9 + 5;
    y -= 1e9 + 5;
}

int gethash(int base, int mod) {
    int hashvalue = 0;
    for (const auto &x: temp) {
    // maybe exsit negative 
        hashvalue = 1ll * hashvalue * base % mod + (x + 101);
        hashvalue %= mod;
    }
    return hashvalue;
}
gethash(263, int(1e9) + 7);

// 树哈希 树的同构问题 若哈希值

// 随机哈希


// 线性探测
int mov(vector<int> &arr, int pos) {
    if (arr[pos] == 0) {
        arr[pos] = pos + 1;
        return pos + 1; 
    }
    arr[pos] = mov(arr, arr[pos]);
    return arr[pos];
}
```



## DP

### mask/map

```c++
// 1e6 * 30 * 26 -- 1e9
unordered_map<long long, long long> dp;
long long codec(int l, int r, int cur) {
    return l * 100100 + r*100 + cur;
}


// ！subset
// lowbit
int lowbit(int x) {
    return x & (-x);
}

for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // sub...
}
// 状态压缩枚举子集
// 注意 ^ 是在arr[i] 完全包含时才代表子集，否则会影响值
for (int i = 0; i < N; i++) {
    for (int j = mask - 1; j > -1; j--) {
        dp[j] = min(dp[j], dp[j & (j ^ arr[i])] + 1);
    }
}

// 采用后向定义的方式更为高效
for(int i = 1 ; i < n ; i ++){
    for(int j = 0 ; j < 21 ; j ++){
        if(!(i >> j & 1)) continue ;
        for(int k = 0 ; k < 21 ; k ++) {
            // 右移 & 1, 防止重复更新
            if(!g[j][k] || (i >> k & 1)) continue;
            // 跳过 i + (1 << k)
            dp[i + (1 << k)][k] += dp[i][j];
        }
    }
}
```

### path

```c++
// 二维背包路径 - 不同于一维
for (int i = 1; i <= n; i++) {
    for (int j = target; j > -1; j--) {
        // 注意不同于一维背包的省略
        dp[i][j] = dp[i - 1][j];
        if (j >= res[i - 1])   
            dp[i][j] = max(dp[i][j], dp[i - 1][j - res[i - 1]] + res[i - 1]);
    }
}
```

### 记忆化

```c++
// 记忆化注意使用void
if (!dp[l][j - 1].size()) {
    dfs(s, l, j - 1);
}
// n^2 + l - r遍历 == n^3
```

### 环

<img src="/images/circle-1.png" alt="image-20220326223751746" style="zoom:50%;" />

## 博弈论

### IGC博弈

经典的Bash, Wythoff 以及Nim博弈问题, 都属于所谓的公平组合博弈(Impartial Combinatorial Games, ICG), ICG具有的的特征/性质如下(用局势(position)描述游戏中的一个状态):

<img src="/images/game-1.png" alt="image-20220329101921911" style="zoom: 67%;" />

枚举分析, 转化状态, 找规律：

#### 枚举状态

剩下3堆石子
（1,1,k）、（1,k,k）和（k,k,k）都是必胜态【都可以留下（k,k）必败态给对手】，
接下来对于任一个（a,b,c）都可以转化为（k+m, k+n, k+p）
而对于m\n\p，有3种情况，分别是
① 三者相等，就是（k’,k’,k’），为必胜态。
② 两者相等, 这样把k+m取完，留下必败态给对手，也是必胜态。
③ 三者不等，这种情况非常复杂，用简单的公式难以表达，我们可以观察到（1,2,3）是必败态，但是（1,2,4）是必胜态，两者只是相差一个石子。

#### 推理

1. ? 异或的规律 
2. 总能从先手必胜态->后手必败态
3. 反证矛盾, 先手当前状态不可能失败

### 极大极小

MIN_MAX  


lq - 异或序列

1. 从高位bit开始, bit == 1 直接获胜
2. bit 为奇数，且总数为奇数 - 胜利
3. ! bit为奇数，总数为偶数 - 失败 (可以选择其他，知道不得不选)

## 数论

### 误差分析

** l-2117 abbreviating-the-product-of-a-range 误差分析
<img src="/images/error.png" style="zoom: 50%;" />

乘法转对数，利用double可以自动四舍五入

### 组合

一步dp  
1  
1 1  
1 2 1  
1 3 3 1  

回推状态转移 映射到杨辉三角中  
通过杨辉三角一次向右逆向展开，也就得到了杨辉三角上一列和的表达式  


$$
    \sum_{i = 0} ^{k} C_{n + i}^n = C_{}
$$


```c++
const int maxn = 61;
long long C[maxn][maxn] = {0};
void make_c() {
    C[0][0] = 1;
    for (int i = 1; i <= maxn; i++) {
        C[i][0] = 1;
        for (int j = 1; j <= maxn; j++) {
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j];
        }
    }
}

// lucas定理 
// mod = 1e5 时  
LL fact[maxn+5];
LL a[maxn+10];
LL inv[maxn+10];
void init(){
    a[0] = a[1] = 1;
    fact[0] = fact[1] = 1;
    inv[1] = 1;
    for(int i = 2; i <= 100005; i++)
    {
        fact[i] = fact[i-1] * i % mod;
        inv[i] = (mod - mod/i)*inv[mod%i]%mod;
        a[i] = a[i-1] * inv[i] % mod;
    }
}

LL C(int n, int m){
    return fact[n]*a[n-m]%mod*a[m]%mod;
}

```

### 逆元

```c++
// rsa 解密 求乘法逆元
// 辗转相除
void exgcd(int a, int b, int& x, int& y) {
  	if (b == 0) {
    	x = 1, y = 0;
    	return;
  	}
    // x = y, y = x - a / b * y;
  	exgcd(b, a % b, y, x);
  	y -= a / b * x;
}

// 32 to 127 chr
// 加 mod
e = (x % m + m) % m;

```

### 质因子

```c++
// C++ Version
int euler_phi(int n) {
	int ans = n;
    // 注意i = 2
	for (int i = 2; i * i <= n; i++)
		if (n % i == 0) {
		ans = ans / i * (i - 1);
		while (n % i == 0) n /= i;
    }
	if (n > 1) ans = ans / n * (n - 1);
	return ans;
}
```

### 大数运算

#### 大整数

大数除法 - 大数乘法 (FFT?)

```c++
// 注意'1'而非 1
if (mid == 0 && a[mid] == '1') {
}

// 大整数加减法 大数 - 小数
// carry 表示借位
int carry = 0;
for (int i = A.size() - 1; i >= 0; --i) {
    // 减去借位 加法则加入，注意最后会多一位
    int tmp = A[i] - carry;
    // 注意越界
    if (i < B.size()) tmp = tmp - B[i];
	// 纠正负数
    ans.push_back((tmp + 10) % 10);
    if (tmp < 0)  carry = 1;
	else carry = 0;
}

// 如果高位都是0，则要将这些前导0都要删掉，如果最后结果就是0，则最后一个0不能弹出
// 加法注意添加1
while (ans.size() > 1 && ans.back() == 0) {
    ans.pop_back();
}

// 大整数乘除法 
// 乘法 v * b 判断b==0, 记录进位 
// 多项式fft - 二分...
for( i = 0; i < len1; ++ i) {
    int b = 0;
    for(int j = 0; j < len2 || b; ++ j) {
        // 注意初始化0
        int t = ans[i + j] + str1[i] * str2[j] + b;
        ans[i + j] = t % 10;
        // 进位
        b = t / 10;
    }
    len = i+j-1  //最终的位数
}

// r为余数 最后一起去除前导零（！非前导需保留）
// 竖式除法
r = 0;
for (int i = 0; i < A.size(); i++){
    // 生成新数
    r = r * 10 + A[i];
    // 除前导0都要保留
    q.push_back(r / b);
    // 保留余数
    r = r % b;
}
// 前导零
reverse(q.begin(), q.end());
while (q.size() > 1 && q.back() == 0) {
    q.pop_back();
}

// 大整数减法优化
// 二分估计 log2大整数 - 位数N 
// 记录相减，注意位数的对其 通过补0
int SubStract( int *p1, int *p2, int len1, int len2 ){}
// 将除数扩大，使得除数和被除数位数相等
for ( i=len1-1; i>=0; i-- ) {
    if ( i>=nTimes )
        num_b[i] = num_b[i-nTimes];
    else                     
        num_b[i] = 0;
}
// 重复调用，同时记录减成功的位数
for( j=0; j <= nTimes; j++) {
    // 相同位数减k次
	while((nTemp = SubStract(num_a,num_b + j,len1,len2 - j)) >= 0) {
        len1 = nTemp;
        // 每成功减一次，将商的相应位加1
		num_c[nTimes-j]++;
	}
}
```

#### 快速乘/幂

```c++
// ! extend gcd 不可以使用ull 存在负值 ull a > -1 恒成立
inline ull mul(ull a, ull b, ull mod){
    ull ans = 0;
    while( b > 0 ){
        if(b & 1) ans = (ans + a) % mod;
        a = (a + a) % mod;
        b >>= 1;
    }
    return ans;
}

ull quick_pow(ull a, ull b, ull mod) {
    ull res = 1;
    a %= mod;
    while(b) {
        if (b & 1) res = mul(res, a, mod);
        a = mul(a, a, mod); 
        b >>= 1;
    }
    return res;
}
```

### 素数筛

```c++
// 质数筛
const int maxn 100005;
int visit[maxn];
visit[0] = visit[1] = 1;
// 埃氏筛法, 合数
for (int i = 2; i <= maxn; i++) {
    if (!visite[i]) {
    	for (int j = i * i; j <= maxn; j += i) {
            visit[j] = 1;
        }
    }
}
// 欧拉筛法, 30 = 2*15, 3*10 可能被多次筛选 - 最小质因子 - 欧拉筛
int visit[maxn];
// 素数
int prime[maxn];
for(int i = 2; i <= maxn; i++) {
    if (!visit[i]) {
        // prime[0] 记录当前素数个数
        prime[++prime[0]] = i;
    }
    // prime[j] 表示第j个素数
    for (int j = 1; j <= prime[0] && i * prime[j] <= maxn; j++) {
        visit[i * prime[j]] = 1;
        // 一定不是最小质因子，break
        if (i % prime[j] == 0) {
            break;
        }
    }
}

// 三个公因子相乘的种类数
// factor n^3
// factor_num(i) + factor_num(a / i)
```

### 同余方程

(快速幂 + 快速乘)

cf-209 div2 D 遍历无线纸带  

1. 自反性，对称性，传递性, 线性运算， 幂运算

   <img src="/images/mod-1.png" alt="image-20220331155354746" style="zoom:50%;" />

   $a \equiv b \pmod{m} ⟹ a^n \equiv b^n\pmod{m}$

<img src="/images/mod-2.png" alt="image-20220331151356347" style="zoom: 67%;" />

具体解法

<img src="/images/mod-3.png" alt="image-20220331151512291" style="zoom:67%;" />

<img src="/images/mod-4.png" alt="image-20220331155606327" style="zoom:50%;" />

l-974 subarrays sums divided by k  
modulus = (sum % k + k) % k(c++)  

```c++
// a mod b = a - y [x / y] (x)
int mod(int a, int b) {
    return (a % b + b) % b;
}

inline ull mul(ull a, ull b, ull mod){
    ull ans = 0;
    while( b > 0 ){
        if(b & 1) ans = (ans + a) % mod;
        a = (a + a) % mod;
        b >>= 1;
    }
    return ans;
}

ull quick_pow(ull a, ull b, ull mod) {
    ull res = 1;
    a %= mod;
    while(b) {
        if (b & 1) res = mul(res, a, mod);
        a = mul(a, a, mod); 
        b >>= 1;
    }
    return res;
}

int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

// rsa 解密 求乘法逆元
// 辗转相除
void exgcd(int a, int b, int& x, int& y) {
  	if (b == 0) {
    	x = 1, y = 0;
    	return;
  	}
    // x = y, y = x - a / b * y;
  	exgcd(b, a % b, y, x);
  	y -= a / b * x;
}

// 32 to 127 chr
// 加 mod
e = (x % m + m) % m;

// C++ Version
int euler_phi(int n) {
	int ans = n;
    // 注意i = 2
	for (int i = 2; i * i <= n; i++)
		if (n % i == 0) {
		ans = ans / i * (i - 1);
		while (n % i == 0) n /= i;
    }
	if (n > 1) ans = ans / n * (n - 1);
	return ans;
}

int phi[MAXN];
void init(int n) {
    for (int i = 1; i <= n; i++)
        // 除1外没有数的欧拉函数是本身，所以如果phi[i] = i则说明未被筛到
        phi[i] = i;
    for (int i = 2; i <= n; i++)
        if (phi[i] == i) // 未被筛到
            for (int j = i; j <= n; j += i) // 所有含有该因子的数都进行一次操作
                phi[j] = phi[j] / i * (i - 1);
}
```

 阶乘/因子

取log long double求阶乘的大小

<img src="/images/factor-1.png" alt="image-20220325120510677" style="zoom:50%;" />

```c++
// 朴素法
// C++ Version
list<int> breakdown(int N) {
	list<int> result;
	for (int i = 2; i * i <= N; i++) {
		if (N % i == 0) {  // 如果 i 能够整除 N，说明 i 为 N 的一个质因子。
			while (N % i == 0) N /= i;
			result.push_back(i);
		}
	}
  	if (N != 1) {  // 说明再经过操作之后 N 留下了一个素数
    	result.push_back(N);
	}
	return result;
}
// 求欧拉函数
// C++ Version
int euler_phi(int n) {
	int ans = n;
	for (int i = 2; i * i <= n; i++)
    	if (n % i == 0) {
            // ans - ans / i
        	ans = ans / i * (i - 1);
        while (n % i == 0) n /= i;
    }
    // 减去自身，1不需要减
  	if (n > 1) ans = ans / n * (n - 1);
  	return ans;
}
```

l-29 divide two integers  
cannot use *, /, mod  
divisor multiply - dividend  

08.05 recursively multiply  
64 1 + ... + n  
&& replace if  
repeat replace for  
if b & 1 A + A res += A  

l-371 sum of two integer  
carry = a & b shift left  
while(carry != 0) 

l-369 valid perfect square  
(n + 1)^2 - n^2 = 2n + 1(culmulative)  
f(x) = x^2 - n^2 

## 图

### 欧拉

l-332 reconstruct itinerary  
seven bridge problem solved by Euler  
in degree = out degree(except S/E)  
? visited pop_back()  
dfs(pop()), res.push_back(),reverse  
the last number to end the search is last node  

l-753 cracking the safe  
? state not be visited   
? how to visit n numbers  
: set up a rule -- 0 - k 所有未经历过的状态

```c++
// 判断

// 无向图 ！有向图不满足
// 0 - 2个奇数点为欧拉路径
// 欧拉回路 皆为偶数点

// 有向图 欧拉路径
void dfs(const string& curr) {
    while (vec.count(curr) && vec[curr].size() > 0) {
        string tmp = vec[curr].top();
        vec[curr].pop();
        dfs(move(tmp));
    }
    stk.emplace_back(curr);
}


```

prove:  
each node has k in and out degree : Euler Path  
if no way out, go back to the node  
then find a new node  

```python
# 1、建邻接表adj、入度表indeg、出度表outdeg，省略...
# 2、判断是否存在
# 连通性 - 利用并查集 (除去孤立的节点)
# 回路无奇数度
# 3、dfs求解欧拉路径
ans = []
def dfs(node):
    while adj[node]:
		// 利用pop()
        v = adj[node].pop()
        dfs(v)
        ans.append([node, v]) # 循环里记录结果 循环外则为回路
dfs(start)
            
# 4、最后再逆回来
return ans[::-1]
```

### BFS

```c++
struct node {
    int x, y;
    node (int _x, int _y) {
        x = _x, y = _y;
    }
};
vvi g;
vvi dir = {{1, 0}, {0, -1}, {0, 1}, {-1, 0}};
int n, m;
bool check(int x, int y) {
    return (0 <= x && x < n && 0 <= y && y < m && g[x][y] != 0); 
}

int bfs(int x, int y, int tx, int ty) {
    vvi vis(n, vi(m, 0));
    queue<node> q;
    q.push(node(x, y));
    vis[x][y] = 1;
    int cnt = 0;
    if (x == tx && y == ty) return 0;
    while(q.size()) {
        int nn = q.size();
        for (int i = 0; i < nn; i++) {
            node v = q.front();
            q.pop();
            x = v.x, y = v.y;            
            for (int j = 0; j < 4; j++) {
                int xx = x + dir[j][0], yy = y + dir[j][1];
                if (check(xx, yy)) {
                    if (xx == tx && yy == ty) return cnt + 1; 
                    if (!vis[xx][yy]) {
                        q.push(node(xx, yy));
                        vis[xx][yy] = 1;
                    }
                }
            }
        }
        cnt++;
    }
    return -1;
}

queue<tuple<int, int, int>> q;
//  pre-place start nodes;
while (!q.empty()) {
    auto [u, mask, dist] = q.front();
    q.pop();
    if (mask == (1 << n) - 1) {
        ans = dist;
        break;
    }
    // 搜索相邻的节点
    for (int v: graph[u]) {
        // 将 mask 的第 v 位置为 1
        int mask_v = mask | (1 << v);
        // seen prevent repeated traversals
        if (!seen[v][mask_v]) {
            q.emplace(v, mask_v, dist + 1);
            seen[v][mask_v] = true;
        }
    }
};

```

### 拓扑

```c++
// l-1857 判环
// degree[i] <= 1
// in[i] <= 0

while (!q.empty()) {
    // 记录点数
    ++found;
    int u = q.front();
    q.pop();
    // 将节点 u 对应的颜色增加 1
    ++f[u][colors[u] - 'a'];
    // 枚举 u 的后继节点 v
    for (int v: g[u]) {
        --indeg[v];
        // 将 f(v,c) 更新为其与 f(u,c) 的较大值
        for (int c = 0; c < 26; ++c) {
            f[v][c] = max(f[v][c], f[u][c]);
        }
        // 无向图indeg[v] == 1
        if (!indeg[v]) {
            q.push(v);
        }
    }
}

if (found != n) {
    return -1;
}

for (int i = 0; i < n; ++i) {
    auto edge = edges[i];
    int node1 = edge[0], node2 = edge[1];
    if (parent[node2] != node2) {
        conflict = i;
    } else {
        // record 
        parent[node2] = node1;
        if (uf.find(node1) == uf.find(node2)) {
            cycle = i;
        } else {
            uf.merge(node1, node2);
        }
    }
}

// onstack 判环
void dfs(int i){
	onstk[i]=vis[i]=true;
	for (auto it:al[i]){
		if (onstk[it]) cyc=true;
		if (!vis[it]) dfs(it);
	}
	onstk[i]=false;
}
```

### dfs路径

```c++
// !记录路径
// codec unordered_map<int, int> 两点确定一条直线
// 判断transfer

void dfs(int k) {
	visit[k] = 1;
    // 记录当前的路径
	path[m++] = k;
	for (auto i:graph[k]) {
        if (visit[i] == 0) {
            dfs(i);
        }
        if (visit[i] == 1) {
            for (int j = m - 1;; j--) {
                if (path[j] == i) break;
            }
        }
	}
	visit[k] = 2;
    // 注意回退
	m--;
}

// 无向图
void dfs(int v) {
    path[cnt++] = v;
    vis[v] = 1;
    for (auto &vv:g[v]) {
        // 防止重复
        if (vv == last) continue;
        if (vis[vv] == 2) continue;
        if (vis[vv] == 1) {
            cycle = 1;
        }
        else {
            last = v;
            dfs(vv);
        }
    }
    vis[v] = 2;
}
```

### 判断直径

```c++
// 第一次dfs确认最远端的顶点
// 选任一远端顶点再次遍历
void dfs1(int v, int h) {
    vis[v] = 1;
    if (h > mh) {
        mh = h;
        tmp.clear();
        tmp.pub(v);
    }
    else if (h == mh) {
        tmp.pub(v);
    }
    for (auto &vv:g[v]) {
        if (!vis[vv]) {
            dfs1(vv, h + 1);
        }
    }
}

memset(vis, 0, sizeof(vis));
dfs1(0, 1);
int nxt = tmp[0];
rep (i, 0, sz(tmp)) s.insert(tmp[i]);
memset(vis, 0, sizeof(vis));
dfs1(nxt, 1);
rep (i, 0, sz(tmp)) s.insert(tmp[i]);
for (auto &i:s) cout << i + 1 << endl;
```

### 并查集

```c++
// 并查集
int find(int i){
    if(u[i] != i){
        u[i] = find(u[i]);
    }
    return u[i];
}

void unionn(int a, int b){
    int ra = find(a);
    int rb = find(b);
    if(ra != rb){
        if(sz[ra] > sz[rb]){
            swap(ra, rb);
        }
        u[ra] = rb;
        sz[rb] += sz[ra];
    }
}
```

### 最短路

```c++
// dijstra 
// 一次完成一次节点的更新，可使用priority queue优化
// 每次找到距离最近的节点，无法再被更新
// 若增加相同距离cost的优化 cost[cur] 已经无法再被优化 
const int N=1010;
const int INF=0x3f3f3f3f;
vector<int> adj[N];
int n,score[N][N],vou[N][N];
int d[N],vis[N],w[N],pre[N];

void dijkstra(int s) {
    fill(d,d+N,INF);
	fill(vis,vist+N,0);
	fill(w,w+N,0);
	d[s] = 0;
    // n个节点
	for(int i=0; i<=n; i++) {
		int u=-1, MIN=INF;
		for(int j=0; j<=n; j++) {
			if(!vis[j]&&d[j]<MIN) {
				u=j;
				MIN=d[j];
			}
		}
		if(u==-1) return;
		vist[u]=true;
		for(int x=0; x < adj[u].size(); x++) {
			int v=adj[u][x];
			if(!vist[v]) {
				if(d[u]+score[u][v]<d[v]) {
					d[v]=d[u]+score[u][v];
					w[v]=w[u]+vou[u][v];
					pre[v]=u;
			}
		}
	}
}

// dijstra 聚点 + 邻接表 N + 1个顶点
for(int i=0;i<N;++i){
    if(inDegree[i]==0){
        Adj[N].push_back(i);
        zeroDegree.insert(i);
    }
}

// 找到相同
// INT_MAX溢出
if (dist[node] != dist[tmp[i]])
	return false;

// floyd
for(int k = 0; k <= n; k ++ ){
	for(int i = 0; i <= n; i ++ ){
		for(int j = 0; j <= n; j ++ ){
			if(g[i][k]!=inf&&g[k][j]!=inf)
				g[i][j] = min(g[i][k]+g[k][j],g[i][j]);
            }
        }
    }
}

// dfs 回溯路径 -> 多目标
// pair<int, int> 历史的最大的需要带的累积
rep (i, 0, n) {
    if (!vis[i] && w[id][i] != INF) {
        if (w[id][i] + dis[id] < dis[i]) {
            dis[i] = w[id][i] + dis[id];
            fa[i].clear();
            cv[i].clear();
            for (auto &vv:cv[id]) {
                fa[i].pub(id);
                cv[i].pub(vv + c / 2 - cc[i]);
            }
        }
        else if (w[id][i] + dis[id] == dis[i]) {
            for (auto &vv:cv[id]) {
                fa[i].pub(id);
                cv[i].pub(vv + c / 2 - cc[i]);
            }
        }
    }
}


void dfs(int v) {
    temppath.push_back(v);
    if(v == 0) {
        int need = 0, back = 0;
        for(int i = temppath.size() - 1; i >= 0; i--) {
            int id = temppath[i];
            if(weight[id] > 0) {
                back += weight[id];
            } else {
                if(back > (0 - weight[id])) {
                    back += weight[id];
                } else {
                    need += ((0 - weight[id]) - back);
                    back = 0;
                }
            }
        }
        if(need < minNeed) {
            minNeed = need;
            minBack = back;
            path = temppath;
        } else if(need == minNeed && back < minBack) {
            minBack = back;
            path = temppath;
        }
        temppath.pop_back();
        return ;
    }
    for(int i = 0; i < pre[v].size(); i++)
        dfs(pre[v][i]);
    temppath.pop_back();
}

// 0 - 1 bfs
while (sz(q)) {
    int tt = q.front();
    q.pop();
    if (tt == b) break;
    vis[tt] = 1;
    rep (i, 0, sz(g[tt])) {
        int line = id[tt][i];
        int tar = g[tt][i];
        node nn(line, tt);
        int sign = 1;
        rep (i, 0, sz(par[tt])) {
            if (line == par[tt][i].line) {
                sign = 0;
                break;
            }
        }
        if (dis[tar] > dis[tt] + 1) {
            par[tar].clear();
            dis[tar] = dis[tt] + 1;
            par[tar].pub(nn);
            ex[tar] = ex[tt] + sign;
            q.push(tar);
        }
        else if (dis[tar] == dis[tt] + 1) {
            int ww = ex[tt] + sign;
            if (ww == ex[tar]) {
                par[tar].pub(nn);
            }
            else if (ww < ex[tar]) {
                par[tar].clear();
                par[tar].pub(nn);
                ex[tar] = ww;
            }
            q.push(tar);
        }
    }
}

// A*

```

### MST/强连通

minimum weight spanning tree 使得权值最短的路

1. Kruskal

   ```c++
   // 从最小边开始加入
   // 并查集判断是否有环
   // 无环则加入
   
   sort(edgelist.begin(), edgelist.end());
   
   int ans = 0;
   
   for (auto edge : edgelist) {
       int w = edge[0], x = edge[1], y = edge[2];
       // take that edge in MST if it does form a cycle
       if (s.find(x) != s.find(y)) {
           s.unite(x, y);
           ans += w;
       }
   }
   ```

2. 强连通分量 tarjan

### 网络流问题

源点：有n个点，有m条有向边，其中有一个点比较特殊，它只出不进，即入度为0。这样的点我们称为源点，一般用字母S表示。
汇点：另一个点也比较特殊，只进不出，即出度为0。这样的点我们称为汇点，一般用字母T表示。
容量和流量：每条有向边上有两个量，容量和流量，从i到j的容量表示为c[i,j]表示，流量则用f[i,j]表示。

模板1 最小费用最大流问题 
在最大流的基础上(全选...) 使得费用最小
模板2 二分图权值匹配 - 一一对应  

## 二分

1. 核心是判断f(x)的二元性（一部分相同 一部分不同）以及最快的求法
2. 注意边界的讨论，差值类问题a[l]和a[l - 1]同时考虑即可
3. ! 广义的规律

ls-37

<img src="/images/binary-1.png" alt="image-20220414201412729" style="zoom:50%;" />

直线满足顺序

### 二元性

```c++
// 计数

// 记录小于等于x的数值个数
auto pos = ub(all(v), x) - v.begin();
// 记录大于x的数值个数
sz(v) - pos;
// 记录小于x的数值个数 大于等于同理
auto pos = lb(all(v), x) - v.begin();

// 插入使得数组递增 - 在第一个不大于x的位置上插入 - 本来的意义
arr.insert(pos, v); 
```

存在二元的规律即可

```c++
// 二分 注意边界的处理，若不存在想要找的值得情况。
while(left < right) {
    // 是否加一取决于是否收敛
    int mid = (left + right) / 2;
    // 不需要的结果
    if (nn[mid] < diff) {
        left = mid + 1;
    }
    else {
        right = mid;
    }
}
// lower bound first element not less than i; 
// upper bound first element greater than i; greater<int> 则相反
auto lower = lower_bound(data.begin(), data.end(), i);
if (lower != data.end()) int pos = lower - data.begin();
```

## 贪心

!注意多状态的特性  
只考虑了存在一种可能AC由于AB，但没有考虑到BC的整体情况
总出现在相同的两列 - 点集中斜率的最大值

<img src="/images/greedy01.png" alt="image-20220414201526887" style="zoom:50%;" />  

只需要考虑 a+=lowbit(a)

局部贪心 diff 只有在遇到B是更新  

## 树

### 堆

```c++
void heapify(int size, int i){
	// 最后一个非叶子节点的位置 2x -> 左节点 2x+1 -> 右节点
	int l = 2 * i + 1; 
    int r = 2 * i + 2;
    int largest = i;
    if (l < size && hT[l] > hT[largest])
		largest = l;
	if (r < size && hT[r] > hT[largest])
		largest = r;
	if (largest != i) {
        // 自顶而下调整
        swap(&hT[i], &hT[largest]);
		heapify(size, largest);
  	}
}
// heap sort 堆顶替换，重建堆
void heapSort(int size)
{
    // 建堆（从最后一个非叶子节点向上）
    // size 2n + 2 / 2n + 3
    for(int i = size / 2 - 1; i >= 0; i--) {
        heapify(size, i);
    }
    // 堆排序
    for(int i = size - 1; i >= 1; i--) {
        // 将当前最大的放置到数组末尾
        swap(arr[0], arr[i]);
        // 将未完成排序的部分继续进行堆排序
        heapify(i, 0);             
    }
}
```

### multiset

```c++
// multiset 使用 prev()
auto check = [&](int mid) -> bool {
    int p = pills;
    // 工人的有序集合
    multiset<int> ws;
    for (int i = m - mid; i < m; ++i) {
        ws.insert(workers[i]);
    }
    // 从大到小枚举每一个任务
    for (int i = mid - 1; i >= 0; --i) {
        // 如果有序集合中最大的元素大于等于 tasks[i]
        // rbegin() 不行
        if (auto it = prev(ws.end()); *it >= tasks[i]) {
            ws.erase(it);
        }
        else {
            if (!p) {
                return false;
            }
            auto rep = ws.lower_bound(tasks[i] - strength);
            if (rep == ws.end()) {
                return false;
            }
            --p;
            ws.erase(rep);
        }
    }
    return true;
};
```



### 二叉树

```c++
// 注意树的建图过程 子节点为0 需要排除父节点
// 相似的模式
// 基于一个二叉搜索树即推导 -> 难以证明

// AVL 左左 右右 左右 = 右右 + 左左
// 红黑树 Is It A Red-Black Tree？

// 有可能没有节点
// ！！！注意根节点的特殊情况
if (cur != 1 && graph[cur].size() == 1) {
    isleave = true;
}
else if (cur == 1 && graph[cur].size() == 0) isleave = true;
```

### bit树



树状数组

```c++
static int lowbit(int x) {
    return x & (-x);
}

// a[maxn]
void update(int x, int v) {
    // x += 1 若nums从0开始
    for(int i = x; i < maxn; i += lowbit(i))
        c[i] += v;
}
int getsum(int x) {
    int sum = 0;
    for(int i = x; i >= 1; i -= lowbit(i))
        sum += c[i];
    return sum;
}	
int sumRange(int i, int j) {
    // i + 1 到 j + 1;
    return sum[j + 1] - sum[i];
}
```

线段树

l-307 range sum query  
[solutions](https://zhuanlan.zhihu.com/p/92920381)  
sqrt(n) blocks(known length)  
binary indexed tree(Fenwick tree)
对操作数进行累加 (前面所有的操作数) 而非数值本身

![image-20220307143054073](/images/bit-1.png)

l-1622 fancy-sequence  
inverse order - add all multall opt - ax + b  
combine opt 
使用数组快于vector

```c++
void operator += (const node &t){
    a = a * t.a%mod;
    b = (b * t.a + t.b)%mod;
}
```

```c++
// 线段树 完全二分树
// 2n - 4n
// 记录范围的完全二叉树, 类似于堆,注意节点
// 自顶而下的更新

// 动态开点
struct node {
    ll l, r, v = 0, vv = 0, lz = 0, llz = 0, is_c = 0;
}tree[4 * maxn];

void create_node(int cur) {
    if (tree[cur].is_c) return;
    tree[cur].is_c = 1;
    tree[cur].l = cnt++;
    tree[cur].r = cnt++;
}

void push_up(int cur) {
    tree[cur].v = tree[tree[cur].l].v + tree[tree[cur].r].v;
    tree[cur].vv = max(tree[tree[cur].l].vv, tree[tree[cur].r].vv);
}

// lazy_tag
void push_down(int cur, int lv, int rv) {
    int mid = (lv + rv) / 2;
    int ln = tree[cur].l, rn = tree[cur].r;
    tree[ln].lz += tree[cur].lz;
    tree[ln].v += tree[cur].lz * (mid - lv + 1);
    tree[rn].lz += tree[cur].lz;
    tree[rn].v += tree[cur].lz * (rv - mid);
    tree[cur].lz = 0;
    tree[ln].llz += tree[cur].llz;
    tree[ln].vv += tree[cur].llz;
    tree[rn].llz += tree[cur].llz;
    tree[rn].vv += tree[cur].llz;
    tree[cur].llz = 0;
}

void update(int cur, int lv, int rv, int l, int r, ll v) {
    create_node(cur);
    if (l <= lv && rv <= r) {
        tree[cur].v += v * (rv - lv + 1);
        tree[cur].lz += v;
        tree[cur].vv += v;
        tree[cur].llz += v;
        return;
    }
    push_down(cur, lv, rv);
    int mid = (lv + rv) / 2;
    if (l <= mid) {
        update(tree[cur].l, lv, mid, l, r, v);
    }
    if (mid < r) {
        update(tree[cur].r, mid + 1, rv, l, r, v);
    }
    push_up(cur);
}

ll query(int cur, int lv, int rv, int l, int r) { 
    create_node(cur);
    if (l <= lv && rv <= r) {
        return tree[cur].v;
    } 
    push_down(cur, lv, rv);
    int mid = (lv + rv) / 2;
    ll v1 = -1, v2 = -1;
    if (r <= mid) {
        v1 = query(tree[cur].l, lv, mid, l, r);
        return v1;
    }
    else if (l > mid) {
        v2 = query(tree[cur].r, mid + 1, rv, l, r);
        return v2;
    }
    v1 = query(tree[cur].l, lv, mid, l, r);
    v2 = query(tree[cur].r, mid + 1, rv, l, r);
    return v1 + v2;
}

ll qquery(int cur, int lv, int rv, int l, int r) { 
    create_node(cur);
    if (l <= lv && rv <= r) {
        return tree[cur].vv;
    }
    push_down(cur, lv, rv);
    int mid = (lv + rv) / 2;
    ll v1 = -1, v2 = -1;
    if (r <= mid) {
        v1 = qquery(tree[cur].l, lv, mid, l, r);
        return v1;
    }
    else if (l > mid) {
        v2 = qquery(tree[cur].r, mid + 1, rv, l, r);
        return v2;
    }
    v1 = qquery(tree[cur].l, lv, mid, l, r);
    v2 = qquery(tree[cur].r, mid + 1, rv, l, r);
    return max(v1, v2);
}
```

## 指针

### 滑动

```c++
// 滑动
while (i <= j, j < n) {
    if (a > tar) {
        ans = max(ans, val);
        j++;
    }
    else {
        i++;
        // 补集，不需要更新
        ans = max(ans, val); 
    }
}
```

### 链表数组

```c++
// 创建链表，或用map
const int MAXN=100010;
int bg,n,k;
struct node {
	int id,data,next;
} Node[MAXN];

vector<node> ans;

while(cpy != -1) {
    ans.push_back(Node[cpy]);
    cpy = Node[cpy].next;
} 
```

## String 

### Trie

```c++
// 可删除
struct TrieNode {
    string word;
    unordered_map<char, TrieNode *> children;
    TrieNode() {
        this->word = "";
    }   
};

// 同时判断isend
if (nxt->word.size() > 0) {
    res.insert(nxt->word);
    nxt->word = "";
}

// 遍历结束删除
if (nxt->children.empty()) {
    root->children.erase(ch);
}
```

### KMP

```c++
// 相反方向需要map
// 动态规划 - 前缀
vector<int> nxt(m);
for (int i = 1, j = 0; i < m; i++) {
    while(j > 0 && part[j] != part[i]) j = nxt[j - 1];
    if (part[j] == part[i]) nxt[i] = ++j;
}

// kmp匹配
while(l < n) {
    if (ns[l] == s[r]) {
        l++;
        r++;
    }
    else {
        res += r;
        while(r > 0 && ns[l] != s[r]) {
            r = pre[r - 1];
            res += r;
        } 
        if (r == 0 && ns[l] != s[r]) l++;
    }
    if (r == n) {
        //...
        r = pre[r];
    }

}
```

### string_hash

[hash](#hash)

字母的hash
(long long ) int(1e9 + 7) prime  base = 31    
l-1044 longest duplicate substring  

```c++
// 滑动哈希 长度为定值
long long mult = qPow(base, len - 1);
ha = ((ha - A[i - len] * mult % mod + mod) % mod * base + A[i]);

// 前缀哈希 提取一段距离 可以选择两组哈希防止冲突、
// 常用base 37 171 MOD 1e9 + 7
vector<long long> f(n + 1), P(n + 1);
for (int i = 1; i <= n; i++) f[i] = (f[i - 1] * 171 + s[i - 1]) % MOD;
P[0] = 1;
for (int i = 1; i <= n; i++) P[i] = P[i - 1] * 171 % MOD;
long long h = (f[i + mid - 1] - f[i - 1] * P[mid] % MOD + MOD) % MOD;

```

## Prob+

### entropy

[entropy](../view/prob.md#entropy) - as information (信息量) ！可能的输出 - 匹配可能的结果

[The Twelve-Coins Puzzles](https://www.av8n.com/physics/twelve-coins.htm)

1. calc the entropy(information) <= 实验的信息

2. 确保每一步实验后的信息量仍然满足上述条件，注意分堆后，保留上次称重的信息，只要选中一个砝码，就知道是更重的/更轻的，即使还没有选中，但此时只需要选出砝码的信息量即可。

3. transmit to a code -> the result table RRR RRB ...

4. 矛盾条件 若一个corn为RRB, 那么若他较轻，则会出现LLB的情况 

   even though it appears we have 27 codewords, this approach has no chance of handling more than 13 coins. 

   一一对应每一个硬币 - 假设实验为定值

<img src="/images/information-1.png" alt="image-20220326205757610" style="zoom:50%;" />

[twelve coin code](https://coady.github.io/posts/coin-balance/)  

### 编码

generate add 0 / add 1  
map(instead of recursive)  
l-1238 circulate from start  
$ i \quad xor \quad (i >> 1)\quad xor \quad start$  

1. if a ^ b = c ^ b  a == b  

2. a,b at most one bit different, res is still gray code 

3. num to grey - gray to num

  ```python
# num to gray 
i ^ (i >> 1)  
# gray to num 与n的每一位亦或 
res = n
while n > 0:  
	n >> = 1 
    res ^= n
# num to gray
  ```

### 组合

```c++
// ncr = (n - 1)Cr + (n - c)C(r - 1)
// 未选取特定元素的组合 - 选取了特定元素的组合
// ncr
long long C(int n, int r) {
    if(r > n - r) r = n - r; // because C(n, r) == C(n, n - r)
    long long ans = 1;
    int i;
    for(i = 1; i <= r; i++) {
        ans *= n - r + i;
        ans /= i;
    }
    return ans;
}

# define MAX 100 // assuming we need first 100 rows
long long triangle[MAX + 1][MAX + 1];

void makeTriangle() {
    int i, j;

    // initialize the first row
    triangle[0][0] = 1; // C(0, 0) = 1

    for(i = 1; i < MAX; i++) {
        triangle[i][0] = 1; // C(i, 0) = 1
        for(j = 1; j <= i; j++) {
            triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
        }
    }
}

long long C(int n, int r) {
    return triangle[n][r];
}
```

l-491 increasing subsequences  
check duplicate same value  
the former is selected and the latter is not x  
or with hash code  

** l-458 poor pigs  
combination C(i, j) = C(i - 1, j) + C(i - 1, j - 1);(add new i)  


### random

l-384 shuffle an array  
fishier-yates shuffle  
i(0 - n) j = i + rand()%(len - i) swap(i, j)  
each position  
P(not selceted) % P(selceted by jth)  
correctness proof  
has n! conditions(through condition probability)  
$$
P(x'(i) = b_i \quad \text{for 1 $\le$ i $\le$ n}) = \frac{1}{n!}
$$
motekalo  
count times in each pos  

## 几何

### K值

```c++
// 多次分类
// 归一化 + 第一个复数为0 ...
ll d1 = x1 - x2, d2 = y1 - y2;
ll sign = (d1 >= 0) ^ (d2 >= 0) ? -1 : 1;
ll fac = __gcd(abs(d1), abs(d2));
ll x = sign * abs(d1)/fac, ll y = abs(d2)/fac;

if (x == 0) {
    y = 1;
} else if (y == 0) {
    x = 1;
} else {
    if (y < 0) {
        x = -x;
        y = -y;
    }
    // 提高精度
    int gcdXY = gcd(abs(x), abs(y));
    x /= gcdXY, y /= gcdXY;
}

// 防止溢出
ll sign = (d1 ^ d2) >= 0 ? 1 : -1;
// -1 0 1 0 同属于一种 ！0的正负性单独讨论
sign = (d1 == 0 || d2 == 0) ? 1 : sign;
ll fac = __gcd(abs(d1), abs(d2));
ll x = sign * abs(d1)/fac, y = abs(d2)/fac;

// k1 * b2 == k2 * b1 判断平行
// (x1 - x0)(y3 - y2) = (y1 - y0)(x3 - x2);
// ax + by + c = 0 -> a1 * b2 = a2 * b1 c
// y - y1 = (y2 - y1)/(x2 - x1) * (x - x1)
```

```c++
M_PI
double eps = 1e-6;
// 向量
struct V {
    double x, y;
    V() : x(0), y(0) {}
    V(double a, double b) : x(a), y(b) {}
};

// 常见运算符
inline V operator * (const double &x,const V &a){return (V){a.x*x,a.y*x};}
// 点积、叉积 |a|*|b| cos / sin(可代表面积)
inline double operator * (const V &a,const V &b){return a.x*b.x+a.y*b.y;}
inline double operator ^ (const V &a,const V &b){return a.x*b.y-a.y*b.x;}

// 相等
inline bool operator == (const V &a,const V &b){return abs(a.x-b.x)<eps&&abs(a.y-b.y)<eps;}
inline bool operator != (const V &a,const V &b){return !(a==b);}

// 长度
inline double len(const V &a){return sqrt(a.x*a.x+a.y*a.y);}

// 角度
// 两向量与原点的夹角
inline double angle(const V &a,const V &b) { return acos(a * b / len(a) / len(b)); }

// 钝角
inline bool dun(const V &a,const V &b,const V &c){return ((b-a)*(c-a))<-eps;}//angle:BAC

// atan2 直接得到向量与x轴的角度 -pi 到 pi
inline double angle(double x, double y) {return atan2(y, x);}

// 旋转 t为旋转角度 (x + yi) × (cosθ + sinθi) 逆时针旋转
inline V rotate(const V &o, double t){
  	double s=sin(t), c=cos(t);
  	return (V){o.x*c - o.y*s, o.x*s + o.y*c};
}

// 表示直线方程
struct line{
  	// 方向 a点 b点
 	V d,a,b;
};

inline line trans(const V &a,const V &b){//given points
  V dd(b.x-a.x, b.y-a.y);
  dd = dd / len(dd);
  return (line) {dd, a, b};
}

// 方向向量叉积为0
inline bool gongxian(const line &a,const line &b) {return abs(a.d ^ b.d)<eps;}

// 假设为直线，判断交点在不在线段上
inline V jiaodian(line u, line v){
  	// 不共线 
	double k = ((v.a - u.a) ^ v.d) / (u.d ^ v.d);
	return u.a + (k * u.d);
}

// 点到直线的距离
inline double dis(const line &l,const V &o,int op=0){//op=0:dis on line,op=1:dis on segment
  if(op&&(dun(l.a,o,l.b)||dun(l.b,o,l.a))) return min(len(o-l.a),len(o-l.b));
 	// 等面积 - 叉积求面积 
	// 向量叉积 求三角形 判断共线
 	else return abs((o-l.a)^(o-l.b))/len(l.a-l.b);
}

// 椭圆基本性质 x^2 / a^2+ y^2/ b^2 = 1
// 三点共线 - 行列式求三角形面积，再判断是否为0. / 点到直接的三角形， 判断是否共线

inline V operator+(const V &a, const V &b) { return V(a.x + b.x, a.y + b.y);}
inline V operator-(const V &a, const V &b) {return V(a.x - b.x, a.y - b.y);}
inline V operator/(const V &a, const double b) {return V(a.x / b, a.y / b);}
inline V operator*(const V &a, const double b) {return V(a.x * b, a.y * b);}
double operator*(const V &a, const V &b) { return a.x * b.x + a.y * b.y;}
double operator^(const V &a, const V &b) { return a.x * b.y - a.y * b.x;}
double len(const V& a) {return sqrt(a.x * a.x + a.y *a.y);}

V get_intersection(line &a, line &b) {
    double k = ((b.a - a.a) ^ b.d) / (a.d ^ b.d);
    return V(a.a + a.d * k);
}

line transform(const V &a, const V &b){
    V dd = V(b.x - a.x, b.y - a.y);
    dd = dd / len(dd);
    return line{dd, a, b};
}

bool is_para(const line &a, const line &b) {
    return abs(a.d ^ b.d) < eps;
}

bool is_Same(const line &a, const line &b) {
    return abs((b.a - a.a) ^ (b.a - a.b)) < eps;
}

bool is_inline(const line &a, const V &b) {
    double l = a.a.x, r = a.b.x;
    bool res = false;
    if (l > r) swap(l, r);
    if (abs(l - r) > eps) {
        res = res | (l <= b.x && b.x <= r);
    }
    else {
        double ll = a.a.y, rr = a.b.y;
        if (ll > rr) swap(ll, rr);
        res = res | (ll <= b.y && b.y <= rr);
    }
    return res;
}

class Solution {
public:
    vector<double> intersection(vector<int>& start1, vector<int>& end1, vector<int>& start2, vector<int>& end2) {
        V a(start1[0], start1[1]), b(end1[0], end1[1]), c(start2[0], start2[1]), d(end2[0], end2[1]);
        if (a.x > b.x) swap(a, b);
        if (c.x > d.x) swap(c, d);
        if (a.x == b.x) if (a.y > b.y) swap(a, b);
        if (c.x == d.x) if (c.y > d.y) swap(c, d);
        if (a.x > c.x) {
            swap(a, c);
            swap(b, d);
        }
        else if (a.x == c.x) {
            if (a.y > c.y) {
                swap(a, c);
                swap(b, d);
            }
        }

        line l1 = transform(a, b);
        line l2 = transform(c, d);
        vector<double> ans;
        if (is_para(l1, l2)) {
            if (!is_Same(l1, l2)) return ans;
            else {
                if (c.x > b.x) return ans;
                else if(a.x != c.x) {
                    ans = {c.x, c.y};
                    return ans;
                }
                if (a.x == c.x) {
                    if (c.y > b.y) return ans;
                    else {
                        ans = {c.x, c.y};
                        return ans;
                    }
                }
            }
        }
        else {
            V target = get_intersection(l1, l2);
            bool r1 = is_inline(l1, target);
            bool r2 = is_inline(l2, target); 
            if (r1 && r2) {
                ans = {target.x, target.y};
                return ans;
            }
        }
        return ans;
    }
};
```

## basic

### define

```c++
#include <bits/stdc++.h>

using namespace std;

// #define int long long
#define ll long long
#define vi vector<ll>
#define vvi vector<vi>
#define rep(i, a, b) for(auto i = (a); (i) < (b); (i)++)
#define rrep(i, b, a) for (auto i = (b); (i) > (a); (i)--)
#define fastio std::ios_base::sync_with_stdio(false); cin.tie(NULL);
#define all(v) (v).begin(), (v).end()
#define sz(v) (int)(v).size()
#define ump unordered_map<ll, ll>
#define pub push_back 
#define pob pop_back
#define arr array<ll, 3>
#define pii pair<ll, ll>
#define fi first
#define se second
```

### unique/count/find/rotate

```c++
nums.erase(unique(nums.begin(), nums.end()), nums.end());
auto cnt = count(all(s),'1');
std::size_t found = str.find(str2);
find(vec.begin(), vec.end(), item);

// 1 2 3 4 5 6 7 8 9 -> 4 5 6 7 8 9 1 2 3
std::rotate(myvector.begin(),myvector.begin()+3,myvector.end());

accumulate(v.begin(), v.end(), initial_sum);
```

### 初始化

**使用引用接收参数/返回值**

```c++
// debug
// +-DLOCAL
#ifdef LOCAL
    freopen("data.in", "r", stdin);
#endif
// 引用部分
#include <cstdio> #include <climits>
#define debug(a) cout << #a << " = " << a << endl;
#define mod(x) (x) % MOD
// 声明
using ULL = unsigned long long;
typedef ;

// arr
// INT_MAX注意溢出 10..9
const int INF = 0x3f3f3f3f;
// 初始化 
const int maxn = 1001;
// INT_MAX注意溢出 10..9
const int INF = 0x3f3f3f3f;
// -1 全为1 0 0x3f
int w[maxn][maxn];
fill(&w[0][0], &w[0][0] + maxn * maxn, INF);
memset(w, -1, sizeof(w));

// vector
// Using assignment operator to copy one
vector<vector<int>> vec(m, vector<int> (n, 0));
vect2 = vect1;
```

### 指针

```c++
// 回文串反向
string(prefix + prefix.rbegin() + (len & 1), prefix.rend());

// 距离 注意set O(n)
distance(a.begin, lower_bound(c));

// List
// doubly linked list
List<int> a;
// dynamic array
deque<int> b;

// 声明迭代器
list<Node>::iterator cur = m[key];
```

### 赋值/删除

```c++
using VI=vector<int>;
using VLL=vector<LL>;

#define next(p) (p == n-1 ? 0 : p + 1)
#define prev(p) (p == 0 ? n - 1 : p - 1)

// ull a > -1 恒成立
// val to bool !2-false !!2 = true
!!2  
// 赋值并清空
a = move(b);

// 浮点计算 不用double 前置1.0即可
double cx1 = 1.0 * (b[r] - b[p]) / (k[r] - k[p]);
double x_min = 1e100, x_max = -1e100;
double y_min = 1e100, y_max = -1e100;

// swap 
swap(a, b);

// unique
sort(nums.begin(),nums.end());
// unique array and return the last interator
nums.erase(unique(nums.begin(), nums.end()), nums.end());

// map
it = mymap.find('b');
if (it != mymap.end())
    mymap.erase (it);

// multiset 只删一个
ms.erase(ms.find(v));

// 获取前值
// decomposition declaration
auto [u, mask, dist] = q.front();
// 栈入
q.emplace(i, 1 << i, 0);
// array 代替tuple
array<int, 3> p = {1, 2, 3};
// 从小到大
priority_queue<arr, vector<arr>, greater<arr>> pq;


// 合并集合
pre[next].insert(pre[course].begin(),pre[course].end());
                
```

### 逻辑

```c++
// while 循环
while(int i = 0; i < n;) {
    int tmp = i;
    while(tmp < n && a[i] == a[tmp]) tmp++;
}
// for 循环
for (int i = 0, j = 0; i < n; i++);

// goto  
goto end;
end:;

// sort
order = VI(n);
for(int i = 0;i < n;i++)order[i] = i;
// order与index
sort(order.begin(),order.end(),[&](int x,int y){return a[x] > a[y];});


```

### 数字

1. float/bit表示

   ```c++
   // 0x 16进制 0b 2-bit 0o 8-bit  
   // 2^3 注意10^5有六位
   0x1e5,0x1p3,1e5;
   
   // 奇数 偶数 -> 已 a & 1 来表示
   arr[a&1] = 1;
   
   // ull (1 << 64) - 1 bit
   INT_MAX = (1 << 31) - 1
   INT_MIN = 1 << 31 (~0);
   // !注意通过1ll来移动
   Long = 1ll << 31;
   // 通过stoull转化
   
   char buffer[20];
   sprintf(buffer, "%.2f", a); //...
   
   sscanf(s.c_str(), "farmat", &num); 
   // round - (int)(x + 0.5)
   // round(x * 100) / 100 - 四舍五入
   ```

2. 溢出

   **abs/max出现溢出** 

   ```c++
   // ! 防止溢出 
   llabs();
   
   // c++对负数取模不同于python
   // python -1 // 10 = -1 向负无穷取整，C向0取整
   a == (a / b * b) + a % b;  
   // ture mudulo python
   -1 % 10 = 9;
   // C的取整
   -1 % 10 = -1;
   
   // size_t(0uz) greater than 0 unsigned  
   // unsigned int overflow 从0重新开始
   ```

### 字符串

```c++
// transform 
stoi();
// string to ull
// 0开始 的长度为x的子串
stoull(n.substr(0, x));
// num to string
to_string();
// 回文
string(prefix + prefix.rbegin() + (len & 1), prefix.rend());

// 通过内置string函数代替数字哈希 int + '|'
unordered_set<string> us;
// find 寻找第一个出现字符串的位置
code.find(string, start_pos);
```

### custom

```c++
// compare
// 注意不能小于等于
sort(arr.begin(), arr.end(), [](const vector<int> &a, const vector<int> &b) {
    if (a[0] == b[0]) return a[1] < b[1];
    return a[0] < b[0];
});

// sort greater 代表相反
bool cmp(T a, T b) {
    
}

// queue
struct cmp{
     // bool operator()
     bool operator()(const pis &a, const pis &b) {
         //...
     }
}

// cmp as function/lambda
priority_queue<Foo, vector<Foo>, decltype(cmp)> que(cmp);
// cmp as class
priority_queue<Foo, vector<Foo>, Compare> pq;

struct myHash{
	size_t operator()(Cell const& s) const  {
		return (size_t) (s.x * 0x1f1f1f1f) ^ s.y;
	}
};

// this is const
bool operator==(const Pos& otherPos) const
{
    if (this->row == otherPos.row && this->col == otherPos.col) return true;
    else return false;
}
```

### I/O

```c++
// getline
// !getline 前还有一个换行符
cin.get();
string str;
getline(cin,str);

// 不定长
if (cin.get() == '\n') break;

// 提取信息
sscanf(str.c_str(), "%d is the root", &y);
    
// 输出
// 面对不能多余打印的内容 - 提前存储 - 后打印 
printf("%05d\n", val);
// 最少的总宽度 x2.12 + 展示符号
printf("%+05.2f\n", val);

// conditional cout
cout << x == 1 ? "a" : "b" << endl;
// string literal 索引 \n\0 (\0是默认的一位)
cout << a[i] << " \n"[i == N - 1];

// interactive 
// [] 为正则，表示出\n外的字符
#include <stdio.h>
#include<stdlib.h>
int main()
{
    char str[20];
    int i;
    for (i=0; i<2; i++) {
        scanf("%[^\n]s", str);
        printf("%s\n", str);
        // fflush(stdin);
    }
    return 0;
}
```

### 内存分析

使用l r代替新增的数组 LCA

```c++
node* build(vi &a, int l, int r) {
    if (l > r) return nullptr;
    node *head = new node(a[l]);
    int ml = r + 1;
    rep (i, l + 1, r + 1) {
        if (a[i] > a[0]) {
            ml = i;
            break;
        }
    }
    head->left = build(a, l + 1, ml - 1);
    head->right = build(a, ml, r);
    return head;
}
```

### 时间分析

总的合并次数 + 遍历次数  

复杂度分析 - 随机变量的估计  ? random

200ms 3*n 三倍时间 == 超时

```c++
// 10**9
#include <chrono>
using namespace std::chrono;
    auto start = high_resolution_clock::now();
	// 10**9 视为1s
	// ull 2s-6s(个人pc), oj 1-2s
	// 10**18 = 10**9s; 3600s = 1h ...
    for (ull i = 1; i <= a; i++) {
        res++;
    }
    cout << res << endl;
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
 
    cout << "Time taken by function: "
         << duration.count() << " microseconds" << endl;
```
