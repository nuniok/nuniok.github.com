---
title: leetcode 习题集
date: 2019-07-22
tags: [算法, leetcode]
id: 1
---

## 15. 三数之和

### 题目

给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。

注意：答案中不可以包含重复的三元组。

例如, 给定数组 nums = [-1, 0, 1, 2, -1, -4]，

满足要求的三元组集合为：
[
  [-1, 0, 1],
  [-1, -1, 2]
]

### 解题思路

初读这道题时忽略了一个点，就是在检查时，如果有两个重复的数字可以都用上组成一个三元组集合，但是在返回结果的时候不能第一个数字参与组成三元组后第二个相同数字继续组成三元组。**①**

有三种思路，先进性排序处理，然后再进行处理。第一种就是做三层枚举；第二种就是两层枚举，在进行 set O(1) 查找；第三种是一层枚举，然后从剩余列表中的左右两边进行查找，满足三元组的添加记录。

下面是主要介绍第三种思路的细节 **②**：

1. 排序处理
2. 从第 0 位置开始遍历
    1. 分别取剩余数组的首尾值进行求和
    2. 如果大于零则向前移动尾部游标
    3. 如果小于零则向后移动头部游标
    4. 如果等于零则添加记录
        1. 添加记录后对首尾游标向中间移动一格
    5. 如果首尾游标没有相交则继续 2.1 步骤处理
3. 进行下一位置的遍历，直到数组尾部
4. 返回结果

整个流程思路基本是这样子的，然后我们对于边界情况的处理单独进行描述 **③**

1. 如果当前遍历位置值大于 0 则直接返回结果
2. 对于我在 ① 中描述的情况，需要在 2.1 之前进行与判断，当前位置与上一位置值相同则跳过，进行排重处理
3. 同样的情况处理在 4.1 之后也要进行首尾游标移动方向相邻值的排重处理

### 解题思维

1. 首先需要做到的是充分理解题意，至少要做到能肉眼推导正确结果。
2. 解决方案一般都会有多种，合理选择最优方案进行骨架设计 ②，充分考虑时间和空间复杂度。
3. 然后解决边界条件 ③，优化代码可读性。
4. 充分进行测试验证算法的正确性。

### 解题代码

最后放一下解题代码，也是参考别人的方案实现的：

```
import java.util.*;

public class ThreeSum {

    public static List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> resp = new ArrayList<>();
        Arrays.sort(nums);
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] > 0) break;
            int l = i + 1;
            int r = nums.length - 1;
            if (i > 0 && nums[i-1] == nums[i]) continue;
            while (l < r){
                int sum = nums[i] + nums[l] + nums[r];
                if ( sum> 0) r--;
                else if (sum < 0) l++;
                else if (sum == 0){
                    resp.add(Arrays.asList(nums[i], nums[l] , nums[r]));
                    while (l < r && nums[l] == nums[l+1]) l++;
                    while (l < r && nums[r] == nums[r-1]) r--;
                    l++;
                    r--;
                }
            }
        }
        return resp;
    }
}

```

----------------


## 22. 括号生成

### 题目

给出 n 代表生成括号的对数，请你写出一个函数，使其能够生成所有可能的并且有效的括号组合。

例如，给出 n = 3，生成结果为：

```
[---
title: 51. N皇后
date: 2019-08-20
tags: [算法, leetcode]
id: 1
---
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]
```

### 思路

根据递归做暴力处理，同时进行剪枝操作。

### 解答

```
import java.util.ArrayList;
import java.util.List;

public class GenerateParenthesis {
    public static void main(String[] args) {
        GenerateParenthesis obj = new GenerateParenthesis();
        List<String> stringList = obj.generateParenthesis(3);
        System.out.println(stringList);
    }

    public List<String> generateParenthesis(int n) {
        List<String> collect = new ArrayList<>();
        gen(collect, "", n, n);
        return collect;
    }

    public void gen(List<String> collect, String cur, int left, int right) {
        if (left == 0 && right == 0) {
            collect.add(cur);
            return;
        }
        if (left > 0) {
            gen(collect, cur + "(", left - 1, right);
        }
        if (right > 0 && right > left) {
            gen(collect, cur + ")", left, right - 1);
        }
    }
}

```

----------------

## 49、242. 字母异位词

第一题：

`242. 有效的字母异位词`
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1:

输入: s = "anagram", t = "nagaram"
输出: true
示例 2:

输入: s = "rat", t = "car"
输出: false

说明:
你可以假设字符串只包含小写字母。

解答第一个思路是使用 HashMap 进行字频统计再对比，第二个思路是字符串排序后进行比较。

第二题：

`49. 字母异位词分组`

给定一个字符串数组，将字母异位词组合在一起。字母异位词指字母相同，但排列不同的字符串。

示例:

输入: ["eat", "tea", "tan", "ate", "nat", "bat"],
输出:
[
  ["ate","eat","tea"],
  ["nat","tan"],
  ["bat"]
]
说明：

所有输入均为小写字母。
不考虑答案输出的顺序。


练习输出：

```
import java.util.*;

public class Anagram {
    public static void main(String[] args) {
        System.out.println(isAnagram("anagram", "nagaram"));
        System.out.println(isAnagram2("anagram", "nagaram"));
        groupAnagrams(new String[]{"eat", "ate", "aaa"});
    }

    public static boolean isAnagram(String s, String t) {
        if (null == s && null == t) {
            return true;
        } else if (null == s || null == t) {
            return false;
        } else if (s.length() != t.length()) {
            return false;
        }
        Map<Character, Integer> left = new HashMap<>();
        Map<Character, Integer> right = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            left.put(s.charAt(i), left.getOrDefault(s.charAt(i), 0) + 1);
        }
        for (int j = 0; j < t.length(); j++) {
            right.put(t.charAt(j), right.getOrDefault(t.charAt(j), 0) + 1);
        }
        for (Map.Entry<Character, Integer> c : left.entrySet()) {
            if (!c.getValue().equals(right.getOrDefault(c.getKey(), 0))) {
                return false;
            }
        }

        return true;
    }

    public static boolean isAnagram2(String s, String t) {
        if (null == s && null == t) {
            return true;
        } else if (null == s || null == t) {
            return false;
        } else if (s.length() != t.length()) {
            return false;
        }
        char[] left = s.toCharArray();
        char[] right = t.toCharArray();
        Arrays.sort(left);
        Arrays.sort(right);
        for (int i = 0; i < left.length; i++) {
            if (left[i] != right[i]) {
                return false;
            }
        }
        return true;
    }

    public static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> res = new HashMap<>();
        for (String sr : strs) {
            char[] chars = sr.toCharArray();
            Arrays.sort(chars);
            String sortedSr = new String(chars);
            if (!res.containsKey(sortedSr)) {
                res.put(sortedSr, new ArrayList<>());
            }
            List<String> mapVal = res.get(sortedSr);
            mapVal.add(sr);
        }
        List<List<String>> rep = new ArrayList<>();
        for (Map.Entry<String, List<String>> entry : res.entrySet()) {
            rep.add(entry.getValue());
        }
        return rep;
    }
}

```

--------------------

## 51. N皇后

### 题目

n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

![8_queens](/resource/img/8_queens.png)

上图为 8 皇后问题的一种解法。

给定一个整数 n，返回所有不同的 n 皇后问题的解决方案。

每一种解法包含一个明确的 n 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。

示例:

```
输入: 4
输出: [
 [".Q..",  // 解法 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // 解法 2
  "Q...",
  "...Q",
  ".Q.."]
]
解释: 4 皇后问题存在两个不同的解法。
```

### 思路

...

### 解题

```
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class SolveNQueens {
    public static void main(String[] args) {
        SolveNQueens queens = new SolveNQueens();
        System.out.println(queens.solveNQueens(5));
    }

    public List<List<String>> solveNQueens(int n) {
        List<List<String>> resp = new ArrayList<>();
        Set<Integer> cols = new HashSet<>();
        Set<Integer> pie = new HashSet<>();
        Set<Integer> na = new HashSet<>();
        dfs(n, 0, new ArrayList<>(), resp, cols, pie, na);
        return resp;
    }

    public void dfs(int max, int row, List<String> curState, List<List<String>> resp,
                    Set<Integer> cols, Set<Integer> pie, Set<Integer> na) {
        // 终结条件
        if (row >= max) {
            if (curState.size() == max) {
                resp.add(curState);
            }
            return;
        }
        // 循环列
        for (int col = 0; col < max; col++) {
            if (cols.contains(col) || pie.contains(row + col) || na.contains(row - col)) {
                continue;
            }
            cols.add(col);
            pie.add(row + col);
            na.add(row - col);
            curState.add(trans(col, max));
            int size = curState.size();
            List<String> newState = (max - row == 1) ? new ArrayList<String>() {{
                addAll(curState);
            }} : curState;
            // 递归层
            dfs(max, row + 1, newState, resp, cols, pie, na);
            cols.remove(col);
            pie.remove(row + col);
            na.remove(row - col);
            curState.remove(size - 1);
        }
    }

    public String trans(int point, int max) {
        char[] chars = new char[max];
        for (int i = 0; i < max; i++) {
            chars[i] = i == point ? 'Q' : '.';
        }
        return String.valueOf(chars);
    }
}

```

------------------


## 69. x 的平方根


实现 `int sqrt(int x)` 函数。

计算并返回 x 的平方根，其中 x 是非负整数。

由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

示例 1:

```
输入: 4
输出: 2
```

示例 2:

```
输入: 8
输出: 2
说明: 8 的平方根是 2.82842..., 
     由于返回类型是整数，小数部分将被舍去。
```

### 思路

二分查找比较

需要注意的地方有两个

1. 注意开始边界问题
2. 注意类型长度越界


### 解答

```
public class MySqrt {
    public static void main(String[] args) {
        MySqrt mySqrt = new MySqrt();
        System.out.println(mySqrt.mySqrt(2147395599));

    }

    // 边界问题
    // 1. 0\1边界
    //  类型长度越界
    public int mySqrt(int x) {
        if (x == 0) return 0;
        if (x == 1) return 1;
        return mySqrt(x, 0, x);
    }

    public int mySqrt(long x, long left, long right) {
        long cur = (right - left) / 2 + left;
        long cur2 = cur * cur;
        if (cur2 == x) {
            return (int) cur;
        } else if (right - left == 1) {
            return (int) left;
        }

        if (cur2 < x) {
            left = cur;
        } else if (cur2 > x) {
            right = cur;
        } else {
            return (int) cur;
        }
        return mySqrt(x, left, right);
    }
}
```

### 扩展

牛顿迭代法

------------------

## 98. 验证二叉搜索树

### 题目

给定一个二叉树，判断其是否是一个有效的二叉搜索树。

假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
示例 1:

输入:

```
    2
   / \
  1   3
```

输出: true
示例 2:

输入:

```
    5
   / \
  1   4
     / \
    3   6
```

输出: false
解释: 输入为: [5,1,4,null,null,3,6]。
     根节点的值为 5 ，但是其右子节点值为 4 。

### 思路

首先拿到这个题看起来思路比较简单，实现起来还有有点困难，而且在思考过程中踩过一个坑，又爬上来的。哎，看题还是要全面点。

1. 首先想到就是中序遍历了，放到一个列表中，然后比较大小即可。
2. 或者是做一个递归操作，判断当前节点是否在一个范围即可。

思路是这么两个思路，代码实现起来为了执行效率做了短路处理，就是边遍历边检查，遇到错误就一路返回不再进行后面处理，当然这是思路理顺后的优化。

中序遍历没坑，直接写就行了，有坑的是第二种操作，刚开始觉得只要比较当前节点的父节点和两个子节点就好了，就像下面画的，已 C 点为当前节点进行处理，实际是一个错误的思路，并且情况也分析的不对。

![](/resource/img/15646758982785.jpg)

意识到问题后就重新分析，把当前节点作为最底端的节点，我们去比较的都是当前节点和父辈及以上的节点的大小，也就是拆出来四种情况。

![](/resource/img/15646763098184.jpg)

其中 `⨁` 表示当前节点，和其它点的相对位置表示左右子节点关系，`min -> max` 指向当前节点值必须在此区间中才可以，`+∞` 和 `-∞` 为单点情况的边界表示。最后拆分出这四种子情况，只要任一节点符合这四种情况之一即当前节点满足，当所有节点均满足则二叉搜索🌲有效，事实根据这个思路写出的代码验证是可行的。比较开心的是重新思考后的思路写出来的代码一次通过✌️。

### 代码

解法1

```
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public boolean isValidBST(TreeNode root){
        return forEachNode(root, new ArrayList<>());
    }

    public boolean forEachNode(TreeNode node, List<Integer> val){
        if (null == node) {
            return true;
        }
        if (!forEachNode(node.left, val)){
            return false;
        }
        if (!validOrAdd(val, node)){
            return false;
        }
        if (!forEachNode(node.right, val)){
            return false;
        }
        return true;
    }
    public boolean validOrAdd(List<Integer> val, TreeNode node){
        if(val.size() > 0 && val.get(val.size() - 1) >= node.val){
            return false;
        }else{
            return val.add(node.val);
        }
    }
}
```

解法2

```
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public boolean isValidBST(TreeNode root){
        return subValidBSTLeft(root, null, null);
    }

    public boolean subValidBSTLeft(TreeNode node, Integer min, Integer max) {
        if (null == node){
            return true;
        }
        if (null == min && null == max){
        }else if (null == min && null !=max && node.val < max){
        }else if (null != min && null == max && min < node.val){
        }else if (null != min && null != max && min < node.val && node.val < max){
        }else {
            return false;
        }
        // left
        if (!subValidBSTLeft(node.left, min, node.val)){
            return false;
        }
        // right
        if (!subValidBSTLeft(node.right, node.val, max)){
            return false;
        }
        return true;
    }
}
```

-----------------

## 102. 二叉树的层次遍历

### 问题

给定一个二叉树，返回其按层次遍历的节点值。 （即逐层地，从左到右访问所有节点）。

例如:
给定二叉树: [3,9,20,null,null,15,7],

```
    3
   / \
  9  20
    /  \
   15   7
```

返回其层次遍历结果：

```
[
  [3],
  [9,20],
  [15,7]
]
```

### 解答

```
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> resp = new ArrayList<>();
        levelOrder(root, 0, resp);
        return resp;
    }
    public void levelOrder(TreeNode cur, int cur_level, List<List<Integer>> resp) {
        if(null == cur){
            return;
        }
        if(cur_level == resp.size()){
            resp.add(new ArrayList<>());
        }
        resp.get(cur_level).add(cur.val);
        levelOrder(cur.left, cur_level+1, resp);
        levelOrder(cur.right, cur_level+1, resp);
    }
}
```

> 一次过


------------------------

## 104. 二叉树的最大深度

### 问题

给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

说明: 叶子节点是指没有子节点的节点。

示例：
给定二叉树 [3,9,20,null,null,15,7]，

```
    3
   / \
  9  20
    /  \
   15   7
```

返回它的最大深度 3 。

### 解答

```
class Solution {
    public int maxDepth(TreeNode root) {
        return maxDepth(root, 0);
    }
    public int maxDepth(TreeNode cur, int level) {
        if(null == cur) return level;
        int left_level = maxDepth(cur.left, level + 1);
        int right_level = maxDepth(cur.right, level + 1);
        return left_level > right_level ? left_level: right_level;
    }
}
```

> 一次过

-----------------

## 111. 二叉树的最小深度

### 题目

给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

说明: 叶子节点是指没有子节点的节点。

示例:

给定二叉树 [3,9,20,null,null,15,7],

```
    3
   / \
  9  20
    /  \
   15   7
```

返回它的最小深度  2.

### 解答

```
class Solution {
    public int minDepth(TreeNode root) {
        return minDepth(root, 0);
    }

    public int minDepth(TreeNode cur, int level) {
        if (null == cur) return level;
        if (null == cur.left && null == cur.right) {
            return level + 1;
        } else if (null != cur.left && null == cur.right) {
            return minDepth(cur.left, level + 1);
        } else if (null == cur.left && null != cur.right) {
            return minDepth(cur.right, level + 1);
        } else {
            int left_level = minDepth(cur.left, level + 1);
            int right_level = minDepth(cur.right, level + 1);
            return left_level > right_level ? right_level : left_level;
        }
    }
}
```

---------------

## 141. 环形链表

给定一个链表，判断链表中是否有环。

为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

正常的解题思路，通过记录走过的节点来判断是否有环。

时间复杂度：O(n)，对于含有 n 个元素的链表，我们访问每个元素最多一次。添加一个结点到哈希表中只需要花费 O(1) 的时间。

空间复杂度：O(n)，空间取决于添加到哈希表中的元素数目，最多可以添加 n 个元素。

```
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        HashSet<Integer> points = new HashSet<Integer>();
        ListNode cur = head;
        while (null != cur){
            int curHashCode = cur.hashCode();
            if(points.contains(curHashCode)){
                return true;
            }
            points.add(curHashCode);
            cur = cur.next;
        }
        return false;
    }
}
```

第二种解题思路是双指针大小步，一个指针每次走一步，另一个指针每次走两步，如果有环的话则两个指针最终会相遇。

在最糟糕的情形下，时间复杂度为 O(N+K)，也就是 O(n)。

空间复杂度：O(1)，我们只使用了慢指针和快指针两个结点，所以空间复杂度为 O(1)。

```
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        if (null == head){
            return false;
        }else if (null == head.next){
            return false;
        }else if (head == head.next.next){
            return true;
        }
        ListNode minCur = head.next;
        ListNode maxCur = head.next.next;
        while (minCur != maxCur){
            if (null == minCur.next){
                return false;
            }else if (null == maxCur.next){
                return false;
            }else if (null == maxCur.next.next){
                return false;
            }
            minCur = minCur.next;
            maxCur = maxCur.next.next;
            if (minCur == maxCur){
                return true;
            }
        }
        return false;
    }
}
```

-------------------

## 146. LRU缓存

运用你所掌握的数据结构，设计和实现一个  LRU (最近最少使用) 缓存机制。它应该支持以下操作： 获取数据 get 和 写入数据 put 。

获取数据 get(key) - 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
写入数据 put(key, value) - 如果密钥不存在，则写入其数据值。当缓存容量达到上限时，它应该在写入新数据之前删除最近最少使用的数据值，从而为新的数据值留出空间。

链接：https://leetcode-cn.com/problems/lru-cache


```
from collections import OrderedDict

class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self._cache = OrderedDict()
        self._size = capacity

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self._cache:
            return -1
        val = self._cache.pop(key)
        self._cache[key] = val
        return val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self._cache:
            self._cache.pop(key)
            self._cache[key] = value
        else:
            if len(self._cache) == self._size:
                self._cache.popitem(last=False)
            self._cache[key] = value


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```

有序字典的解法
时间复杂度 O(1)
空间复杂度 O(capacity)

Java 解法需要 LinkedHashMap **TODO**

LRU(Least Recently Used)最少最近使用，一种页面置换算法。

LFU(Least Frequently Used)最近最不常用。



### 其它

LRU

![](/resource/img/15720909856457.jpg)


----------------


## 206. 反转链表

```
public class ReverseLinkedList {
    public static void main(String[] args) {
        ListNode listNode = ListNode.of(
                1,
                ListNode.of(
                        2,
                        ListNode.of(
                                3,
                                ListNode.of(
                                        4,
                                        ListNode.of(
                                                5, null
                                        )
                                )
                        )
                )
        );
        ListNode next = listNode;
        while (null != next) {
            System.out.println(next.val);
            next = next.next;
        }

        System.out.println("===");
        ListNode reverse = reverse3(listNode);

        ListNode next2 = reverse;
        while (null != next2) {
            System.out.println(next2.val);
            next2 = next2.next;
        }
    }

    /**
     * 官方推荐的
     * @param head
     * @return
     */
    public static ListNode reverse2(ListNode head) {
        // prev -> curr -> nextTemp
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }

    /**
     * 自己写的
     * @param head
     * @return
     */
    public static ListNode reverse(ListNode head) {
        // cur -> prev -> tmp
        ListNode cur = head;
        ListNode next = head.next;
        head.next = null;
        while (null != cur) {
            ListNode tmp = null;
            if (null != next) {
                tmp = next.next;
                next.next = cur;
            }
            if (null == next) {
                break;
            }
            cur = next;
            next = tmp;
        }
        return cur;
    }

    /**
     * 复写的
     * 1. 记录前一个节点，当前节点
     * 2. 迭代
     * 3. 取出当前节点到临时变量
     * 4. -- 现在有 prev -> curr -> next 三个节点
     * 5. 将 curr.next -> prev，改变指向方向
     * 6. 依次挪动节点位置 prev = curr , curr = nextTemp
     * 7. 最后返回 prev
     *
     * 时间复杂度 O(n)
     * 空间复杂度 O(1)
     * @param head
     * @return
     */
    public static ListNode reverse3(ListNode head) {
        // prev -> curr -> next
        ListNode prev = null;
        ListNode curr = head;
        while (null != curr) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }
}
```

------------------

## 208. 实现 Trie (前缀树)

### 题目


实现一个 Trie (前缀树)，包含 insert, search, 和 startsWith 这三个操作。

示例:

Trie trie = new Trie();

trie.insert("apple");
trie.search("apple");   // 返回 true
trie.search("app");     // 返回 false
trie.startsWith("app"); // 返回 true
trie.insert("app");
trie.search("app");     // 返回 true
说明:

你可以假设所有的输入都是由小写字母 a-z 构成的。
保证所有输入均为非空字符串。


### 分析

前缀树
Trie
字典树

### 解答

```
public class Trie {
    private final int SIZE = 26;
    private Node root;

    private class Node {
        private boolean isStr;
        private int num;
        private Node[] child;

        public Node() {
            child = new Node[SIZE];
            isStr = false;
            num = 1;
        }
    }

    public Trie() {
        root = new Node();
    }

    public void insert(String word) {
        if (null == word || word.isEmpty()) {
            return;
        }
        Node pNode = this.root;
        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i) - 'a';
            if (pNode.child[index] == null) {
                Node tmp = new Node();
                pNode.child[index] = tmp;
            } else {
                pNode.child[index].num++;
            }
            pNode = pNode.child[index];
        }
        pNode.isStr = true;
    }

    public boolean search(String word) {
        if (null == word || word.isEmpty()) {
            return false;
        }
        Node pNode = this.root;
        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i) - 'a';
            if (pNode.child[index] == null || (word.length() - i == 1 && pNode.child[index].isStr == false)) {
                return false;
            }
            pNode = pNode.child[index];
        }
        return true;
    }

    public boolean startsWith(String prefix) {
        if (null == prefix || prefix.isEmpty()) {
            return false;
        }
        Node pNode = this.root;
        for (int i = 0; i < prefix.length(); i++) {
            int index = prefix.charAt(i) - 'a';
            if (pNode.child[index] == null) {
                return false;
            }
            pNode = pNode.child[index];
        }
        return true;
    }
}

```

-------------------

## 703. 数据流中的第K大元素

设计一个找到数据流中第K大元素的类（class）。注意是排序后的第K大元素，不是第K个不同的元素。

你的 KthLargest 类需要一个同时接收整数 k 和整数数组nums 的构造器，它包含数据流中的初始元素。每次调用 KthLargest.add，返回当前数据流中第K大的元素。

```
import java.util.PriorityQueue;

public class KthLargest {
    private PriorityQueue<Integer> minHeap;
    private int kSize;

    public KthLargest(int k, int[] nums) {
        kSize = k;
        minHeap=new PriorityQueue<Integer>(kSize);
        for (int i = 0; i< nums.length; i++){
            add(nums[i]);
        }
    }

    public int add(int val) {
        if (minHeap.size() < kSize){
            minHeap.offer(val);
        }else if (minHeap.peek() < val){
            minHeap.poll();
            minHeap.offer(val);
        }
        return minHeap.peek();
    }
}
```
Java中PriorityQueue通过二叉小顶堆实现，可以用一棵完全二叉树表示。

关于堆操作：https://shmilyaw-hotmail-com.iteye.com/blog/1775868

操作说明：

<table><thead><tr class="header"><th>方法名</th><th>功能描述</th></tr></thead>
<tbody><tr class="odd"><td>add(Ee)</td><td>在队列头部增加一个元素，如果容量已满，则抛出异常，成功则返回true。</td></tr>
<tr class="even"><td>clear()</td><td>清空</td></tr>
<tr class="odd"><td>contains(Objecto)</td><td>检查是否包含当前参数元素</td></tr>
<tr class="even"><td>offer(Ee)</td><td>在队列头部增加一个元素，如果容量已满，则返回false，成功加入，返回true。</td></tr>
<tr class="odd"><td>peek()</td><td>返回队列头部节点，但不移除队列头节点。</td></tr>
<tr class="even"><td>poll()</td><td>将队列头部元素移出队列并返回。</td></tr>
<tr class="odd"><td>remove(Objecto)</td><td>将队列头部元素移出队列并返回，如果队列为空，则抛出异常。</td></tr>
<tr class="even"><td>size()</td><td>返回长度</td></tr></tbody></table>

---------------
