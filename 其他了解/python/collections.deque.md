deque 是一个双端队列, 如果要经常从两端append 的数据, 选择这个数据结构就比较好了, 如果要实现随机访问,不建议用这个,请用列表. deque 优势就是可以从两边append ,appendleft 数据. 这一点list 是没有的.

```
import collections
d = collections.deque([])
d.append('a') # 在最右边添加一个元素，此时 d=deque('a')
d.appendleft('b') # 在最左边添加一个元素，此时 d=deque(['b', 'a'])
d.extend(['c','d']) # 在最右边添加所有元素，此时 d=deque(['b', 'a', 'c', 'd'])
d.extendleft(['e','f']) # 在最左边添加所有元素，此时 d=deque(['f', 'e', 'b', 'a', 'c', 'd'])
d.pop() # 将最右边的元素取出，返回 'd'，此时 d=deque(['f', 'e', 'b', 'a', 'c'])
d.popleft() # 将最左边的元素取出，返回 'f'，此时 d=deque(['e', 'b', 'a', 'c'])
d.rotate(-2) # 向左旋转两个位置（正数则向右旋转），此时 d=deque(['a', 'c', 'e', 'b'])
d.count('a') # 队列中'a'的个数，返回 1
d.remove('c') # 从队列中将'c'删除，此时 d=deque(['a', 'e', 'b'])
d.reverse() # 将队列倒序，此时 d=deque(['b', 'e', 'a'])
f=d.copy()
print(f)#deque(['b', 'e', 'a'])
f.clear()
print(f)#deque([])

#可以指定队列的长度，如果添加的元素超过指定长度，则原元素会被挤出。
e=collections.deque(maxlen=5)
e.extend([1,2,3,4,5])
e.append("a")
print(e)
#deque([2, 3, 4, 5, 'a'], maxlen=5)
e.appendleft("b")
print(e)
#deque(['b', 2, 3, 4, 5], maxlen=5)
e.extendleft(["c","d"])
print(e)
#deque(['d', 'c', 'b', 2, 3], maxlen=5)
```

