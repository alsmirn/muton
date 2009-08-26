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

    version = '0.20090826'

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
   
    -c tag and folder Selects all files which has ad (admission) in tag and 
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
    
    parser = OptionParser()
#    option_list = [
#        make_option('-e', '--export', type='bool', 
#            action='store_const', const=0, 
#            dest='action', default=False,
#            help='export tags into specified file'),
#    ]
#    parser = OptionParser(option_list=option_list)
    options, args = parser.parse_args()

    #@TODO: use callbacks from optparse lib to rewrite console control system 

    if not len(args):
        app = App()
        gtk.main()
    else:
        parser.error("incorrect number of arguments")
        
