import os
import csv
from xml.sax.saxutils import escape
import xml.dom.minidom

class ScannedInfoWriter():
    """Returns CSV and XML with all albums info."""

    def __init__(self, collection):
        self.collection = collection
        self._alb_size_dict = {}
        self._col_titles = ('artist', 'album', 'year', 'genre', 
                      'bitrate', 'format', 'size', 'comment')
        
        #Format of variable bitrate output
        self._bitr_samples = ('', '128', '160', '192', '256', '320')

    def scan_alb_size(self):
        """"Counts size of each album - for each tag type 'album' """

        alb_list = [] #List of albums
        for path, v in self.collection.items():
            if 'album' in v and v['album'] not in alb_list:
                alb_list.append(v['album'])

        for alb in alb_list:
            alb_size = 0
            for path, v in self.collection.items():
                if 'album' in v and v['album'] == alb:
                    alb_size += float(os.path.getsize(path)) / (1<<20)
                self._alb_size_dict[alb] = ['%4.2f' % alb_size]

    def write(self, out_path, grouping, extension):
        """
        @param output_mode: type of grouping, i.e. by album, by artist or no
        @param extension: format of export file, i.e. CSV or XML by now
        """
        
        fmt = "%s.%s"
        output_name = 'output'
        out_filepath = os.path.join(out_path, fmt % (output_name, extension))
        
        if extension == 'csv':
            self.make_CSV(grouping, out_filepath)
        elif extension == 'xml':
            self.make_XML(grouping, out_filepath)
    
    def make_CSV(self, grouping, out_filepath):
        """
        @param grouping: like SQL group_by, may be ('album', 'song')
        @param out_filepath: path to .csv file with collection description 
        """
        
        if grouping == 'album':
            grouping_cache = [] #List of albums for checking of uniqueness
            self.scan_alb_size()
    
        output_descriptor = open(out_filepath, 'w')
        collection_description = csv.writer(output_descriptor, 
                                            delimiter=';', 
                                            quoting=csv.QUOTE_MINIMAL)
        collection_description.writerow([ct.capitalize() \
                                         for ct in self._col_titles])
    
        for path, tags in self.collection.items():
            
            if 'tag_error' in tags:
                continue
            
            field_to_append = None
            album_name = tags['album']

            if str(tags['bitrate']) not in self._bitr_samples:
                tags['bitrate'] = 'VBR %s' % str(tags['bitrate'])
            
            if grouping == 'album':
                if album_name not in grouping_cache:
                    grouping_cache.append(album_name)
                    field_to_append = self._alb_size_dict[album_name][0]
                else: 
                    continue
            elif grouping == 'song':
                field_to_append = float(os.path.getsize(path))/(1<<20)
                    
            row = [tags['artist'], tags['album'], tags['year'], 
                   tags['genre'], tags['bitrate'], tags['format'],
                   field_to_append, tags['comment']]
            collection_description.writerow(row)

        output_descriptor.close()
    
    def make_XML(self, grouping, output_xml):
        """Returns XML with all pattern info (for example - album info)."""
        
        self._fx = open(output_xml, "w")
        if grouping == 'album':
            self.scan_alb_size()
       
        doc = xml.dom.minidom.Document()
        
        media_info_elem = doc.createElement("MediaInfo")
        doc.appendChild(media_info_elem) 

        mark = [] # List of tags for checking the uniqueness    
        # output_mode for this method can be any tag ('album', 'year' etc.)
        
        for (_, tags) in self.collection.items():        
            album_info_elem = doc.createElement("AlbumInfo")

            if grouping in tags and tags[grouping] not in mark:

                # notation that bitrate is VBR
                if str(tags['bitrate']) not in self._bitr_samples:
                    tags['bitrate'] = 'VBR %s' % str(tags['bitrate']) 

                for tag in self._col_titles:                  
                    media_info_elem.appendChild(album_info_elem)

                    if tag == 'size':
                        checked = self._alb_size_dict[tags['album']][0]
                    elif tag == 'year':
                        checked = tags['year'][0:4]
                    else:
                        checked = tags[tag]
                        if isinstance(checked, str):
                            checked = escape(tags[tag])                            
                        else:
                            checked = str(checked)
        
                    elem_name = doc.createElement(tag.capitalize())
                    album_info_elem.appendChild(elem_name)
                    
                    txt_elem = doc.createTextNode(checked)
                    elem_name.appendChild(txt_elem)
                
                mark.append(tags[grouping])
                
        doc.writexml(self._fx, newl="\n", addindent="    ", encoding="UTF-8")
        self._fx.close()        
        