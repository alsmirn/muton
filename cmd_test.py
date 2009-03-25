# -*- coding: utf-8 -*-

import sys, getopt
from optparse import OptionParser


class My():
    def __init__(self, s, n):
        self.s = s
        self.n = n
    def pr(self):
        print self.s
        print self.n

def usage():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--extr",
                  help="Extracts media file by the sign from the tag") 

        
def main(argv):
    s = 'dfd'
    n = 'Sasha'
    try:                                
        opts, args = getopt.getopt(argv, 'hs:n:', ['help', 'strs=', 'name='])
    except getopt.GetoptError:
        usage()           
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()                     
            sys.exit() 
        elif opt in ('-s', '--strs'):
            s = arg
    for opt, arg in opts:
        if opt in ('-n'):
            n = arg
    pr = My(s, n)
    pr.pr()

if __name__ == "__main__":
    main(sys.argv[1:])

  
  
