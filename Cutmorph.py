#! /usr/bin/python
#-*- coding:utf-8 -*-


"""
文章の解析
  ->形態素解析
"""

import re
import sys

# ファイル関係
def FOpen(_file):
    dat_file = ''
    if len(sys.argv)==1: dat_file = _file
    else: dat_file = sys.argv[1]

    f = open(dat_file,'r')
    lines = f.readlines()
    
    return lines,dat_file

# unicode変換
def toUnicode(_lines):
    lines = []
    for i in range(len(_lines)):
        lines.append(_lines[i].decode('utf-8'))
    return lines

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
            nowMode = 'KANJI'
        elif re.match(u"[ぁ-ゞ]", _str[i]) != None:
            nowMode = 'HIRAGANA'
        elif re.match(u"[ァ-ヾ]", _str[i]) != None:
            nowMode = 'KATAKANA'
        elif re.match(u"[ｦ-ﾝ]", _str[i]) != None:
            nowMode = 'HANKANA'
        elif re.match(u"[。、！？―（）\.,!\?\-\(\)…・]", _str[i]) != None:
            nowMode = 'KIGOU'
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

# main
lines,dat_file = FOpen(u'text/sample.txt')
lines = toUnicode(lines)
lines = "".join(lines)

morph = Morph(lines)

fn = u'save/m_'+dat_file.split('/')[-1]+'.txt'
f = open(fn,'w')
for i in morph:
    f.write(i.encode("utf-8")+"\n")
f.close()

