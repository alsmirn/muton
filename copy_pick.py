'''
Created on 16 May 2009
'''

import os
from distutils import file_util, dir_util

class FileCopierBySign():
    """Makes the extraction in the media collection and copies to the specified
    folder files with the specified genre or another parameter"""
    
    def __init__(self, collection):
        self.collection = collection
                       
    def copy(self, output_path, info_type, search_item):
        restr_symbols = ('|', ':', '\\', '/', '?', '<', '>', '*', '"')
        win_depr_punct = (' ', '..', '...')
        
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

