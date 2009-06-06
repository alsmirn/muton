#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, getopt, os, sys

import collection
import tag_writer
import outputter
import renamer
import copy_pick

class Usage(Exception):
    """Usage class ;)
    """

    version = '0.20090520'

    def __init__(self, msg):
        self.msg = \
    """
    Command line feature design:
    
    python muton.py (COMMANDS) one_path_to_collection
    
    COMMANDS:
    -w                Writes all tags to standard output in custom format 
                      (default format is CSV).
    -f filename       Means "file", specifies output file
    --format fmt_name Set format of output ('album', 'atom')
                      @TODO normal output_mode in outputter module.

    -n                Rename files by template
                      (default template is: '%track% - %artist% - %title%').
    --template "t"    Specifies custom template.
    
    -c tag ad folder  Select all files which has ad (admission) in tag and copy 
                      to specified folder
                      
    
    #4 Manual tags rewriting...
    """

def main(argv=None):
    """
    Main function ;)
    """

    """
    Needs rewrite according Usage message
    """
    time_start = time.time()
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            optlist, args = getopt.getopt(argv[1:], 'vhwf:z', 
                                          ['version', 'help', 'format=', ])
        except getopt.GetoptError, msg:
            raise Usage(msg)

        # Treat arg as possible path for scan
        for arg in args:
            if os.path.isdir(arg):
                path = unicode(arg)
                break
            else:
                print "%s is not a directory!" % (arg,)
                sys.exit(True)
        if args == []:
            #If no path specified, search in current derectory
            path = os.getcwd()

        for opt, arg in optlist:
            if opt in ('-v', '--version'):
                print Usage.version
                sys.exit()
            elif opt in ('-h', '--help'):
                raise Usage('')
            elif opt in ('-w', ):
                scaner = collection.MediaScanner()
                c = scaner.scan(path)
                wr_output = outputter.ScannedInfoWriter(c)
                wr_output.write(u'chris_goes_rock', 'album', 'xml')

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "use --help ;)"
        return 2

    print 'Execution time is %3.1f seconds.' % (time.time() - time_start,)

    #scanner = collection.MediaScanner()
    #write_tags = tag_writer.TagWriteManager(c)
    #extract = copy_pick.FileCopierBySign(c)


    #if wrout_set != 0:
        #wr_output = outputter.ScannedInfoWriter(c)
        #wr_output.write(u'information_chris_goes_rock', 'album', 'xml')
        
        
    #rename = renamer.Renamer(c)
    #pattern = '%track% - %artist% - %title%'
    #scan_albums.scan()
    #rename.manager('recursive', '', '%artist% - %title%')
    #extract.copy('F:\\', 'genre', 'Post-Rock')
    ##write_tags.tag_write_man('single', u'E:\\Test\\test\\02 - October Tide - Rain Without End.mp3', 'album', 'album!!!')


if __name__ == "__main__":

    sys.exit(main())
    