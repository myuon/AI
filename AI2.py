#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
マルコフ連鎖を用いた
アリーチェとの会話プログラム(n-gram)
"""
import random
import sys

# 全角文字だけ抜き出して、1文字ずつ格納
def GetWideChar(lines,wide):
    for i in range(len(lines)):
        n = 0
        while n < len(lines[i])-1:
            tip = ''
            if n % 2 == 0 and not lines[i][n] in [' ', '\n'] :
                tip += lines[i][n]
            tip += lines[i][n+1]
            if tip != '　' :
                wide += [tip]
            n += 2
    return

#n文字ずつのリストに再構築
def NGramList(wide,n):
    new = ['']*(len(wide)-n+1)
    for i in range(len(wide)-n+1):
        for l in range(n):
            new[i] += wide[i+l]
    return new

# ソート
def Sort(wide,num=[]):
    if num == [] :
        wide.sort()
    else:
        for i in range(len(num)):
            bf = num.index(max(num[i:]),i)
            tmp = num[bf]
            num[bf] = num[i]
            num[i] = tmp

            tmp = wide[bf]
            wide[bf] = wide[i]
            wide[i] = tmp

# 重複の削除
def Uniqs(wide):
    new = []
    num = []
    prev = ''
    px = -1
    for i in wide:
        if i == prev:
            num[px] += 1
        else:
            new += [i]
            prev = i
            px += 1
            num += [1]
    return new,num

# 連鎖しながら出力
def TypeChar(wide,n,message):
    for i in range(2,len(wide[n])):
        if i % 2 == 0:
            message += wide[n][i]+wide[n][i+1]
    return wide[n][-2]+wide[n][-1],message

# main
s = sys.argv[1]
if s == '':
    s = 'text/sample.txt'
n = raw_input("n-gram：")
if n == '':
    n = 3
else:
    n = int(n)
f = open(s,'r')
lines = f.readlines()

wide = []
start = ''

GetWideChar(lines,wide)
wide = NGramList(wide,n)
Sort(wide)
wide,num = Uniqs(wide)
Sort(wide,num)

# Quick 1st-letter-List
ql = []
for i in wide:
    ql += [i[0]+i[1]]

print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while s != 'exit' :
    s = raw_input("あなた：")
    if s != '' and s != 'exit' :
        start = ''
        while not start in ql:
            p = random.randint(0,len(s)/2-1)
            start = s[p*2]+s[p*2+1]
        tip = start
        hist = 0
        message = start

        while tip != '。' and tip != '？' and tip != '！' and hist <= 500:
            cnt = []
            for l in range(len(ql)):
                if ql[l] == tip:
                    cnt += [l]*num[l]
            n = random.choice(cnt)

            tip,message = TypeChar(wide,n,message)
            hist += 1
        print 'アリーチェ：'+message
        
print "アリーチェ：ばいば〜い"

