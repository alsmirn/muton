import os, codecs, re, sys

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
        new_name = os.path.join(os.path.split(path)[0], self.ren_sample + \
        os.path.splitext(path)[1])
        try:
            os.rename(path, new_name)
        except WindowsError:
            print 'The filename, directory name, or volume label syntax is incorrect', \
            path

    def make_sample(self, path, pattern):

        restr_symbols = '|', ':', '\\', '/', '?', '<', '>', '*', '"'
        win_depr_punct = ' ', '..', '...'

        key = self.collection[path]
        #Making safe print of track number
        if 'track' in key.keys() and re.search('\/', key['track']):
            m = re.search('\/', key['track'])
            track_n = key['track'][0:m.start()]
        elif 'track' in key.keys():
            track_n = key['track']
        else: track_n = ''

        #Adding 0 to track numbers without 0 - with 0 files are sorted better
        if track_n != '' and len(track_n) <= 1:
            track_n = '0' + track_n

        tag_items = {'artist': key['artist'],
            'album': key['album'],
            'year': key['year'],
            'genre': key['genre'],
            'title': key['title'],
            'track': track_n}

        s = pattern.split('%')
        #Replacing list's items by tag info
        for i in range(len(s)):
            try:
                s[i] = tag_items[s[i]]
            except KeyError:
                pass
        self.ren_sample = (''.join(symb for symb in s))

        #Stripping restricted symbols
        for rs in restr_symbols:
            if re.search(self.ren_sample, ' ' + rs):
                self.ren_sample = self.ren_sample.replace(rs, '')
            elif self.ren_sample.find(rs) != - 1:
                self.ren_sample = self.ren_sample.replace(rs, '')

        for wdp in win_depr_punct:
            self.ren_sample = self.ren_sample.lstrip(wdp).rstrip(wdp)
