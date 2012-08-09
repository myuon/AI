#! /usr/bin/python
#-*- coding:utf-8 -*-

import random
import sys
import re

import Alice_AI

if __name__ == "__main__":
    AI = []
    AI.append(Alice_AI.AliceEngine("save/alice_2.txt",u"Alice"))
    AI.append(Alice_AI.AliceEngine("save/bob_2.txt",u"Bob"))

    input = u""
    while True:
        input = AI[0].mainloop(input)
        input = AI[1].mainloop(input)

