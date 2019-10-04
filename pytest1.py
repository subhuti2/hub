#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 21:05:43 2018

@author: pwang
"""
# 2018-06-18

print('hello, world')

print('The quick brown fox', 'jumps over', 'the lazy dog')

print(300)

print(100 + 300 + 500)

print('please input your name:\n')
name = input()
print('hello,', name)

print(r'''hello,\n
world''')

print('''line1
...line2
...line3''')

a = 'ABC'
b = a
a = 'XYZ'
print(b)

12 % 4
n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"'
s4 = r'''Hello,
Lisa!'''

print(s1, s2, n, f, s3, s4)

print('包含中文的str')
ord('A')
ord('中')
chr(66)
'\u4e2d\u6587'
'ABC'.encode('ascii')
'中文'.encode('utf-8')
'中文'.encode('ascii')
b'ABC'.decode('ascii')
len('ABC')
 len('中文'.encode('utf-8'))
'Hi, %s, you have $%d.' % ('Michael', 1000000)

print('%2d-%02d' % (3, 1))
print('%.2f' % 3.1415926)


classmates = ['Michael', 'Bob', 'Tracy']
classmates.append('Adam')
classmates.insert(1, 'Jack')
classmates.pop()
classmates.pop(2)

L = ['Apple', 123, True]
s = ['python', 'java', ['asp', 'php'], 'scheme']
len(s)
p = ['asp', 'php']
s = ['python', 'java', p, 'scheme']
s[2][1][1]
classmates = ('Michael', 'Bob', 'Tracy')

t = (1, 2)
t = (1)
tt = (1,)



L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
print(L[0][0])
print(L[1][1])
print(L[2][2])


age = 1
if age >= 18:
    print('your age is', age)
    print('adult')
elif age >= 6:
    print('your age is', age)
    print('teenager')
else:
    print('your age is', age)
    print('teenager')    
    
birth = input('birth: ')
birth = int(birth)
if birth < 2000:
    print('00前')
else:
    print('00后')

H = input('Height: ')
W = input('Weight')
bmi = float(W) / (float(W)**2)
if bmi < 18.5:
    print('过轻')
elif bmi < 25:
    print('正常')
elif bmi < 28:
    print('过重')
elif bmi < 32:
    print('肥胖')
else
    print('严重肥胖')

names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)    
    
list(range(5))


sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)

n = 1
while n <= 100:
    n = n + 1
    if n % 2 : # 如果n是偶数，执行continue语句
        continue # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(n)
print('END')


d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d['Adam'] = 67

'Thomas' in d

d.pop('Bob')

d.pop()

s = set([1, 1, 2, 2, 3, 3])
print(s)
s.add(4)
s.remove(4)


s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
s1 & s2
s1 | s2
a = ['c', 'b', 'a']
a.sort()
a

f = open('/Users/wang/git/hub/hub/X1.txt', 'r')
f.read()
f.close()

f = open('/Users/wang/git/hub/hub/X1.txt', 'r')
f.read()
f.close()

with open('/Users/wang/git/hub/hub/X1.txt', 'r') as f:
    print(f.readline())

with open('/Users/wang/git/hub/hub/X1.txt', 'r') as f:
    y = f.read()

f = open('/Users/wang/git/hub/hub/X1.txt', 'r')
k = 0
for line in f.readlines():
    y[k] = line
    k = k + 1
f.close()
