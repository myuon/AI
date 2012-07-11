#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Pythonで人工知能…人工無能？

"""
print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"

s = ''
while s != 'exit' :
    s = raw_input("あなた：")
    if s != '' and s != 'exit' : print "アリーチェ：ふ〜ん、それで？"

print "アリーチェ：ばいば〜い"

