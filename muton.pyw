#!/usr/bin/env python

import os
import sys
import time
import getopt
from optparse import Option, OptionGroup, OptionParser

import gtk
import pygtk
import gtk.glade

import collection
import tag_writer
import outputter
import renamer
import copy_pick

pygtk.require('2.0')


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


def _tag_export_callback(option, opt, value, parser):
    
    parser.rargs = filter(lambda x: not x.startswith('-'), parser.rargs)

    if len(parser.rargs) == 2:
        scanner = collection.MediaScanner()
        c = scanner.scan(unicode(parser.rargs[0]))
        wr_output = outputter.ScannedInfoWriter(c)
        wr_output.write(parser.rargs[1], parser.values.resolution, 
            parser.values.fmt)
        sys.exit(0)
    elif len(parser.rargs) < 2:
        print 'Not enough arguments to run export'
        sys.exit(1)
    else:
        print 'Too much arguments to run export'
        print 'Note: additional parameters goes before main...'
        sys.exit(1)

def _init_parser():
    parser = OptionParser(version="%prog 0.20090827",
        usage="%prog [SECONDARY OPTIONS] (PRIMARY OPTIONS) ARGS\n"
        "Usage note: without options and args start graphical interface")

    primary_group = OptionGroup(parser, "PRIMARY OPTIONS")
    secondary_group = OptionGroup(parser, "SECONDARY OPTIONS")

    primary_group.add_option('-e', action='callback', 
        callback=_tag_export_callback,
        help="exports info from tags to specified file in custom format.\n"
            "ARGS: path_to_collection path_to_output_file.fmt"),
    
    secondary_group.add_option('--fmt', type='choice', dest='fmt', 
        default='xml', choices=['xml', 'csv'], 
        help='specifies format of output collection description'),
    #@TODO: using incrementation
    secondary_group.add_option('--res', type='choice', dest='resolution', 
        default='album', choices=['album', ],
        help='specifies resolution of output collection description'),
    
    parser.add_option_group(primary_group)
    parser.add_option_group(secondary_group)
    
    return parser

def _controller():
    
    if len(sys.argv) == 1:
        # graphical interface call
        app = App()
        gtk.main()
    else:
        # command line usage
        _init_parser().parse_args()

if __name__ == "__main__":
    sys.exit(_controller())
    