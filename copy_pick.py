'''
Created on 16 May 2009
'''

import os
import re
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
                
                # @note: THIS OPERATION YOU CAN DO IN ONE REGULAR EXPR, THINCK!
                strip_tags = ('artist', 'album')
                
                for tag in strip_tags:
                    for rs in restr_symbols:
                        v[tag] = re.sub(r'[ ]?%s' % rs, '', v[tag])

                    for wdp in win_depr_punct:
                        v[tag] = v[tag].strip(wdp)

                #Making path for the extraction
                file_path = os.path.join(output_path, v['artist'].decode('utf-8'),
                            v['year'] + ' ' + v['album'].decode('utf-8'))
                dir_util.mkpath(file_path)
                #Copying files
                if v['artist'] != '' and v['album'] != '' and v['year'] != '':
                    file_util.copy_file(k, file_path, 'update = true')

