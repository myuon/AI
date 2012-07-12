#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
形態素解析プログラムによって出力された
形態素のテキストファイルを利用して応答する
マルコフ連鎖の形態素型アリーチェとの会話プログラム
"""
import random
import sys

# ファイル関係
def FOpen(name):
    f = file(name,'r')
    s = f.readlines()
    t = ''
    for i in s:
        t += i
    s = t.split('\n')
    del(s[-1])

    return s

# n個ずつ形態素が含まれるリストに再構築
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

# 開始文字列の決定
def SetStartch(line,l):
    line += '　'
    for i in range(l,len(line),2):
        # 漢字があったらそれを開始文字とする
        if line[i]>='\x88':
            l = i
            break
        elif line[i]=='　':
            l = i
            break
    # なければ仕方がないので適当に
    if line[l]=='　':
        start = 'あ'
    else:
        start = line[l]+line[l+1]
        while line[l+2]>='\x88':
            l += 2
            start += line[l]+line[l+1]
    return start,l

# 形態素の中から単語を探してリストから自由に選択したものを返す
def Findch(start):
    cnt = []
    for i in range(len(s)):
        if start in s[i] and start[0] == s[i][0]:
            cnt += [i]*num[i]
            return random.choice(cnt)
    # 見つからなかった場合
    return -1

# 連鎖しながら出力
def TypeChar(wide,n,message):
    # 重複の削除
    i = 0
    while i < range(len(message)):
        if wide[n][-1-i] == message[-1-i] and wide[n][-2-i] == message[-2-i]:
            message = message.strip(message[-1]+message[-2])
            i -= 2
        else:
            break
        i += 2

    message += wide[n]
    return wide[n],message

# メッセージの表示
def Mes(start):
    tip = start
    hist = 0
    message = start

    # メッセージは最大50単語まで
    while not( '。' in tip or '？' in tip or '！' in tip ) and hist <= 50:
        # はじめの単語を決定する
        n = Findch(tip)

        tip,message = TypeChar(s,n,message)
        hist += 1
    print 'アリーチェ：'+message

# main
t = sys.argv[1]
if t=='': t = 'text/sample.txt'
s = NGramList(FOpen(t),2)
Sort(s)
s,num = Uniqs(s)
Sort(s,num)

print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
cv = ''
while cv != 'exit' :
    cv = raw_input("あなた：")
    if cv != '' and cv != 'exit' :
        # cvから漢字を切り出してはじめの文字にする
        l = 0
        start,l = SetStartch(cv,l)
        while Findch(start) == -1:
            start,l = SetStartch(cv,l)
            print start
        Mes(start)

print "アリーチェ：ばいば〜い"

