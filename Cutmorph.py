#! /usr/bin/python
#-*- coding:utf-8 -*-


"""
文章の解析
  ->形態素解析
"""
# 全角文字だけ抜き出して、すべて突っ込む
def GetWideChar(lines,wide):
    for i in range(len(lines)):
        n = 0
        while n < len(lines[i])-1:
            tip = ''
            l = lines[i][n]
            if (l>'\x7F' and l<'\xA0') or (l>'\xDF' and l<'\xF0'):
                tip += lines[i][n]
            tip += lines[i][n+1]
            if tip != '　' :
                wide[0] += tip
            n += 2
    return

#形態素の切り出し
def Morph(wide):
    m,prev = '',''
    tmp = wide[0]
    mor = []
    pm = -1
    for i in range(0,len(tmp),2):
        ch = tmp[i]+tmp[i+1]
        # 長音「ー」は前の形態に引っ張られる
        if ch == 'ー':
            m = prev
        elif tmp[i]>='\x88':
            m = 'c'
        elif tmp[i]=='\x83' and 40<=tmp[i+1]<='\x96':
            m = 'k'
        elif ch=='.' or ch==',' or ch=='。' or ch=='、':
            m = 'n'
        else:
            m = 'e'

        if m != prev and m != 'n':
            mor += [tmp[i]+tmp[i+1]]
            pm += 1
        else:
            mor[pm] += tmp[i]+tmp[i+1]
        prev = m
    return mor

# main
s = raw_input("ファイル名:")
if s == '':
    s = 'text\cut.txt'
f = open(s,'r')
lines = f.readlines()

wide = ['']
GetWideChar(lines,wide)
wide = Morph(wide)

fn = 'text\save\morph_'+s[s.index('\\')+1:-4]+'.txt'
f = open(fn,'w')
for i in wide:
    f.write(i+'\n')
    print i
f.close()

