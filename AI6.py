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
    fn = t
    f = file(t,'r')
    s = f.readlines()
    t = ''
    for i in s:
        t += i
    s = t.split('\n')
    del(s[-1])

    return s,fn

# 形態素の切り出し
def Morph(line):
    m,prev = '',''
    tmp = line
    mor = []
    pm = -1
    for i in range(0,len(line),2):
        ch = tmp[i]+tmp[i+1]
        # 長音「ー」は前の形態に引っ張られる
        if ch == 'ー':
            m = prev
        elif tmp[i]>='\x88':
            m = 'c'
        elif tmp[i]=='\x83' and 40<=tmp[i+1]<='\x96':
            m = 'k'
        elif ch=='.' or ch==',' or ch=='。' or ch=='、' or ch=='？' or ch=='！':
            m = 'n'
        else:
            m = 'e'

        if m != prev:
            mor += [tmp[i]+tmp[i+1]]
            pm += 1
        else:
            mor[pm] += tmp[i]+tmp[i+1]
        prev = m
    return mor

# 形態素リストの作成
def NGramList(m):
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

# 回答文の作成
def Answer(s,ch):
    hst = 0
    mes = ch
    tip = ch
    while tip != '。' and tip != '！' and tip != '？' and hst <= 50:
        mes,tip = Sentence(s,tip,mes)
        hst += 1
    return mes

# 形態素の解析
def AddMorph(cv,fn,s):
    w = Morph(cv)
    f = open(fn,'a')
    for i in w:
        f.write(i+'\n')
    f.close()

    # いま解析した形態素をリストに追加
    s += NGramList(w)

    # ユーザーの入力から名詞を選んで言葉を返す
    c = '00'
    l = 0
    while c[0]<'\x88':
        c = random.choice(w)
        l += 1
        if l > len(w)*2:
            break
    return c

# main
m,fn = FOpen('text\\save\\mem_hi.txt')
s = NGramList(m)

cv = ''
print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while cv != 'exit':
    cv = raw_input("あなた：")
    if cv != '' and cv != 'exit':
        # 相手の入力を形態素解析にかける
        tip = AddMorph(cv,fn,s)
        if tip != '':
            mes = Answer(s,tip)
            print 'アリーチェ：'+mes
    
print "アリーチェ：ばいば〜い"

