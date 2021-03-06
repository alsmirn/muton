#!/usr/bin/env python
import os
import re
import sys

from collections import OrderedDict

try:
    import mutagen
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.apev2 import APEv2
    from mutagen.oggvorbis import OggVorbis
except ImportError, e:
    print e
    print "Use command `pip install mutagen`."
    sys.exit(1)


class MediaScanner():
    """
    @see: Scans input folder (dirpath) and returns a list of all
    audio files with their absolute paths.

    @author: Alexander Artemov
    """

    def __init__(self):
        self.tag_info = {}
        self.tag_error = ''
        self._paths = []  # list of file paths

    def scan(self, path):
        self.scan_fs(path)
        self.read_tags()
#        cProfile.runctx("self.read_tags()", globals(), locals(), 'log')
        return self.tag_info

    def scan_fs(self, path):
        """
        Make list of all files in dirpath

        @param dirpath: input dirpath
        """
        ext_list = ('.mp3', '.ape', '.ogg', '.flac')
        file_list = os.listdir(path)

        #Scanning the whole contents of the folder
        allpaths = [os.path.join(path, name) for name in file_list \
                    if ".%s" % name.lower().split(".")[-1] in ext_list]

        #Selecting only folders
        subdirs_paths = [os.path.join(path, name) for name in file_list \
                         if os.path.isdir(os.path.join(path, name))]

        #Adding to the list of the paths
        self._paths.extend(allpaths)

        #Applying the same scheme to the subfolders
        for subdir in subdirs_paths:
            self.scan_fs(subdir)

    def read_tags(self):
        #Creating a dictionary with path as key and tags as value
        for path in self._paths:
            lower_path = path.lower()

            if os.path.isdir(path):
                continue

            if lower_path.endswith(".mp3"):
                self.tag_info[path] = self.read_mp3_tag(path)
            elif lower_path.endswith(".flac"):
                self.tag_info[path] = self.read_flac_tag(path)
            elif lower_path.endswith(".ape"):
                self.tag_info[path] = self.read_ape_tag(path)
            elif lower_path.endswith(".ogg"):
                self.tag_info[path] = self.read_ogg_tag(path)

    def read_mp3_tag(self, path):
        """
        Returns mp3 tag info.
        """

        media_info = MediaFileInfo()

        try:
            mp3_audio = MP3(path)  # Reading tags
        except mutagen.mp3.HeaderNotFoundError:
            error_message = 'No MP3 tag found or %r is not a valid MP3 file.'
            try:
                media_info.tag_error = error_message % \
                                 path.encode(sys.stdout.encoding or "utf-8")
            except UnicodeDecodeError:
                media_info.tag_error = error_message % path
                print path

            return media_info

        #Initializing only those tags that are used in outputter
        media_info.artist = media_info.title = media_info.album = \
            media_info.year = media_info.genre = media_info.track = \
            media_info.comment = ''

        if 'TPE1' in mp3_audio: media_info.artist = str(mp3_audio['TPE1'])
        if 'TIT2' in mp3_audio: media_info.title = str(mp3_audio['TIT2'])
        if 'TALB' in mp3_audio: media_info.album = str(mp3_audio['TALB'])
        if 'TDRC' in mp3_audio: media_info.year = str(mp3_audio['TDRC'])
        if 'TCON' in mp3_audio: media_info.genre = str(mp3_audio['TCON'])
        if 'TRCK' in mp3_audio: media_info.track = str(mp3_audio['TRCK'])
        if 'TPOS' in mp3_audio: media_info.disc_number = str(mp3_audio['TPOS'])
        if 'TPUB' in mp3_audio: media_info.publisher = str(mp3_audio['TPUB'])
        if 'USLT' in mp3_audio: media_info.lyrics = str(mp3_audio['USLT'])

        #There can be infinite numbers of comment tags, so we can read any

        #First we escaping non printable tags
        bad_comms = "COMM:ID3v1:'eng'", "COMM:\x01:'\\x00\\x00Z'"

        for key in mp3_audio.keys():
            """There can be special "comment" tags, created by Itunes Player.
            For example COMM:iTunPGAP:'eng'. It's value can be "1NUL"
            (NUL - is the special symbol) or another symbols.
            These tags are not useful for export and not safe for reading
            (escape symbols could not be applied). So we are excluding them
            from export.
            """

            if not re.search('iTun', key) and key not in bad_comms \
            and re.match('COMM:', key):
                media_info.comment = str(mp3_audio[key])

        #There can be infinite numbers of url tags, so we can read any
        for key in mp3_audio.keys():
            if 'WXXX:' in key:
                media_info.url = str(mp3_audio[key])

        media_info.format = 'mp3'
        media_info.bitrate = mp3_audio.info.bitrate / 1000

        return media_info

    def read_flac_tag(self, path):
        """Returns flac file info."""

        media_info = MediaFileInfo()

        try:
            flac_audio = FLAC(path)  # Reading tags
        except mutagen.flac.FLACNoHeaderError:
            media_info.tag_error = "%r is not a valid FLAC file" % \
                (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            return media_info

        flac_tags = [
            'artist', 'title', 'album', 'date', 'genre', 'tracknumber',
            'comment', 'rating', 'composer', 'publisher', 'track', 'encoder',
            'originallyricist', 'origartist', 'copyright', 'album artist',
            'lyrics', 'lyricist', 'labelno', 'encodedby', 'mood', 'copyright',
            'label', 'radiostationname', 'bpm', 'ensemble', 'conductor',
            'compilation', 'isrc', 'discnumber', 'originalartist', 'url',
            'authorurl', 'radiostationurl', 'audiosourceurl', 'buycdurl',
            'audiofileurl']
        flac_tags = dict().fromkeys(flac_tags, '')

        #Creating a dictionary with tag id as key and tags as value
        for ft in flac_tags.keys():
            if ft in flac_audio:
                flac_tags[ft] = flac_audio[ft][0].encode('utf-8')
            else:
                flac_tags[ft] = ''

        media_info.artist = flac_tags['artist']
        media_info.title = flac_tags['title']
        media_info.album = flac_tags['album']
        media_info.year = flac_tags['date']
        media_info.genre = flac_tags['genre']
        media_info.track_number = flac_tags['tracknumber']
        media_info.comment = flac_tags['comment']
        media_info.copyright = flac_tags['copyright']
        media_info.lyrics = flac_tags['lyrics']
        media_info.disc_number = flac_tags['discnumber']
        media_info.labelno = flac_tags['labelno']
        media_info.label = flac_tags['label']
        media_info.encodedby = flac_tags['encodedby']
        media_info.encoder = flac_tags['encoder']
        media_info.lyricist = flac_tags['lyricist']
        media_info.ensemble = flac_tags['ensemble']
        media_info.compilation = flac_tags['compilation']
        media_info.orig_lyricist = flac_tags['originallyricist']
        media_info.orig_artist = flac_tags['originalartist']
        media_info.conductor = flac_tags['conductor']
        media_info.rating = flac_tags['rating']
        media_info.bpm = flac_tags['bpm']
        media_info.isrc = flac_tags['isrc']
        media_info.radiost_name = flac_tags['radiostationname']
        media_info.url = flac_tags['url']
        media_info.author_url = flac_tags['authorurl']
        media_info.buycd_url = flac_tags['buycdurl']
        media_info.audiosource_url = flac_tags['audiosourceurl']
        media_info.radiost_url = flac_tags['radiostationurl']
        media_info.audiof_url = flac_tags['audiofileurl']
        media_info.format = 'flac'
        media_info.sample_rate = flac_audio.info.sample_rate
        media_info.channels = flac_audio.info.channels
        media_info.bps = flac_audio.info.bits_per_sample
        media_info.total_samples = flac_audio.info.total_samples
        media_info.length = flac_audio.info.length
        media_info.bitrate = ''  # real bitrate is different

        return media_info

    def read_ape_tag(self, path):
        """Returns ape file info."""

        media_info = MediaFileInfo()
        try:
            ape_audio = APEv2(path)  # Reading tags
        except mutagen.apev2.APENoHeaderError:
            tag_error_msg = "No APE tag found or %r is not a valid APE file"

            try:
                media_info.tag_error = tag_error_msg % \
                    (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            except UnicodeDecodeError:
                # TODO! check this case
                pass

            return media_info

        ape_tags = [
            'artist', 'title', 'album', 'year', 'genre', 'track', 'comment',
            'rating', 'bpm', 'encoder', 'lyrics', 'lyricist',
            'originallyricist', 'labelno', 'encodedby', 'mood', 'copyright',
            'album artist', 'label', 'radiostationname', 'ensemble',
            'conductor', 'compilation', 'isrc', 'discnumber', 'originalartist',
            'url', 'authorurl', 'radiostationurl', 'audiosourceurl',
            'buycdurl', 'audiofileurl', 'composer']
        ape_tags = dict().fromkeys(ape_tags, '')

        #Creating a dictionary with tag id as key and tags as value
        for at in ape_tags.keys():
            if at in ape_audio:
                ape_tags[at] = ape_audio[at][0].encode('utf-8')
            else:
                ape_tags[at] = ''

        media_info.artist = ape_tags['artist']
        media_info.title = ape_tags['title']
        media_info.album = ape_tags['album']
        media_info.year = ape_tags['year']
        media_info.genre = ape_tags['genre']
        media_info.track = ape_tags['track']
        media_info.comment = ape_tags['comment']
        media_info.copyright = ape_tags['copyright']
        media_info.lyrics = ape_tags['lyrics']
        media_info.disc_number = ape_tags['discnumber']
        media_info.labelno = ape_tags['labelno']
        media_info.label = ape_tags['label']
        media_info.encodedby = ape_tags['encodedby']
        media_info.encoder = ape_tags['encoder']
        media_info.lyricist = ape_tags['lyricist']
        media_info.ensemble = ape_tags['ensemble']
        media_info.compilation = ape_tags['compilation']
        media_info.orig_lyricist = ape_tags['originallyricist']
        media_info.orig_artist = ape_tags['originalartist']
        media_info.conductor = ape_tags['conductor']
        media_info.rating = ape_tags['rating']
        media_info.bpm = ape_tags['bpm']
        media_info.isrc = ape_tags['isrc']
        media_info.radiost_name = ape_tags['radiostationname']
        media_info.url = ape_tags['url']
        media_info.author_url = ape_tags['authorurl']
        media_info.buycd_url = ape_tags['buycdurl']
        media_info.audiosource_url = ape_tags['audiosourceurl']
        media_info.radiost_url = ape_tags['radiostationurl']
        media_info.audiof_url = ape_tags['audiofileurl']
        media_info.format = 'ape'
        media_info.bitrate = ''

        return media_info


    def read_ogg_tag(self, path):
        """Returns ape file info."""

        media_info = MediaFileInfo()
        try:
            ogg_audio = OggVorbis(path) #Reading tags
        except:
            media_info.tag_error = \
                "No Ogg tag found or %r is not a valid OGG file" % \
                (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            return media_info
        
        ogg_tags = [
            'artist', 'title', 'album', 'year', 'genre', 'tracknumber', 
            'comment', 'composer', 'coverartmime', 'date', 'rating', 
            'publisher', 'totaltracks', 'lyrics', 'lyricist', 
            'originallyricist', 'labelno', 'encodedby', 'mood', 'copyright', 
            'label', 'radiostationname', 'bpm', 'ensemble', 'conductor', 
            'compilation', 'isrc', 'discnumber', 'originalartist', 
            'origartist', 'album_artist', 'compilation', 'url', 'authorurl', 
            'radiostationurl', 'audiosourceurl', 'buycdurl', 'audiofileurl', 
            'coverartmime', 'encoder']
        ogg_tags = dict().fromkeys(ogg_tags, '')

        #Creating a dictionary with tag id as key and tags as value
        for ot in ogg_tags.keys():
            if ot in ogg_audio:
                ogg_tags[ot] = ogg_audio[ot][0].encode('utf-8')
            else:
                ogg_tags[ot] = ''

        media_info.artist = ogg_tags['artist']
        media_info.title = ogg_tags['title']
        media_info.album = ogg_tags['album']
        media_info.year = ogg_tags['year']

        if media_info.year == '':
            media_info.year = ogg_tags['date']

        media_info.genre = ogg_tags['genre']
        media_info.track = ogg_tags['tracknumber']
        media_info.comment = ogg_tags['comment']
        media_info.album_artist = ogg_tags['album_artist']
        media_info.ensemble = ogg_tags['ensemble']
        media_info.copyright = ogg_tags['copyright']
        media_info.publisher = ogg_tags['publisher']
        media_info.lyrics = ogg_tags['lyrics']
        media_info.lyricist = ogg_tags['lyricist']
        media_info.composer = ogg_tags['composer']
        media_info.disc_number = ogg_tags['discnumber']
        media_info.label = ogg_tags['label']
        media_info.labelno = ogg_tags['labelno']
        media_info.total_tracks = ogg_tags['totaltracks']
        media_info.encoder = ogg_tags['encoder']
        media_info.encodedby = ogg_tags['encodedby']
        media_info.compilation = ogg_tags['compilation']
        media_info.orig_lyricist = ogg_tags['originallyricist']
        media_info.orig_artist = ogg_tags['originalartist']
        media_info.orig_artist2 = ogg_tags['origartist']
        media_info.conductor = ogg_tags['conductor']
        media_info.rating = ogg_tags['rating']
        media_info.mood = ogg_tags['mood']
        media_info.coverartmime = ogg_tags['coverartmime']
        media_info.bpm = ogg_tags['bpm']
        media_info.isrc = ogg_tags['isrc']
        media_info.url = ogg_tags['url']
        media_info.radiost_name = ogg_tags['radiostationname']
        media_info.url = ogg_tags['url']
        media_info.author_url = ogg_tags['authorurl']
        media_info.buycd_url = ogg_tags['buycdurl']
        media_info.audiosource_url = ogg_tags['audiosourceurl']
        media_info.radiost_url = ogg_tags['radiostationurl']
        media_info.audiof_url = ogg_tags['audiofileurl']
        media_info.format = 'ogg'
        media_info.bitrate = ogg_audio.info.bitrate / 1000
        media_info.length = ogg_audio.info.length

        return media_info


class MediaFileInfo2(object):
    __slots__ = (
            '_MediaFileInfo__initialised', 'tag_error', 'rec_dates', 'artist',
            'title', 'album', 'year', 'genre', 'track', 'comment', 'bitrate',
            'format', 'copyright', 'date_of_rec', 'enc_time', 'orig_rel_time',
            'audio_delay', 'rel_time', 'tag_time', 'encoder', 'lyricist',
            'lyrics', 'rec_time', 'rec_year', 'cont_gr_desc', 'track_number',
            'lang', 'length', 'tag_length', 'media_type', 'mood',
            'orig_f_name', 'orig_lyricist', 'orig_artist', 'orig_album',
            'orig_artist2', 'ensemble', 'coverartmime', 'total_tracks',
            'orig_rel_year', 'owner', 'accomp', 'conductor', 'bpm', 'remixer',
            'produced', 'publisher', 'album_artist', 'rec_dates',
            'radiost_name', 'radiost_owner', 'url', 'buycd_url', 'author_url',
            'audio_url', 'radiost_url', 'audiosource_url', 'audiof_url',
            'composer', 'rating', 'f_type', 'encodedby', 'enc_by',
            'alb_sort_ord_key', 'perf_sort_ord_key', 'title_sort_ord_key',
            'isrc', 'enc_settings', 'start_key', 'iTunes_comp_flag',
            'set_subtitle', 'disc_number', 'label', 'labelno', 'size',
            'compilation', 'subt_desc', 'channels', 'sample_rate', 'bps',
            'total_samples')

    def __init__(self, *args, **kwargs):
        pass

    def get_tag(self, tag_name):
        """simple getter by tag_name"""
        if tag_name in self.__slots__:
            try:
                return self.__getattribute__(tag_name)
            except AttributeError:
                return None
        else:
            raise Exception("Tag with name '%s' does not exist." % tag_name)

    def get_tags(self):
        """return list of all possible tags"""
        return self.__slots__

    def get_active_tags(self):
        """return list of all initialized tags"""
        actual_tags = {}
        for tag in self.__slots__:
            try:
                actual_tags[tag] = self.__getattribute__(tag)
            except AttributeError:
                pass
        return actual_tags


class MediaFileInfo(dict):
    """
    @see: Realization of object "MediaFileInfo" with multiple properties.
    (Using overloading __getattr__ and __setattr__.)

    @note: We can set only concrete tags from "tag_names" tuple.

    @TODO: refactoring. Make common multiple-attributes fabric and extend them.

    @author: Alexey Smirnov
    """
    def __init__(self, indict=None):
        if indict is None:
            indict = {}

        # set any attributes here - before initialization
        # these remain as normal attributes
        dict.__init__(self, indict)
        self.__initialised = True
        # after initialization, setting attributes is the same as setting an item

    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Maps attributes to values. Only if we are initialized."""

        tag_names = (
            '_MediaFileInfo__initialised', 'tag_error', 'format', 'artist',
            'title', 'album', 'year', 'genre', 'track', 'comment',
            'disc_number', 'publisher', 'bitrate', 'url')

        if item not in tag_names:
            #raise AttributeError(item)
            #TODO: pass is temporary solution
            pass

        if not self.__dict__.has_key('_MediaFileInfo__initialised'):
            # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):
            # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)


if __name__ == '__main__':

    try:
        path = sys.argv[1]
    except IndexError:
        msg = """
            Collection path doesn't specified.
            Usage: python collection.py path > outfile"""
        print(msg)
        sys.exit(1)

    tag_info = MediaScanner().scan(path)

    # order by path
    tag_info = OrderedDict(sorted(tag_info.items(), key=lambda t: t[0]))

    for vals in tag_info.values():
        try:
            print "%(artist)s|%(title)s" % vals
        except KeyError, e:
            print "|"
