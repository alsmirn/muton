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
                      (default format is XML).
    -f filename       Means "file", specifies output file
    --format fmt_name Set format of output ('album', 'atom')
                      @TODO normal output_mode in outputter module.
   
    -n                Renames files by template
                      (default template is: '%track% - %artist% - %title%').
    --template "t"    Specifies custom template.
    
    -c tag ad folder  Selects all files which has ad (admission) in tag and copy 
                      to specified folder
    -o output path    Folder to copy files      

    -r                Writes text to specified tags in:
                      a) specified files;
                      b) all files in specified folder.
    
    """

def main(argv=None):
    """
    Main function, curiously enough ;)
    """

    """
    Needs rewrite according Usage message
    """
    time_start = time.time()
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            optlist, args = getopt.getopt(argv[1:], 'vhwnrcf:t:o:z', 
            ['version', 'help', 'format=', 'template='])
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
            #If no path specified, search in current directory
            path = os.getcwd()

        for opt, arg in optlist:
            if opt in ('-v', '--version'):
                print Usage.version
                sys.exit()
            elif opt in ('-h', '--help'):
                raise Usage('')
            elif opt in ('-o', '--out_path'):
                out_path = unicode(arg)
            elif opt in ('-g', '--tag_type'):
                tag_type = arg       
            elif opt in ('-s', '--search_item'):
                search_item = arg   
            elif opt in ('-w', ):
                scanner = collection.MediaScanner()
                c = scanner.scan(path)
                wr_output = outputter.ScannedInfoWriter(c)
                wr_output.write(u'E:\\', 'album', 'xml')
            elif opt in ('-n', ):
                scanner = collection.MediaScanner()
                c = scanner.scan(path)
                rename = renamer.Renamer(c)
                rename.manager('recursive', '', '%track% - %artist% - %title%')
            elif opt in ('-c', ):
                scanner = collection.MediaScanner()
                c = scanner.scan(path)    
                extract = copy_pick.FileCopierBySign(c)
                extract.copy(u'E:\\', 'genre', 'Metal')
            elif opt in ('-r', ):
                scanner = collection.MediaScanner()
                c = scanner.scan(path) 
                write_tags = tag_writer.TagWriteManager(c)
                write_tags.tag_write_man('single', u'E:\\Test\\test\\04 - Ashes of Your Enemy - Binge & Purge.Mp3', 'album', 'alb!!!')

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "use --help ;)"
        return 2

    print 'Execution time is %3.1f seconds.' % (time.time() - time_start,)

#    scanner = collection.MediaScanner()
#    c = scanner.scan(u'E:\\Test\\test')
#    
#    write_tags = tag_writer.TagWriteManager(c)
    #extract = copy_pick.FileCopierBySign(c)


    #if wrout_set != 0:
        #wr_output = outputter.ScannedInfoWriter(c)
        #wr_output.write(u'information_chris_goes_rock', 'album', 'xml')
        
        
    #rename = renamer.Renamer(c)
    #pattern = '%track% - %artist% - %title%'
    #scan_albums.scan()
    #rename.manager('recursive', '', '%artist% - %title%')
    #extract.copy('E:\\', 'genre', 'Metal')
    #write_tags.tag_write_man('single', u'E:\\Test\\test\\02 - October Tide - Rain Without End.mp3', 'album', 'album!!!')


if __name__ == "__main__":

    sys.exit(main())
    