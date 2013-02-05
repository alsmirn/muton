import sys
import re

import mutagen
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import (ID3, TIT2, TPE1, TDRC, TALB, TCON, COM, TRK, TPOS,
                         TPUB,  USLT, WXXX, APIC)


class TagWriteManager():

    def __init__(self, collection):
        self.collection = collection
        self._paths = []  # list of file paths

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
            elif tag_type == 'disc_number':
                mp3_tagWriter.mp3_write_disc_number(path, input_string)
            elif tag_type == 'publisher':
                mp3_tagWriter.mp3_write_publisher(path, input_string)
            elif tag_type == 'url':
                mp3_tagWriter.mp3_write_url(path, input_string)
            elif tag_type == 'lyrics':
                mp3_tagWriter.mp3_write_lyrics(path, input_string)
            elif tag_type == 'picture':
                mp3_tagWriter.mp3_write_picture(path, input_string)

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
            self.mp3_audio = ID3(self.path)  # Reading tags
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

    def mp3_write_disc_number(self, path, input_string):
        self.mp3_audio.add(TPOS(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_publisher(self, path, input_string):
        self.mp3_audio.add(TPUB(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_url(self, path, input_string):
        self.mp3_audio.add(WXXX(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_lyrics(self, path, input_string):
        self.mp3_audio.add(USLT(encoding=3, text=input_string))
        self.mp3_audio.save()

    def mp3_write_picture(self, path, input_string):
        self.mp3_audio.add(APIC(encoding=3, mime='-->', type=3, data=input_string))
        self.mp3_audio.save()


class FLACTagWriter():
    """Writes tags to FLAC file"""

    def flac_write_tags(self, path, tag_type, input_string):
        try:
            flac_audio = FLAC(path)  # Reading tags
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
            ape_audio = APEv2(path)  # Reading tags
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
            ogg_audio = OggVorbis(path)  # Reading tags
        except:
            print ("No Ogg tag found or %r is not a valid OGG file") \
            % (path.encode(sys.stdout.encoding or "utf-8", "replace"), )
            return
        ogg_audio[tag_type] = input_string
        ogg_audio.save()
     def play_file(self, song):
         sd = open(self.f, "rb")
         pygame.mixer.music.load(sd)
         pygame.mixer.music.play()
         self.create_window()
         self.circle_num = random.randint(40,60)

         self.gen_window_vars()
         while True:
         self.counter += 1
         cur_pos = pygame.mixer.music.get_pos()

         self.visualize(self.sampled_audio[cur_pos][1])
         self.draw_window(self.sampled_audio[cur_pos][1])

         time.sleep(0.01)
