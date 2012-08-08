#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
形態素の候補が複数あれば
そのうちもっとも確率の高いものを選ぶ
"""
import random
import strings
import files

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

# 文の生成に使用する形態素インデックスを決定
def DicIndex(nglist,mes,pmes):
    # 選ぶ形態素の候補
    n1,n2 = Morph(mes),Morph(pmes)
    cnd_w,cnd_w_cnt = [],[]

    for i in range(len(n1)):
        stat = strings.Findch(cnd_w,n1[i])
        if stat == []:
            if ( n1[i] in strings.OutNoun(n1)) == True:
                cnd_w += [n1[i]]
                cnd_w_cnt += [len(strings.Findch(nglist,n1[i]))*100]
            else:
                cnd_w += [n1[i]]
                cnd_w_cnt += [len(strings.Findch(nglist,n1[i]))/100]

    for i in range(len(n2)):
        stat = strings.Findch(cnd_w,n2[i])
        if stat == []:
            if ( n2[i] in strings.OutNoun(n2)) == True:
                cnd_w += [n2[i]]
                cnd_w_cnt += [len(strings.Findch(nglist,n2[i]))]
            else:
                cnd_w += [n2[i]]
                cnd_w_cnt += [len(strings.Findch(nglist,n2[i]))/100]

#    for i in range(len(cnd_w)):
#        print cnd_w[i]+":"+str(cnd_w_cnt[i])

    cnt_max=[0,0]
    for i in range(len(cnd_w)):
        if cnd_w_cnt[i]>cnt_max[0]:
            cnt_max[0]=cnd_w_cnt[i]
            cnt_max[1]=i

    return cnd_w[cnt_max[1]]

# 文の作成
def Sentence(s,ch,mes):
    # 始まりの文字を探す
    r = strings.Findch(s,ch)
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
def AddMorph(cv,fn,s,prev):
    # ユーザーの入力から形態素を切り出す
    w = Morph(cv)
    f = open(fn,'a')
    for i in w:
        f.write(i+'\n')
    f.close()

    # いま解析した形態素をリストに追加
    s += strings.NGramList(w)

    # 名詞を検索
    c = DicIndex(s,cv,prev)
#    c = random.choice(s)[0]

    return c

# main
m,fn = files.FOpen('text\\save\\mem_cut.txt')
nglist = strings.NGramList(m)

mes = ''
pmes = '私はアリーチェです。'
print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
while mes != 'さようなら':
    mes = raw_input("あなた：")
    if mes != '' and mes != 'さようなら':
        # 相手の入力を形態素解析にかける
        fr_word = AddMorph(mes,fn,nglist,pmes)
        if fr_word != '':
            ans = Answer(nglist,fr_word)
            print 'アリーチェ：'+ans
            pmes = mes
    
print "アリーチェ：ばいば〜い"

