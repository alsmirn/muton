#!/usr/bin/env python

import time, getopt, sys

import collection
import tag_writer
import outputter
import renamer
import copy_pick

def main():

    scanner = collection.MediaScanner()
    c = scanner.scan(u"/home/alexey/ChrisGoesRock/")
        
    write_tags = tag_writer.TagWriteManager(c)
    extract = copy_pick.FileCopierBySign(c)
    wr_output = outputter.ScannedInfoWriter(c)   
    rename = renamer.Renamer(c)
    
    pattern = '%track% - %artist% - %title%'
   
    argv = sys.argv[1:]
    try:                                
        opts, args = getopt.getopt(argv, 'tewrp:o:n:s:m:f:g:c:', ['extr', \
        'export', 'wr_tags', 'rename', 'path=', 'o_path=', 'pattern=', \
        'new_str=', 'mode=', 'f_type=', 'tag_type=', 'search_item='])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        scanner = collection.MediaScanner()
        if opt in ('-p', '--path'):
            path = unicode(arg)
            c = scanner.scan(path)
        elif opt in ('-o', '--out_path'):
            out_path = unicode(arg)
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
        if opt in ('-t', '--extr'):
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
                       
    wr_output.write(u'information_chris_goes_rock', 'album', 'csv')
    
    #scan_albums.scan()
    #rename.manager('recursive', '', '%artist% - %title%')
    #extract.copy('F:\\', 'genre', 'Post-Rock')
    ##write_tags.tag_write_man('single', u'E:\\Test\\test\\02 - October Tide - Rain Without End.mp3', 'album', 'album!!!')    
                            
if __name__ == "__main__":

    time_start = time.ctime()    
    
    sys.exit(main())
    
    print 'Execution time is %d seconds.' % (time_start - time.ctime(),)
