#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, getopt, sys
from distutils import file_util
from distutils import dir_util
import collection
import tag_writer
import outputter
import renamer

print (time.ctime())

class FileCopierBySign():
    """Makes the extraction in the media collection and copies to the specified
    folder files with the specified genre or another parameter"""
    
    def __init__(self, collection):
        self.collection = collection
                       
    def copy(self, output_path, info_type, search_item):
        restr_symbols = '|', ':', '\\', '/', '?', '<', '>', '*', '"'
        win_depr_punct = ' ', '..', '...'
        
        for k, v in self.collection.items():
            """Creates for each artist and album separate folder and copies
            files to them"""           
            try:
                a = v['artist']
            except TypeError:
                print ("%r is not a valid audio file") % (k, )
                return            
            if v[info_type].find(search_item) != - 1:
                
                #Stripping restricted symbols in artist and album name  
                for rs in restr_symbols:
                    if v['artist'].find(' ' + rs) != - 1:
                        v['artist'] = v['artist'].replace(rs, '')
                    elif v['artist'].find(rs) != - 1:
                        v['artist'] = v['artist'].replace(rs, '')

                    if v['album'].find(' ' + rs) != - 1:
                        v['album'] = v['album'].replace(rs, '')
                    elif v['album'].find(rs) != - 1:
                        v['album'] = v['album'].replace(rs, '')

                for wdp in win_depr_punct:
                    v['artist'] = v['artist'].lstrip(wdp).rstrip(wdp)
                    v['album'] = v['album'].lstrip(wdp).rstrip(wdp)
                            
                #Making path for the extraction    
                file_path = os.path.join(output_path, v['artist'].decode('utf-8'),
                v['year'] + ' ' + v['album'].decode('utf-8'))
                dir_util.mkpath(file_path)
                #Copying files
                if v['artist'] != '' and v['album'] != '' and v['year'] != '':
                    file_util.copy_file(k, file_path, 'update = true')
                    
def cmd(argv):
    pattern = '%track% - %artist% - %title%'
   
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
            extract = FileCopierBySign(c)
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
                            
if __name__ == "__main__":
    """
    our "main()" calls:
    - scanner()
    - collection()
    - scannedInfoWriter()
    - FileCopierBySign
    - writer()
    - tagWriteManager()
    """

    scanner = collection.MediaScanner()
    c = scanner.scan(u"e:\\Music\\Test")
#    for path, v in c.items():
#        print path, v
        
    write_tags = tag_writer.TagWriteManager(c)
    extract = FileCopierBySign(c)
    wr_output = outputter.ScannedInfoWriter(c)   
    rename = renamer.Renamer(c)
    
    cmd(sys.argv[1:])

    wr_output.write(u'E:\\My Documents\\', 'album', 'xml')
    #scan_albums.scan()
    #rename.manager('recursive', '', '%artist% - %title%')
    #extract.copy('F:\\', 'genre', 'Post-Rock')
    ##write_tags.tag_write_man('single', u'E:\\Test\\test\\02 - October Tide - Rain Without End.mp3', 'album', 'album!!!')
    #test
    print (time.ctime())