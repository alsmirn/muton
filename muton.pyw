#!/usr/bin/env python

import os
import sys
import time
import getopt
from optparse import OptionParser

import gtk
import pygtk
import gtk.glade

import collection
import tag_writer
import outputter
import renamer
import copy_pick

pygtk.require('2.0')

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
    -e                Exports info from tags to standard output in custom format 
                      (default format is XML).
                      For example: muton.exe -o e:\ -e d:\Downloads
                      It will export info from files in path "d:\Downloads" to 
                      xml file in path "e:\"
   
    -n                Renames files by template
                      (default template is: '%track% - %artist% - %title%').
   
    -c tag ad folder  Selects all files which has ad (admission) in tag and 
                      copies to specified folder
                        
    -r                Writes text to specified tags in:
                      a) specified files;
                      b) all files in specified folder.
 
    -o output path    Folder to copy files                         
    -f filename       Means "file", specifies output file (temporary not avail.)
    --template "t"    Specifies custom template  (temporary not avail.)
    --format fmt_name Set format of output ('album', 'atom')  (temp. not avail.)
    """
    #@TODO: normal output_mode in outputter module.

def main(argv=None):
    """
    Main function, curiously enough ;)
    """

    """
#    Needs rewrite according Usage message
#    """
    time_start = time.time()
#    
#    if argv is None:
#        argv = sys.argv
#    try:
#        try:
#            optlist, args = getopt.getopt(argv[1:], 'vhenrcf:t:o:z', 
#            ['version', 'help', 'format=', 'template='])
#        except getopt.GetoptError, msg:
#            raise Usage(msg)
#
#        # Treat arg as possible path for scan
#        for arg in args:
#            if os.path.isdir(arg):
#                path = unicode(arg)
#                break
#            else:
#                print "%s is not a directory!" % (arg,)
#                sys.exit(True)
#        if args == []:
#            #If no path specified, search in current directory
#            path = os.getcwd()
#
#        for opt, arg in optlist:
#            if opt in ('-v', '--version'):
#                print Usage.version
#                sys.exit()
#            elif opt in ('-h', '--help'):
#                raise Usage('')
#            elif opt in ('-o', '--out_path'):
#                out_path = unicode(arg)
#            elif opt in ('-g', '--tag_type'):
#                tag_type = arg       
#            elif opt in ('-s', '--search_item'):
#                search_item = arg 
#            elif opt in ('-e', ):
#                scanner = collection.MediaScanner()
#                c = scanner.scan(path)
#                #c = cProfile.run('scanner.scan(path)', 'log')
#                wr_output = outputter.ScannedInfoWriter(c)
#                wr_output.write(out_path, 'album', 'xml')
#            elif opt in ('-n', ):
#                scanner = collection.MediaScanner()
#                c = scanner.scan(path)
#                rename = renamer.Renamer(c)
#                rename.manager('recursive', '', '%track% - %artist% - %title%')
#            elif opt in ('-c', ):
#                scanner = collection.MediaScanner()
#                c = scanner.scan(path)    
#                extract = copy_pick.FileCopierBySign(c)
#                extract.copy(u'E:\\', 'genre', 'Metal')
#            elif opt in ('-r', ):
#                scanner = collection.MediaScanner()
#                c = scanner.scan(path) 
#                write_tags = tag_writer.TagWriteManager(c)
#                write_tags.tag_write_man('single', u'E:\\Test\\test\\04 - Ashes of Your Enemy - Binge & Purge.Mp3', 'album', 'alb!!!')
#            else:
#                assert False, "unhandled option"
#
#    except Usage, err:
#        print >>sys.stderr, err.msg
#        return 2



    print 'Execution time is %3.1f seconds.' % (time.time() - time_start,)

#    scanner = collection.MediaScanner()
#    c = scanner.scan(u'E:\\New Music')
#    c = cProfile.runctx("scanner.scan(u'E:\\Test')", globals(), locals(), 'log')
#    p = pstats.Stats('log')
#    p.strip_dirs().sort_stats('calls').print_stats(20)
#    p.sort_stats('calls').print_callers(.5, 'init')
#    p.sort_stats('cumulative').print_stats(10)


#    wr_output = outputter.ScannedInfoWriter(c)
#    wr_output.write(u'e:\\', 'album', 'xml')
#    
#    write_tags = tag_writer.TagWriteManager(c)
    #extract = copy_pick.FileCopierBySign(c)       
        
    #rename = renamer.Renamer(c)
    #pattern = '%track% - %artist% - %title%'
    #scan_albums.scan()
    #rename.manager('recursive', '', '%artist% - %title%')
    #extract.copy('E:\\', 'genre', 'Metal')
    #write_tags.tag_write_man('single', u'E:\\Test\\test\\02 - October Tide - Rain Without End.mp3', 'album', 'album!!!')

class App:
    """This class makes the GUI interface on the basis of the glade XML files"""
    
    def __init__(self):
        #By now it's only for export, so the name is
        self.main_xml = "glade_files/export.glade"        
        #Parsing the glade xml file
        self.wTree = gtk.glade.XML(self.main_xml)       
        #Dictionary for the export button action
        dic = { 
        "exp_click" : self.export,
          }

        self.wTree.signal_autoconnect(dic)
        #Making close equal to destroy
        self.dialog = self.wTree.get_widget("dialog1")
        if (self.dialog):
            self.dialog.connect("destroy", self.close_app)
            
    def export(self, widget):
        """By now I realized only one possibility of muton"""
        #Getting values from text fields 
        path = self.wTree.get_widget('path_entry').get_text()
        out_path = self.wTree.get_widget('out_path_entry').get_text()
        format = self.wTree.get_widget('format').get_active_text().lower()
        #Executing export
        scanner = collection.MediaScanner()
        c = scanner.scan(unicode(path))
        wr_output = outputter.ScannedInfoWriter(c)
        wr_output.write(out_path, 'album', format)

        
    def close_app(self, widget):    
        gtk.main_quit()    
        
if __name__ == "__main__":

    app = App()
    gtk.main()
