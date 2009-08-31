import re
import os
import sys
import codecs

class Renamer():
    def __init__(self, collection):
        self.collection = collection
        self.ren_sample = ''

    def manager(self, ren_mode, path, pattern):
        if ren_mode == 'single':
            self.single_rename(path, pattern)
        else:
            self.recursive_rename(pattern)

    def recursive_rename(self, pattern):
        for path in self.collection.keys():
            self.single_rename(path, pattern)

    def single_rename(self, path, pattern):
        self.make_sample(path, pattern)

        #Renaming file
        new_name = os.path.join(os.path.split(path)[0], 
            self.ren_sample + os.path.splitext(path)[1])
        try:
            os.rename(path, new_name)
        except WindowsError:
            print 'The filename, directory name, or volume label syntax is incorrect', \
                path

    def make_sample(self, path, pattern):

        key = self.collection[path]
        
        restr_symbols = ('|', ':', '\\', '/', '?', '<', '>', '*', '"')
        win_depr_punct = (' ', '..', '...')

        tag_items = {}
        tag_items_names = ('artist', 'album', 'album', 'year', 'genre', 'title')
        
        #Making safe print of track number
        track_number = str()
        track_tag_name = 'track'
        
        if track_tag_name in key.keys():
            track_number = "%02d" % key[track_tag_name].split('/')[0]
        
        tag_items[track_tag_name] = track_number
        
        #Filling tag_items from file
        for item in tag_items_tuple:
            tag_items[item] = key[item]
        
        #Replacing list's items by tag info
        s = pattern.split('%')
        for i in range(len(s)):
            try:
                s[i] = tag_items[s[i]]
            except KeyError:
                pass
        self.ren_sample = (''.join(symb for symb in s))

        #Stripping restricted symbols
        for rs in restr_symbols:
            if rs in self.ren_sample:
                self.ren_sample = self.ren_sample.replace(rs, '')

        for wdp in win_depr_punct:
            self.ren_sample = self.ren_sample.strip(wdp)
