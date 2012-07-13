#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
マルコフ連鎖を用いた
アリーチェとの会話プログラム(n-gram)
"""
import random
import sys

# ファイル関係
def FOpen(_file):
    dat_file = ''
    if len(sys.argv)==1: dat_file = _file
    else: dat_file = sys.argv[1]

    n = raw_input("n-gram：")
    if n == '': n = 3
    else: n = int(n)

    f = open(dat_file,'r')
    lines = f.readlines()
    
    return lines,n

# unicode変換
def GetWideChar(_lines):
    lines = []
    for i in range(len(_lines)):
        lines.append(_lines[i].decode('utf-8'))
    return lines

# n文字ずつのリストに再構築
def NGramList(_lines,n):
    _lines = "".join(_lines)
    lines = []
    for i in range(len(_lines)):
        if i+n == len(_lines)-1: break
        lines.append(_lines[i:i+n])

    return lines

# 重複の削除
def Uniqs(_lines):
    prevStr = ''
    fSame = False
    wrdList = []
    lstIndex = -1

    for i in range(len(_lines)):
        if prevStr == _lines[i]: fSame = True
        else: fSame = False

        if fSame == True:
            wrdList[lstIndex][1] += 1
        else:
            wrdList.append([_lines[i],1])
            lstIndex += 1

        prevStr = _lines[i]
    return wrdList

# ルーレットを作る
def MakeRouret(_wrdList, iniChar):
    rouret = []
    iniList = [x[0][0] for x in _wrdList]
    index = iniList.index(iniChar)
    while iniChar == iniList[index] :
        rouret += [index]*_wrdList[index][1]
        index += 1
    
    return rouret

# main
lines,n = FOpen('text/sample.txt')

lines = GetWideChar(lines)
lines = NGramList(lines,n)
lines.sort()

wrdList = Uniqs(lines)

print u"アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"

while True:
    s = raw_input("あなた：").decode('utf-8')
    if s == '': continue

    iniChar = ''
    for i in range(len(s)):
        if s[i] in [x[0][0] for x in wrdList]:
            iniChar = s[i]
            break
    if iniChar == '':
        iniChar = random.choice([i[0][0] for x in wrdList])
    
    word = ''
    cnt = 0
    msg = ''
    while word == '' or (word[-1] != u'。' and word[-1] != u'？' and word[-1] != u'！' and cnt <= 20):
        rouret = MakeRouret(wrdList, iniChar)
        word = wrdList[random.choice(rouret)][0]
        msg += word[:-1]
        iniChar = word[-1]
        cnt += 1

    print u"アリーチェ："+msg

print "アリーチェ：ばいば〜い"
