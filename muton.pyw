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

def _tag_export_execute(path_to_collection, path_to_output, grouping, format):
    time_beg = time.time()
    scanner = collection.MediaScanner()
    c = scanner.scan(unicode(path_to_collection))
    wr_output = outputter.ScannedInfoWriter(c)
    wr_output.write(path_to_output, grouping, format)
    print 'Tag export execution time %3.1f seconds.' % (time.time() - time_beg, )
    return 0

def _tag_export_callback(option, opt, value, parser):

    required_args_num = 2
    parser.rargs = filter(lambda x: not x.startswith('-'), parser.rargs)

    if len(parser.rargs) == required_args_num:
        return _tag_export_execute(parser.rargs[0], parser.rargs[1], 
            parser.values.grouping, parser.values.fmt)
    elif len(parser.rargs) < required_args_num:
        print 'Not enough arguments to run export'
    else:
        print 'Too much arguments to run export'
        print 'Note: additional parameters goes before main...'
        
    return 1


class App:
    """This class makes the GUI interface on the basis of the glade XML files
    """
    
    def __init__(self):
        #By now it's only for export, so the name is
        self.main_xml = "glade_files/export.glade"        
        #Parsing the glade xml file
        self.wTree = gtk.glade.XML(self.main_xml)       
        #Dictionary for the export button action
        dic = {"exp_click" : self.export}

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
        extension = self.wTree.get_widget('format').get_active_text().lower()
        grouping = self.wTree.get_widget('grouping').get_text().lower()
        #Executing export
        _tag_export_execute(path, out_path, grouping, extension)
        
    def close_app(self, widget):    
        gtk.main_quit()    


def _init_parser():
    #@TODO: catch exception when user instead of folder name specifies filename 
    parser = OptionParser(version="%prog 0.20090827",
        usage="%prog [AUXILIARY OPTIONS] (OPTIONS) ARGS\n"
        "Usage note: without options and args start graphical interface")

    parser.add_option('-e', action='callback', 
        callback=_tag_export_callback,
        help="exports info from tags to specified file in custom format.\n"
            "ARGS: path_to_collection path_to_output_file.fmt"),
    
    auxiliary_group = OptionGroup(parser, "AUXILIARY OPTIONS")
    
    auxiliary_group.add_option('--fmt', type='choice', dest='fmt', 
        default='xml', choices=['xml', 'csv'], 
        help='specifies format of output collection description'),
    #@TODO: using incrementation
    auxiliary_group.add_option('--res', type='choice', dest='grouping', 
        default='album', choices=['album', ],
        help='specifies grouping of output collection description'),
    
    parser.add_option_group(auxiliary_group)
    
    return parser


def controller():
    
    if len(sys.argv) == 1:
        # graphical interface call
        app = App()
        gtk.main()
    else:
        # command line usage
        return _init_parser().parse_args()


if __name__ == "__main__":
    sys.exit(controller())
    