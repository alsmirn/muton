# -*- coding: utf-8 -*-

from mutagen.apev2 import APEv2
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.asf import ASF
from mutagen.id3 import ID3
import re, getopt, sys
from optparse import OptionParser

def usage():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--extr",
                  help="Extracts media file by the sign from the tag") 
    print 'ttt'

def audio():
    #ape_audio = APEv2("E:/Test/Red Sparowes - At The Soundless Dawn.ape")
    #ogg_audio = OggVorbis('E:\\Test\\01 - Austin TV - Ana No Te Fall.ogg')
    #flac_audio = FLAC('E:/Test/Test2/05 - God Is An astronaut - First Day of Sun.flac')
    mp3_audio = MP3("E:\\Music\\Vast\\1998 Visual Audio Sensory Theater\\10 - Vast - Somewhere Else To Be.mp3")
    
    #wma_audio = ASF(u"E:/Test/Test2/13 - Harvest Rain - Glowing Across.wma")
    mp3_tags = mp3_audio
    print mp3_tags
    #print mp3_tags['TPE1']
    #print mp3_audio["COMM:SL Comment:'eng'"]
    

    #usage()
#    try:                                
#        opts, args = getopt.getopt(argv, 'h', ['help'])
#    except getopt.GetoptError:
#        usage()
#        sys.exit(2)
#    for opt, arg in opts:
#        if opt in ("-h", "--help"):
#            usage()                     
#            sys.exit() 
audio()