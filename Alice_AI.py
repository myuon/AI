#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
モジュール化
"""
import random
import sys
import re

EOS = [u'。',u'！',u'？',u'!',u'?',u'.']

class StrFunctions(object):
    def __init__(self):
        pass

    def tounicode(self, _lines):
        lines = []
        for i in range(len(_lines)):
            lines.append(_lines[i].decode('utf-8'))
        return "".join(lines)
    
    def ngramlist(self, _list):
        wrdList = []
        for i in range(len(_list)-1):
            wrdList.append([_list[i],_list[i+1]])
            
        return wrdList

    def judgesentence(self, msg_list, str_mlist, pre_str_mlist):
        score = 0
        for i in str_mlist:
            if i in msg_list:
                score += 10
    
        for i in pre_str_mlist:
            if i in msg_list:
                score += 3
                
        return score

    def morphtoken(self,_str):
        morphlist = []
        nowMode = 'None'
        preMode = 'None'
        index = -1
        for i in range(len(_str)):
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
                morphlist.append(_str[i])
                index += 1
            else:
                if nowMode == 'OTHER': continue
                morphlist[index]+=_str[i]
    
            preMode = nowMode
        return morphlist

class AliceEngine(object):
    def __init__(self, _filename):
        self.strf = StrFunctions()

        self.lines, self.filename = self.readtoken(_filename)
        self.tokenlist = self.strf.ngramlist(self.strf.morphtoken(self.lines))
        
        self.userstr = u""
        self.pre_userstr = u""
    
    def readtoken(self, _filename):
        filename = ''
        if len(sys.argv)==1: filename = _filename
        else: filename = sys.argv[1]
    
        lines = open(filename,'r').readlines()
        lines = self.strf.tounicode(lines)
        
        return lines, filename

    def addtoken(self, _msg):
        _tokens = self.strf.morphtoken(_msg)
        if _tokens == []: return []
        
        if _tokens[-1] not in EOS:
            _tokens.append(u'。')
        
        f = open(self.filename,'a')
        for i in _tokens:
            f.write(i.encode("utf-8")+"\n")
        f.close()
    
        self.tokenlist.append([self.tokenlist[-1][-1],_tokens[0]])
        self.tokenlist += self.strf.ngramlist(_tokens)
    
        return _tokens
    
    def makerouret(self, iniChar):
        rouret = []
        iniList = [x[0] for x in self.tokenlist]
    
        if not iniChar in iniList: return []
    
        index = iniList.index(iniChar)
        while iniChar in iniList[index]:
            rouret.append(index)
            index += 1
            if index >= len(iniList)-1:
                break
        
        return rouret

    def makesentence(self, iniIndex):
        msg = ''
        cnt = 0
        while cnt == 0 or (not self.tokenlist[iniIndex][0][-1] in EOS and cnt <= 20):
            msg += self.tokenlist[iniIndex][0]
            cnt += 1
            iniList = self.makerouret(self.tokenlist[iniIndex][1])
            if not iniList: iniIndex = random.randint(0,len(self.tokenlist)-1)
            else: iniIndex = random.choice(iniList)
            
        return msg
    
    def makeinilist(self):
        inilist = []
        for i in self.userstr:
            inilist += self.makerouret(i)

        if self.pre_userstr != []:
            for i in self.pre_userstr:
                inilist += self.makerouret(i)
                
        if inilist == []:
            inilist = [random.randint(0,len(self.tokenlist)-1)]
        
        return inilist

    def makemessage(self, inilist):
        message = []
        for i in inilist:
            _msg = self.makesentence(i)
            message.append([_msg, self.strf.judgesentence(_msg, self.userstr, self.pre_userstr)])

        message = sorted(message, key=lambda x:x[1], reverse=True)
        return message
    
    def mainloop(self):
        while True:
            input = raw_input("あなた：").decode('utf-8')
            if input == '': continue

            self.userstr = self.addtoken(input)
        
            for i in EOS:
                while i in self.userstr: self.userstr.remove(i)
                while i in self.pre_userstr: self.pre_userstr.remove(i)

            message = self.makemessage(self.makeinilist())
            print u"アリーチェ："+message[int(random.randint(0,len(message)-1)/4)][0]

            self.pre_userstr = self.userstr

if __name__ == "__main__":
    alice = AliceEngine("save/alice.txt")

    print "アリーチェ：いらっしゃいませ〜。メッセージをどうぞ〜"
    alice.mainloop()


