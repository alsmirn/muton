import os
import csv
import codecs
from xml.sax.saxutils import escape

class ScannedInfoWriter():
    """Returns CSV and XML with all albums info."""

    def __init__(self, collection):
        self.collection = collection
        self._alb_size_dict = {}
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
                    alb_size += float(os.path.getsize(path)) / 1048576
                self._alb_size_dict[alb] = ['%4.2f' % alb_size]

    def write(self, out_path, output_mode, extension):
        fmt = "%s.%s"
        output_name = 'output'
        
        out_filepath = os.path.join(out_path, fmt % (output_name, extension))
        
        if extension == 'csv':
            self.make_CSV(output_mode, out_filepath)
            #self.make_excel_CSV(output_mode, out_filepath)
        elif extension == 'xml':
            self.make_XML(output_mode, out_filepath)
    
    def make_CSV(self, output_mode, output_csv):
        self.scan_alb_size()
        mark = [] #List of albums for checking of uniqueness
    
        col_titles = (
            'artist', 'album', 'year', 'genre', 
            'bitrate', 'format', 'size', 'comment')
    
        output_descriptor = open(output_csv, 'w')
        collection_description = csv.writer(output_descriptor, 
                                            delimiter=';', 
                                            quoting=csv.QUOTE_MINIMAL)
        collection_description.writerow([ct.capitalize() for ct in col_titles])
    
        for path, v in self.collection.items():
            try:
                if str(v['bitrate']) not in self._bitr_samples:
                    v['bitrate'] = 'VBR %s' % str(v['bitrate'])
                if output_mode == 'album':
                    if v['album'] in mark:
                        continue
                    else:
                        row = [
                            v['artist'], v['album'], v['year'][0:4], 
                            v['genre'], v['bitrate'], v['format'], 
                            self._alb_size_dict[v['album']][0], v['comment']]
                        collection_description.writerow(row)
                        mark.append(v['album'])
                else:
                    row = [
                        v['artist'], v['album'], v['year'][0:4],
                        v['genre'], v['bitrate'], v['format'],
                        float(os.path.getsize(path))/1048576, v['comment']]
                    collection_description.writerow(row)
            except TypeError:
                print "%r is not a valid audio file" % (path, )
                return

        output_descriptor.close()
    
    #@TODO: rewrite function using dom.minidom
    #@TODO: make output sorted by artist
    def make_XML(self, output_mode, output_xml):
        """Returns XML with all pattern info (for example - album info)."""

        self._fx = open(output_xml, "w")
        self._fx.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self._fx.write("<MediaInfo>\n")

        if output_mode == 'single':
            self.write_single_XML()
        else:
            self.write_group_XML(output_mode)

        self._fx.write("\n</MediaInfo>")
        self._fx.close()

    def write_single_XML(self):
        for path, tags in self.collection.items():
            if 'bitrate' in tags and str(tags['bitrate']) not in self._bitr_samples:
                tags['bitrate'] = 'VBR ' + str(tags['bitrate'])
            self._fx.write("<FileInfo>\n")
            
            if 'artist' in tags:
                self._fx.write("<Artist> %s </Artist>\n" % escape(tags['artist']))
            else:
                self._fx.write("<Artist> %s </Artist>\n" % escape(path))

            self._fx.write("<Title> %s </Title>\n" % escape(tags['title']) \
                           if 'title' in tags else str(),)
            self._fx.write("<Album> %s </Album>\n" % escape(tags['album']) \
                           if 'album' in tags else str(),)
            self._fx.write("<Year> %s </Year>\n" % (tags['year'][0:4],) \
                           if 'year' in tags else str(),)
            self._fx.write("<Genre> %s </Genre>\n" % escape(tags['genre']) \
                           if 'genre' in tags else str(),)
            self._fx.write("<Bitrate> %s </Bitrate>\n" % tags['bitrate'] \
                           if 'bitrate' in tags else str(),)
            self._fx.write("<Format> %s </Format>\n\t" % tags['format'] \
                           if 'format' in tags else str(),)
            self._fx.write("<Size> %4.2f </Size>\n\t" % \
                           (float(os.path.getsize(path))/1048576))
            self._fx.write("<Comment> %s </Comment>\n" % escape(str(tags['comment'])) \
                           if 'comment' in tags else str(),)
            self._fx.write("</FileInfo>")
            
    def write_group_XML(self, output_mode):
        self.scan_alb_size()
        mark = [] #List of tags for checking the uniqueness
        #output_mode for this method can be any tag ('album', 'year' etc.)
        for path, v in self.collection.items():
            if output_mode in v and v[output_mode] not in mark:

                # notation that bitrate is VBR
                if str(v['bitrate']) not in self._bitr_samples:
                    v['bitrate'] = 'VBR %s' % str(v['bitrate'])
                
                # tags to write
                xml_tags_list = ('artist', 'album', 'year', 'genre', 
                    'bitrate', 'format', 'size', 'comment')
                
                final_string = []
                for tag in xml_tags_list:
                   
                    if tag == 'size':
                        checked = self._alb_size_dict[v['album']][0]
                    elif tag == 'year':
                        checked = v['year'][0:4]
                    else:
                        checked = v[tag]
                        if isinstance(checked, str):
                            checked = escape(v[tag])                            
                        else:
                            checked = str(checked)

                    capitalized = tag.capitalize()
                    
                    piece = "\t<%s>%s</%s>\n" % (capitalized, checked, capitalized)
                    final_string.append(piece)
                
                self._fx.write("<AlbumInfo>\n%s</AlbumInfo>\n" % \
                                str().join(final_string))
                
                mark.append(v[output_mode])
