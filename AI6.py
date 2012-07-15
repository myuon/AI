#! /usr/bin/python
#-*- coding:utf-8 -*-


"""
形態素解析を用いた
会話記憶型人工無能
"""
import random
import sys
import re


# ファイル関係
def FOpen(_file):
    dat_file = ''
    if len(sys.argv)==1: dat_file = _file
    else: dat_file = sys.argv[1]

    f = open(dat_file,'r')
    lines = f.readlines()
    lines = toUnicode(lines)
    
    return lines, dat_file

# unicode変換
def toUnicode(_lines):
    lines = []
    for i in range(len(_lines)):
        lines.append(_lines[i].decode('utf-8'))
    return "".join(lines)

# 形態素リストの作成
def NGramList(_list):
    wrdList = []
    for i in range(len(_list)-1):
        wrdList.append([_list[i],_list[i+1]])
        
    return wrdList

#形態素の切り出し
def Morph(_str):
    nowMode = 'None'
    preMode = 'None'
    morphList = []
    index = -1
    for i in range(len(_str)):
        # 長音「ー」は前の形態に引っ張られる
        if re.match(u"[ー]", _str[i]) != None:
            nowMode = preMode
        elif re.match(u"[\u4e00-\u9fa5]", _str[i]) != None:
            nowMode = 'ZEN_KANJI'
        elif re.match(u"[ぁ-ゞ]", _str[i]) != None:
            nowMode = 'ZEN_HIRAGANA'
        elif re.match(u"[ァ-ヾ]", _str[i]) != None:
            nowMode = 'ZEN_KATAKANA'
        elif re.match(u"[ｦ-ﾝ]", _str[i]) != None:
            nowMode = 'HAN_KATAKANA'
        elif re.match(u"[。、！？―（）・…]", _str[i]) != None:
            nowMode = 'ZEN_KIGOU'
        elif re.match(u"[\.,!\?\-\(\)]", _str[i]) != None:
            nowMode = 'HAN_KIGOU'
        elif re.match(u"[ﾞﾟ]", _str[i]) != None:
            nowMode = 'OTHER'
            if preMode == 'HAN_KATAKANA':
                nowMode = preMode
        elif re.match(u"[a-zA-Z]", _str[i]) != None:
            nowMode = 'ALPHABET'
        elif re.match(u"[0-9]", _str[i]) != None:
            nowMode = 'HAN_NUMBER'
        elif re.match(u"[０-９]", _str[i]) != None:
            nowMode = 'ZEN_NUMBER'
        else:
            nowMode = 'OTHER'
            
        if nowMode == 'OTHER': continue

        if nowMode != preMode:
            morphList.append(_str[i])
            index += 1
        else:
            morphList[index]+=_str[i]

        preMode = nowMode
    return morphList

# 形態素の解析
def AddMorph(_str, dat_file, _wrdList):
    m_str = Morph(_str)
    if m_str == []: return []

    f = open(dat_file,'a')
    for i in m_str:
        f.write(i.encode("utf-8")+"\n")
    f.close()

    _wrdList.append([_wrdList[-1][-1],m_str[0]])
    _wrdList += NGramList(m_str)

    return m_str
    
# ルーレットを作る
def MakeRouret(_wrdList, iniChar):
    rouret = []
    iniList = [x[0] for x in _wrdList]

    if not iniChar in iniList:
        return []

    index = iniList.index(iniChar)
    while iniChar == iniList[index]:
        rouret.append(index)
        index += 1
        if index >= len(iniList)-1:
            break
    
    return rouret


# main
lines,dat_file = FOpen('save/ai6.txt')
wrdList = NGramList(Morph("".join(lines.split("\n"))))

print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while True:
    s = raw_input("あなた：").decode('utf-8')
    if s == '': continue

    s_morphs = AddMorph(s, dat_file, wrdList)

    iniList = []
    for i in range(len(s_morphs)):
        iniList += MakeRouret(wrdList, s_morphs[i])

    msg = ''
    cnt = 0
    iniIndex = 0
    while cnt == 0 or (not wrdList[iniIndex][0][-1] in [u'。',u'！',u'？',u'!',u'?',u'.'] and cnt <= 20):
        if not iniList: iniIndex = random.randint(0,len(wrdList)-1)
        else: iniIndex = random.choice(iniList)
        msg += wrdList[iniIndex][0]
        cnt += 1
        iniList = MakeRouret(wrdList, wrdList[iniIndex][1])

    print u"アリーチェ："+msg

print "アリーチェ：ばいば〜い"

