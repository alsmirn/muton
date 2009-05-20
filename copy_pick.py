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
    
    _RESTR_SYMB = ('|', ':', '\\', '/', '?', '<', '>', '*', '"')
    _DEPR_PUNCT = (' ', '..', '...')

    def __init__(self, collection):
        self.collection = collection

    def copy(self, output_path, info_type, search_item):
        """Trying iterate scanned tags in collection"""
        for current_file_path, scanned_tags in self.collection.items():
            #Creates for each artist and album separate folder and copies
            #files to them
            try:
                tmp_var = self._TAGS_TO_CLEAN[0]
            except TypeError:
                print ("%r is not a valid audio file") % (current_file_path, )

            if scanned_tags[info_type].find(search_item) == - 1:
                # not found
                continue
            else:
                #Stripping restricted symbols in artist and album name
                # @note: THIS OPERATION YOU CAN DO IN ONE REGULAR EXPR, THINCK!
                for tag in self._TAGS_TO_CLEAN:
                    for rs in self._RESTR_SYMB:
                        scanned_tags[tag] = re.sub(r'[ ]?%s' % rs, '', scanned_tags[tag])

                    for wdp in self._DEPR_PUNCT:
                        scanned_tags[tag] = scanned_tags[tag].strip(wdp)

                # If all obligatory tags exist after cleaning
                if all([scanned_tags[o_tags] for o_tags in self._OBLIGATORY_TAGS]):
                    #Making path for the extraction
                    
                    #@TODO: automatic build fmt parameter from _OBLIGATORY_TAGS
                    fmt = "%(artist)s %(year)d %(album)s"
                    
                    out_file_path = os.path.join(output_path, fmt.decode('utf-8') % scanned_tags)
                    dir_util.mkpath(out_file_path)
                    #Copying files
                    file_util.copy_file(current_file_path, out_file_path, 'update = true')
