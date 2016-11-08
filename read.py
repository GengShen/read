# coding: utf-8
import sys
import os
import time
import re
from ydcv import lookup_word

sep_dict = {'sentence': '.', 'line': '\n', }


class read:

    def __init__(self, file_name, mode='normal', sep='.'):
        self.file_name = file_name
        self.mark = '='*10+'\n'
        file_content = open(file_name, 'r').read().split(self.mark)
        self.contents = file_content[0].split(sep)
        self.length = len(self.contents)
        self.loop_flag = True
        self.mode = mode
        self.sep = sep
        self.mark_num = 0
        self.note = 'note:'
        if len(file_content) == 3:
            self.mark_num = int(file_content[1].split(':')[0])
            self.note = file_content[2]

    def print_line(self, e):
        os.system("clear")
        sys.stdout.write(' '*50+'\r')
        sys.stdout.flush()
        sys.stdout.write('\n'*20 + '\t'*2+e.replace('\n', '\\')+'\n\r')
        sys.stdout.flush()

    def start(self):
        start_num = self.mark_num
        for n in range(start_num, self.length):
            self.mark_num = n
            self.i = self.contents[n]
            self.print_line(self.i)
            word = raw_input("\r")
            self.wait_do(word)
            if not self.loop_flag:
                break
            if self.mode == 'rewrite':
                self.rewrite(re.findall('\\b\\w+\\b', self.i))
            elif self.mode == 'note':
                self.write_note()
        self.exit_do()
        print '阅读结束。'

    def write_note(self):
        content = raw_input(self.note)
        if content == 'exit':
            self.exit_do()
        self.note += content

    def wait_do(self, word):
        if word == '':
            pass
        elif word == 'exit':
            self.exit_do()
        else:
            os.system("python ydcv.py "+word)
            word = raw_input('\r')
            self.wait_do(word)

    def rewrite(self, lst):
        if len(lst) == 0:
            return
        words = lst
        words = [i.lower() for i in words]
        os.system("clear")
        w = raw_input('\n'*20 + '\t'*2 + 'rewrite:')
        if w == '':
            return
        elif w == 'exit':
            self.exit_do()
        write_words = w.split()
        if words == write_words:
            return
        else:
            o = [i for i in words if i not in write_words]
            x = raw_input()
            self.print_line(' '.join(o)+'\n'+self.i)
            word = raw_input("\r")
            if len(o) == 0:
                return
            else:
                self.rewrite(words[words.index(o[0]):])

    def exit_do(self):
        w_content = self.sep.join(self.contents)
        mode = self.mode
        num = self.mark_num
        for i in sep_dict:
            if sep_dict[i] == self.sep:
                sep = i
                break
        f = open(self.file_name, 'w')
        f.write(w_content+'\n')
        f.write(self.mark)
        f.write(str(num) + ':'+mode+':'+sep+'\n')
        f.write(self.mark)
        f.write(self.note)
        f.close()
        self.loop_flag = False

# argvs: file_name,mode,sep
# mode:normal,rewrite,note
# sep: sentence,line
if __name__ == '__main__':
    file_name = sys.argv[-1]
    mode = 'normal'
    sep = sep_dict['sentence']
    if len(sys.argv) == 1:
        print 'no file name'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    if len(sys.argv) > 2:
        mode = sys.argv[2]
    if len(sys.argv) > 3:
        sep = sep_dict[sys.argv[3]]
    #
    r = read(file_name, mode, sep)
    r.start()
