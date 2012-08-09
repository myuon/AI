#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
乱択アルゴリズムと評価函数で次の文章を選択する
文末終了判定を追加
"""
import random
import sys
import re

EOS = [u'。',u'！',u'？',u'!',u'?',u'.']

# ファイル関係
def fOpen(_file):
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
def nGramList(_list):
    wrdList = []
    for i in range(len(_list)-1):
        wrdList.append([_list[i],_list[i+1]])
        
    return wrdList

#形態素の切り出し
def morph(_str):
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
        elif re.match(u"[。、！？―〜（）・…]", _str[i]) != None:
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
            
        if nowMode == 'OTHER':
            preMode = nowMode
            continue

        if nowMode != preMode:
            morphList.append(_str[i])
            index += 1
        else:
            if nowMode == 'OTHER': continue
            morphList[index]+=_str[i]

        preMode = nowMode
    return morphList

# 形態素の解析
def addMorph(_str, dat_file, _wrdList):
    m_str = morph(_str)
    if m_str == []: return []
    
    if m_str[-1] not in EOS:
        m_str.append(u'。')
    
    f = open(dat_file,'a')
    for i in m_str:
        f.write(i.encode("utf-8")+"\n")
    f.close()

    _wrdList.append([_wrdList[-1][-1],m_str[0]])
    _wrdList += nGramList(m_str)

    return m_str
    
# ルーレットを作る
def makeRouret(_wrdList, iniChar):
    rouret = []
    iniList = [x[0] for x in _wrdList]

    if not iniChar in iniList:
        return []

    index = iniList.index(iniChar)
    while iniChar in iniList[index]:
        rouret.append(index)
        index += 1
        if index >= len(iniList)-1:
            break
    
    return rouret

def makeSentence(iniIndex):
    msg = ''
    cnt = 0
    while cnt == 0 or (not wrdList[iniIndex][0][-1] in EOS and cnt <= 20):
        msg += wrdList[iniIndex][0]
        cnt += 1
        iniList = makeRouret(wrdList, wrdList[iniIndex][1])
        if not iniList: iniIndex = random.randint(0,len(wrdList)-1)
        else: iniIndex = random.choice(iniList)
    return msg

def judgeSentence(msg_list, str_mlist, pre_str_mlist):
    score = 0
    for i in str_mlist:
        if i in msg_list:
            score += 10

    for i in pre_str_mlist:
        if i in msg_list:
            score += 3
            
    return score

# main
lines,dat_file = fOpen('save/ai10.txt')
wrdList = nGramList(morph(lines))
pre_morphs = []

print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while True:
    s = raw_input("あなた：").decode('utf-8')
    if s == '': continue

    now_morphs = addMorph(s, dat_file, wrdList)

    for i in EOS:
        while i in now_morphs: now_morphs.remove(i)

    for i in EOS:
        while i in pre_morphs: now_morphs.remove(i)
        
    iniList = []
    for i in range(len(now_morphs)):
        iniList += makeRouret(wrdList, now_morphs[i])

    if pre_morphs != []:
        for i in range(len(pre_morphs)):
            iniList += makeRouret(wrdList, pre_morphs[i])
            
    if iniList == []:
        iniList = [random.randint(0,len(wrdList)-1)]

    msg = []
    for i in range(len(iniList)):
        _msg = makeSentence(iniList[i])
        msg.append([_msg, judgeSentence(_msg, now_morphs, pre_morphs)])

    msg = sorted(msg, key=lambda x:x[1], reverse=True)

    pre_morphs = now_morphs

    print u"アリーチェ："+msg[int(random.randint(0,len(msg)-1)/4)][0]
