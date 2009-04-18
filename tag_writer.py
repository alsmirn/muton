import os, re, sys
import mutagen
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TPE1, TDRC, TALB, TCON, COM, TRK, TCOP, \
                        TPOS, TEXT, TENC, TSRC, TBPM, TPE3, TPUB, TMOO, TOPE, \
                        TOLY, TOAL, TOFN, TORY, TOWN, TPE2, TPE4, TPRO, TRSN, \
                        TRSO, TSIZ, TSOA, TSOP, TSOT, TSSE, TSST, TRDA, TFLT, \
                        TIME, TIT1, TIT3, TKEY, TLAN, TLEN, TMED, TCMP, TDAT, \
                        TDEN, TDOR, TDLY, TDRL, TDTG, TYER

class TagWriteManager():
    
    def __init__(self, collection):
        self.collection = collection
        self._paths = [] # list of file paths
          
    def tag_write_man(self, path, write_mode, tag_type, input_string):
        if write_mode == 'single':
            self.write(path, tag_type, input_string)
        else: 
            self.deepwrite(tag_type, input_string)

    def deepwrite(self, tag_type, input_string):
        for path in self.collection.keys():
            self.write(path, tag_type, input_string)

    def write(self, path, tag_type, input_string):
        lower_path = path.lower()
        if re.search('\.mp3' + '$', lower_path):
            """Executing methods for each type of mp3 tag"""    
            mp3_tagWriter = MP3TagWriter(path)       
            if tag_type == 'title':                   
                mp3_tagWriter.mp3_write_title(path, input_string)
            elif tag_type == 'artist':
                mp3_tagWriter.mp3_write_artist(path, input_string)
            elif tag_type == 'album':
                mp3_tagWriter.mp3_write_album(path, input_string)
            elif tag_type == 'year':
                mp3_tagWriter.mp3_write_year(path, input_string)
            elif tag_type == 'genre':
                mp3_tagWriter.mp3_write_genre(path, input_string)
            elif tag_type == 'comment':
                mp3_tagWriter.mp3_write_comment(path, input_string)
            elif tag_type == 'trk':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'copyright':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'disc_number':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'encoder':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'lyricist':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'isrc':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'bpm':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'conductor':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'publisher':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'mood':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'orig_artist':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'orig_lyricist':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'orig_album':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'orig_file_name':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'orig_rel_year':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'owner':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'accomp':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'remixer':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'produced':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'radiostation_name':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'radiostation_owner':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'alb_sort_order_key':
                mp3_tagWriter.mp3_write_trk(path, input_string)    
            elif tag_type == 'perf_sort_order_key':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'title_sort_order_key':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'enc_settings':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'set_subtitle':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'rec_year':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'rec_dates':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'file_type':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'rec_time':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'cont_gr_desc':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'subt_desc':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'start_key':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'lang':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'media_type':
                mp3_tagWriter.mp3_write_trk(path, input_string)                    
            elif tag_type == 'date_of_rec':
                mp3_tagWriter.mp3_write_trk(path, input_string)
            elif tag_type == 'enc_time':
                mp3_tagWriter.mp3_write_trk(path, input_string)                    
            elif tag_type == 'orig_rel_time':
                mp3_tagWriter.mp3_write_trk(path, input_string)                    
            elif tag_type == 'audio_delay':
                mp3_tagWriter.mp3_write_trk(path, input_string)                    
            elif tag_type == 'rel_time':
                mp3_tagWriter.mp3_write_trk(path, input_string)                    
            elif tag_type == 'tag_time':
                mp3_tagWriter.mp3_write_trk(path, input_string)                    
        """Executing method for writing flac tags"""             
        if re.search('\.flac' + '$', lower_path):
            flac_tagWriter = FLACTagWriter()
            flac_tagWriter.flac_write_tags(path, tag_type, input_string)
        """Executing method for writing ape tags"""
        if re.search('\.ape' + '$', lower_path):
            ape_tagWriter = APETagWriter()
            ape_tagWriter.ape_write_tags(path, tag_type, input_string)
        """Executing method for writing ogg tags"""
        if re.search('\.ogg' + '$', lower_path):
            ogg_tagWriter = OGGTagWriter()
            ogg_tagWriter.ogg_write_tags(path, tag_type, input_string)
                    
                        
class MP3TagWriter():
    """Writes tags to mp3 files"""
    
    #@warning: can't write tags if tag is absent completely. Need to solve it.
    
    def __init__(self, path):
        self.path = path
        
        try:
            self.mp3_audio = ID3(self.path) #Reading tags
        except (mutagen.id3.ID3NoHeaderError, mutagen.mp3.HeaderNotFoundError):
            print "No MP3 tag found or %r is not a valid MP3 file" % (self.path, )
            return           

    def mp3_write_title(self, path, input_string):
        self.mp3_audio.add(TIT2(encoding=3, text=input_string))
        self.mp3_audio.save()
        
    def mp3_write_artist(self, path, input_string):
        self.mp3_audio.add(TPE1(encoding=3, text=input_string))
        self.mp3_audio.save()       
                    
    def mp3_write_album(self, path, input_string):
        self.mp3_audio.add(TALB(encoding=3, text=input_string))
        self.mp3_audio.save()
                
    def mp3_write_year(self, path, input_string):
        self.mp3_audio.add(TDRC(encoding=3, text=input_string))
        self.mp3_audio.save()   
                
    def mp3_write_genre(self, path, input_string):
        self.mp3_audio.add(TCON(encoding=3, text=input_string))
        self.mp3_audio.save()          
        
    def mp3_write_comment(self, path, input_string):
        self.mp3_audio.add(COM(encoding=3, text=input_string))
        self.mp3_audio.save() 
        
    def mp3_write_trk(self, path, input_string):
        self.mp3_audio.add(TRK(encoding=3, text=input_string))
        self.mp3_audio.save()                                                                         

    def mp3_write_copyright(self, path, input_string):
        self.mp3_audio.add(TCOP(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_disc_number(self, path, input_string):
        self.mp3_audio.add(TPOS(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_encoder(self, path, input_string):
        self.mp3_audio.add(TENC(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_lyricist(self, path, input_string):
        self.mp3_audio.add(TEXT(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_isrc(self, path, input_string):
        self.mp3_audio.add(TSRC(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_bpm(self, path, input_string):
        self.mp3_audio.add(TBPM(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_conductor(self, path, input_string):
        self.mp3_audio.add(TPE3(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_publisher(self, path, input_string):
        self.mp3_audio.add(TPUB(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_mood(self, path, input_string):
        self.mp3_audio.add(TMOO(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_orig_artist(self, path, input_string):
        self.mp3_audio.add(TOPE(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_orig_lyricist(self, path, input_string):
        self.mp3_audio.add(TOLY(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_orig_album(self, path, input_string):
        self.mp3_audio.add(TOAL(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_orig_file_name(self, path, input_string):
        self.mp3_audio.add(TOFN(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_orig_rel_year(self, path, input_string):
        self.mp3_audio.add(TORY(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_owner(self, path, input_string):
        self.mp3_audio.add(TOWN(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_accomp(self, path, input_string):
        self.mp3_audio.add(TPE2(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_remixer(self, path, input_string):
        self.mp3_audio.add(TPE4(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_produced(self, path, input_string):
        self.mp3_audio.add(TPRO(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_radiostation_name(self, path, input_string):
        self.mp3_audio.add(TRSN(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_radiostation_owner(self, path, input_string):
        self.mp3_audio.add(TRSO(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_size(self, path, input_string):
        self.mp3_audio.add(TSIZ(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_alb_sort_order_key(self, path, input_string):
        self.mp3_audio.add(TSOA(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_perf_sort_order_key(self, path, input_string):
        self.mp3_audio.add(TSOP(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_title_sort_order_key(self, path, input_string):
        self.mp3_audio.add(TSOT(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_enc_settings(self, path, input_string):
        self.mp3_audio.add(TSSE(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_set_subtitle(self, path, input_string):
        self.mp3_audio.add(TSST(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_rec_year(self, path, input_string):
        self.mp3_audio.add(TYER(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_rec_dates(self, path, input_string):
        self.mp3_audio.add(TRDA(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_file_type(self, path, input_string):
        self.mp3_audio.add(TFLT(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_rec_time(self, path, input_string):
        self.mp3_audio.add(TIME(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_cont_gr_desc(self, path, input_string):
        self.mp3_audio.add(TIT1(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_subt_desc(self, path, input_string):
        self.mp3_audio.add(TIT3(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_start_key(self, path, input_string):
        self.mp3_audio.add(TKEY(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_lang(self, path, input_string):
        self.mp3_audio.add(TLAN(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_length(self, path, input_string):
        self.mp3_audio.add(TLEN(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_media_type(self, path, input_string):
        self.mp3_audio.add(TMED(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_iTunes_comp_flag(self, path, input_string):
        self.mp3_audio.add(TCMP(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_date_of_rec(self, path, input_string):
        self.mp3_audio.add(TDAT(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_enc_time(self, path, input_string):
        self.mp3_audio.add(TDEN(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_orig_rel_time(self, path, input_string):
        self.mp3_audio.add(TDOR(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_audio_delay(self, path, input_string):
        self.mp3_audio.add(TDLY(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_rel_time(self, path, input_string):
        self.mp3_audio.add(TDRL(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_tag_time(self, path, input_string):
        self.mp3_audio.add(TDTG(encoding=3, text=input_string))
        self.mp3_audio.save()
        

class FLACTagWriter():
    """Writes tags to FLAC file"""

    def flac_write_tags(self, path, tag_type, input_string):
        try:
            flac_audio = FLAC(path) #Reading tags
        except mutagen.flac.FLACNoHeaderError:
            print ("%r is not a valid FLAC file") \
             % (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            return
        flac_audio[tag_type] = input_string
        flac_audio.save()

class APETagWriter():
    """Writes tags to APEv2 file"""

    def ape_write_tags(self, path, tag_type, input_string):
        try:
            ape_audio = APEv2(path) #Reading tags
        except mutagen.apev2.APENoHeaderError:
            print ("No APE tag found or %r is not a valid APE file") % \
            (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            return
        ape_audio[tag_type] = input_string
        ape_audio.save()

class OGGTagWriter():
    """Writes tags to OGG file"""
    
    def ogg_write_tags(self, path, tag_type, input_string):
        try:
            ogg_audio = OggVorbis(path) #Reading tags
        except:
            print ("No Ogg tag found or %r is not a valid OGG file") \
            % (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            return
        ogg_audio[tag_type] = input_string
        ogg_audio.save()
        
