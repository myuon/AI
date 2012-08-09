#! /usr/bin/python
#-*- coding:utf-8 -*-

import re
import sys

r = open(sys.argv[1], 'r')
w = open(sys.argv[1]+".txt", 'w')

BAN = ["RT"]
EOS = [u'。',u'！',u'？',u'!',u'?',u'.']

l = "aaa"
while l != u"":
    l = r.readline().decode('utf-8')
    
    if l != u"" and l[0] == u"\"" and l[1:4].isdigit():
        ls = l.split(u",")[2][1:-2]
        ls = ls.split(u" ")
        while u"RT" in ls: ls.remove(u"RT")
        out = []
        for i in ls:
            if re.match(u"^@.*", i) == None:
                out.append(i)
        out = "".join(out)
        out = "".join(out.split(u"&gt;"))
        out = "".join(out.split(u"&lt;"))

        if out != u"":
            if out[-1] not in EOS: out += u"。"

            w.write(out.encode('utf-8')+"\n")

r.close()
w.close()

