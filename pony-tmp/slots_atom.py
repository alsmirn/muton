"""

Some experiments.

"""

class MediaFileInfo2(object):
    __slots__ = ('artist', 'title', 'album', 'year', 'genre', 'track', 
                 'comment', 'bitrate', 'format', 'copyright',
                 'date_of_rec', 'enc_time', 'orig_rel_time', 'audio_delay',
                 'rel_time', 'tag_time', 'encoder', 'lyricist', 'lyrics',
                 'rec_time', 'rec_year', 'cont_gr_desc', 'track_number',
                 'lang', 'length', 'tag_length', 'media_type', 'mood',
                 'orig_f_name', 'orig_lyricist', 'orig_artist', 'orig_album',
                 'orig_artist2', 'ensemble', 'coverartmime', 'total_tracks',
                 'orig_rel_year', 'owner', 'accomp', 'conductor', 'bpm',
                 'remixer', 'produced', 'publisher', 'album_artist',
                 'rec_dates', 'radiost_name', 'radiost_owner',
                 'url', 'buycd_url','author_url', 'audio_url',
                 'radiost_url', 'audiosource_url', 'audiof_url',
                 'composer', 'rating', 'f_type', 'encodedby',
                 'enc_by', 'alb_sort_ord_key', 'perf_sort_ord_key',
                 'title_sort_ord_key', 'isrc', 'enc_settings',
                 'start_key', 'iTunes_comp_flag', 'set_subtitle',
                 'disc_number', 'label', 'labelno', 'size', 'compilation',
                 'subt_desc', 'channels', 'sample_rate', 'bps', 
                 'total_samples', 'tag_error', 'rec_dates')
    
    #for s in __slots__: eval("%s = ''" % (s,))
    #eval("artist = ''")
    #artist = 'a'
    
    def __init__(self, *args, **kwargs):
        pass
        
instance = MediaFileInfo2()
#print dir(instance)
instance.artist = 'b'
print instance.artist

instance.z = 22434