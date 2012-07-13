#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
形態素解析プログラムによって出力された
形態素のテキストファイルを利用して応答する
マルコフ連鎖の形態素型アリーチェとの会話プログラム
(漢字を優先的に選ぶ)
"""
import random
import sys
import re


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

# 開始文字列の決定(漢字優先)
def SetStartch(_line):
    chList = re.findall(u"[\u4e00-\u9fa5]+", _line)
    if chList == []: return ""
    else: return random.choice(chList)[0]

# 形態素の中から単語を探してリストから選択したものを返す
def Findch(_wrdList, _iniChar):
    iniChar = _iniChar
    if not _iniChar in [x[0][0] for x in _wrdList]: iniChar = random.choice([x[0][0] for x in _wrdList])
        
    return iniChar

# ルーレットを作る
def MakeRouret(_wrdList, iniChar):
    rouret = []
    iniList = [x[0][0] for x in _wrdList]
    index = iniList.index(iniChar)
    while iniChar == iniList[index]:
        rouret += [index]*_wrdList[index][1]
        index += 1
    
    return rouret

# main
lines,n = FOpen('text/sample.txt')

lines = GetWideChar(lines)
lines = NGramList(lines,n)
lines.sort()

wrdList = Uniqs(lines)

print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while True:
    s = raw_input("あなた：").decode('utf-8')
    if s == '': continue

    iniChar = SetStartch(s)
    iniChar = Findch(wrdList, iniChar)

    word,msg = '', ''
    cnt = 0
    while word == '' or (word[-1] != u'。' and word[-1] != u'？' and word[-1] != u'！' and cnt <= 20):
        rouret = MakeRouret(wrdList, iniChar)
        word = wrdList[random.choice(rouret)][0]
        msg += word[:-1]
        iniChar = word[-1]
        cnt += 1

    print u"アリーチェ："+msg

print "アリーチェ：ばいば〜い"

