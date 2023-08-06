---
title: 算法练习记录
date: 2022-06-29 12:24:06
tags: Algorith
---

[Codeforces Round 885 (Div. 2)](https://codeforces.com/contest/1848)

1848-c

```c++
// TLE
int gett(int a, int b) {
    int ans = 0;
    if (a == 0) return 0;
    if (b == 0) return 1;
    if (a == b) return 2;
    if (a > b) {
        int x = a / b;
        // 最后会MOD3 没有必要加上
        ans += (x / 2) * 3;
        if (x % 2 == 1) {
            // 自以为多考虑了一步，实际使得下一次跳转的步长减少了
            // GCD证明一般考虑下界 即两次操作后，一定有 b -> b / 2
            // 分类讨论较为繁琐，一般记住特定的形式
            return ans + 2 + gett(a % b, b - a % b);    
        }
        else {
            return ans + gett(a % b, b);
        }
    }
    if (a < b) {
        return 1 + gett(b, b - a);
    }
}

int gett(int a, int b) {
    int ans = 0;
    if (a == 0) return 0;
    if (b == 0) return 1;
    if (a == b) return 2;
    if (a > b) {
        int x = a / b;
        ans += x / 2 * 3;
        if (x % 2 == 1) {
            return ans + 1 + gett(b, a % b);
        }
        else {
            return ans + gett(a % b, b);
        }
    }
    if (a < b) {
        return 1 + gett(b, b - a);
    }
}
```

[Codeforces Round 887 (Div. 2)](https://codeforces.com/contest/1853)

1853-c

[Codeforces Round 889 (Div. 2)](https://codeforces.com/contest/1855)

1855-b

1855-c2

```c++
// 一共只有31次操作机会

// 若将数组全部转换为大于0 / 小于0 需要19次操作

// 每次可以使得a[i] += a[j]，视为一次操作，目的是使得数组单调增 / 单调减

// 贪心：使得后面的尽量大，前面的尽量小
	// 需要改变的是差值，而不是绝对值的大小
// 拆分问题：两两讨论 a[i] a[i + 1]（前提不能改变a[i]）
	// 假定所有a[i]同号，需要消耗19次操作机会
		// 将a[i]转换为同号的情况 
			// S1：将absmx加到对应符号的值上，需要消耗19次 不符合31次的条件 
				// ！！！可以解决正数11 负数9时的问题
			// S2：设正数为多数，使得pmx变为absmx
				// 倍增需要5次
				// 当正数11 负数9时，9 + 5 = 14
				// 需要减少两次
					// 无法分类讨论 x

// ！有特殊情况使得S1不成立，却没有借助S1排除一部分情况。
// ！S2不能解决的反例不一定要提出一个改善的S2，S1能解决。
// 舍弃S1，认为S2需要改进才能解决问题，导致无法解决问题。  

// 当同时需要索引和值时的代码写法
mxid = max_element(a.begin(), a.end()) - a.begin(), mx = a[mxid];
```

