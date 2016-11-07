import sys
import os
import time
import re
from ydcv import lookup_word


class read:

    def __init__(self, file_name, mode=0, sep='.'):
        self.contents = open(file_name, 'r').read().split(sep)
        self.length = len(self.contents)
        self.loop_flag = True
        self.mode = int(mode)
        if os.path.isfile(file_name.split('.')[0]+"_note"):
            self.note = open(file_name.split('.')[0]+"_note",'r').read()
        else:
            self.note = 'note:'
    def print_line(self,e):
        os.system("clear")
        sys.stdout.write(' '*50+'\r')
        sys.stdout.flush()
        sys.stdout.write('\n'*20 + '\t'*2+e.replace('\n', '\\')+'\r')
        sys.stdout.flush()
    def start(self):
        for n in range(self.length):
            self.i = self.contents[n]
            self.print_line(self.i)
            word = raw_input("\r")
            self.wait_do(word)
            if not self.loop_flag:
                break
            if self.mode == 1:
                self.rewrite(re.findall('\\b\\w+\\b',self.i))
            elif self.mode == 2:
                self.write_note()

    def write_note(self):
        content=raw_input(self.note)
        if content == 'exit':
            f = open(file_name, 'w')
            f.write('.'.join(self.contents[self.contents.index(self.i):]))
            f.close()
            f = open(file_name.split('.')[0]+"_note",'w')
            f.write(self.note)
            f.close()
            self.loop_flag = False
        self.note+=content           

    def wait_do(self, word):
        if word == '':
            pass
        elif word == 'exit':
            f = open(file_name, 'w')
            f.write('.'.join(self.contents[self.contents.index(self.i):]))
            f.close()
            self.loop_flag = False
        else:
            os.system("python ydcv.py "+word)
            word = raw_input('\r')
            self.wait_do(word)

    def rewrite(self,lst):
        if len(lst) == 0:
            return
        words = lst
        words = [i.lower() for i in words]
        os.system("clear")
        w = raw_input('\n'*20 + '\t'*2 + 'rewrite:')
        if w == '':
            return
        write_words = w.split()
        if words == write_words:
            return
        else:
            o = [i for i in words if i not in write_words]
            x =raw_input()
            self.print_line(' '.join(o)+'\n'+self.i)
            word = raw_input("\r")
            if len(o) == 0:
                return
            else:
                self.rewrite(words[words.index(o[0]):])

if __name__ == '__main__':
    file_name = sys.argv[-1]
    if len(sys.argv) > 2:
        mode = sys.argv[-2]
    r = read(file_name,mode)
    r.start()
