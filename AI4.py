#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
形態素解析を用いた
会話記憶型人工無能
"""
import random

# ファイル関係
def FOpen(name):
    t = raw_input('ファイル名:')
    if t == '':
        t = name
    f = file(t,'r')
    s = f.readlines()
    t = ''
    for i in s:
        t += i
    s = t.split('\n')
    del(s[-1])

    return s

# 形態素リストの作成
def NGramList(m,n):
    new = []
    for i in range(0,len(m)-1):
        new += [[m[i],m[i+1]]]
    return new

# 単語のサーチ
def Findch(s,ch):
    ret = []
    for i in range(len(s)):
        if s[i][0]==ch:
            ret += [i]
    return ret

# 文の作成
def Sentence(s,ch,mes):
    # 始まりの文字を探す
    r = Findch(s,ch)
    if len(r)!=0:
        n = random.choice(r)
    else:
        n = -1

    # 選ばれたインデックスからメッセージを作成
    mes += s[n][1]
    return mes,s[n][1]

# 回答文
def Answer(s,ch):
    hst = 0
    mes = ch
    tip = ch
    while tip != '。' and tip != '！' and tip != '？' and hst <= 50:
        mes,tip = Sentence(s,tip,mes)
        hst += 1
    return mes

# ユーザーの入力から自動的に単語を決定する
def Dec_wo(cv,s):
    l = 0
    cv += '  '
    for i in range(0,len(cv),2):
        # 漢字を発見
        if cv[i] >= '\x88':
            l = i
            break
        elif cv[i]==' ':
            l = i
            break
    if cv[l]==' ':
        tip = '\n'
    else:
        tip = cv[l]+cv[l+1]
        while cv[l+2]>='\x88':
            l += 2
            tip += cv[l]+cv[l+1]
    return tip

# main
m = FOpen('text\\save\\morph_new_la.txt')
s = NGramList(m,2)

cv = ''
print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while cv != 'exit':
    cv = raw_input("あなた：")
    if cv != '' and cv != 'exit':
        tip = Dec_wo(cv,s)
        if tip != '\n':
            mes = Answer(s,tip)
            print 'アリーチェ：'+mes
    
print "アリーチェ：ばいば〜い"

