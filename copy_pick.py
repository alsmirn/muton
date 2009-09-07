'''
Created on 16 May 2009
'''
import os
import re
from distutils import file_util, dir_util

class FileCopierBySign():
    """Makes the extraction in the media collection and copies to the specified
    folder files with the specified genre or another parameter"""

    _TAGS_TO_CLEAN = ('artist', 'album')
    _OBLIGATORY_TAGS = _TAGS_TO_CLEAN + ('year', )
    
    _RESTR_SYMB = ('|', ':', r'\\', '/', '\?', '<', '>', '\*', '"')
    _DEPR_PUNCT = (' ', '..', '...')

    def __init__(self, collection):
        self.collection = collection

    def copy(self, output_path, info_type, search_item):
        """Copy files to the selected folder with specified parameters
        """
        #Trying iterate scanned tags in collection
        for curr_f_path, scanned_tags in self.collection.items():
            #Creates for each artist and album separate folder and copies
            #files to them
            try:
                self._TAGS_TO_CLEAN[0]
            except TypeError:
                print ("%r is not a valid audio file") % (curr_f_path, )

            if not scanned_tags[info_type].count(search_item):
                # not found
                continue
            else:
                #Stripping restricted symbols in artist and album name
                for tag in self._TAGS_TO_CLEAN:
                    for rs in self._RESTR_SYMB:
                        scanned_tags[tag] = re.sub(rs, '', scanned_tags[tag])
                    for wdp in self._DEPR_PUNCT:
                        scanned_tags[tag] = scanned_tags[tag].strip(wdp)

                # If all obligatory tags exist after cleaning
                if all([scanned_tags[o_tags] for o_tags in self._OBLIGATORY_TAGS]):
                    #Making path for the extraction
                    
                    #@TODO: automatic build fmt parameter from _OBLIGATORY_TAGS
                    #by now year would be a string instead of int
                    fmt = "%(artist)s %(year)s %(album)s" 
                    
                    out_file_path = os.path.join(output_path, 
                        fmt.decode('utf-8') % scanned_tags)
                    dir_util.mkpath(out_file_path)
                    #Copying files
                    file_util.copy_file(curr_f_path, out_file_path, 
                        'update = true')
