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
    
    python muton.py [COMMANDS] path_to_collection
    
    COMMANDS:

    #0 Scan process is running always if in command line specified #1,2 or 3 
    blocks. This -s option is not obligatory, it uses when you want specifie 
    musical files format. 

    -s                Scan tags in specified format (by default all formats)
    --format f1,f2,   Adjustment of format (mp3, flac, ape)
    

    #1 Scan all files and write tags information on standard output (custom).

    -w                Writes all tags to standard output in custom format 
                      (default format is CSV).
    -f filename       Means "file", specifies output file
    --format fmt_name Set format of output ('album', 'atom')
                      @TODO normal output_mode in outputter module.
                      

    #2 Scan all files and rename by (custom) template.

    -rn               Rename files by template
                      (default template is: '%track% - %artist% - %title%').
    --template "t"    Specifies custom template.
    

    #3 Scan all files and copy selected by tag files to specified folder.

    -cp tag ad folder Select all files which has ad (admission) in tag and copy 
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
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 'tewro:n:s:m:f:g:c:',
                ['extr', 'export', 'wr_tags', 'rename',
                'o_path=', 'pattern=', 'new_str=', 'mode=',
                'f_type=', 'tag_type=', 'search_item='])
        except getopt.GetoptError, msg:
            raise Usage(msg)

        for opt, arg in opts:
            elif opt in ('-t', '--extr'):
                extract = copy_pick.FileCopierBySign(c)
                extract.copy(out_path, tag_type, search_item)
            elif opt in ('-e', '--export'):
                wr_output = outputter.ScannedInfoWriter(c)
                wr_output.write(out_path, mode, f_type)
            elif opt in ('-w', '--wr_tags'):
                write_tags = tag_writer.TagWriteManager(c)
                write_tags.tag_write_man(path, mode, tag_type, new_str)
            elif opt in ('-r', '--rename'):
                rename = renamer.Renamer(c)
                rename.manager(mode, '', pattern)
            elif opt in ('-o', '--out_path'):
                if os.path.isdir(arg):
                    out_path = unicode(arg)
                else:
                    print arg, "is not a directory!"
            elif opt in ('-n', '--pattern'):
                pattern = arg
            elif opt in ('-s', '--new_str'):
                new_str = arg
            elif opt in ('-m', '--mode'):
                mode = arg
            elif opt in ('-f', '--f_type'):
                f_type = arg
            elif opt in ('-g', '--tag_type'):
                tag_type = arg
            elif opt in ('-c', '--search_item'):
                search_item = arg

        scanner = collection.MediaScanner()
        # Treat arg as possible path for scan
        for arg in args:
            if os.path.isdir(arg):
                path = unicode(arg)
                c = scanner.scan(path)
            else:
                print arg, "is not a directory!"
        if args == []:
            #If no path specified, search in current derectory
            c = scanner.scan(os.getcwd())
            #c = scanner.scan(u"/home/alexey/ChrisGoesRock/")

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "use --help ;)"
        return 2

    scanner = collection.MediaScanner()
    #write_tags = tag_writer.TagWriteManager(c)
    #extract = copy_pick.FileCopierBySgn(c)
    wr_output = outputter.ScannedInfoWriter(c)
    #rename = renamer.Renamer(c)
    #pattern = '%track% - %artist% - %title%'

    #What's this?
    wr_output.write(u'information_chris_goes_rock', 'album', 'xml')

    #scan_albums.scan()
    #rename.manager('recursive', '', '%artist% - %title%')
    #extract.copy('F:\\', 'genre', 'Post-Rock')
    ##write_tags.tag_write_man('single', u'E:\\Test\\test\\02 - October Tide - Rain Without End.mp3', 'album', 'album!!!')

if __name__ == "__main__":

    time_start = time.ctime()

    sys.exit(main())
    #This code don't work ;)
    print 'Execution time is %d seconds.' % (time_start - time.ctime(),)
