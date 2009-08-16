from mutagen.mp3 import MP3
import cProfile, pstats

def mp3_reader():

    mp3_audio = MP3('D:\\Downloads\\Raubtier\\2009 Det finns bara krig\\01 - Raubtier - Det finns bara krig.mp3')
#    print mp3_audio.items()
cProfile.run('mp3_reader()', 'log')
p = pstats.Stats('log')
#p.strip_dirs().sort_stats('calls').print_stats(20)
p.sort_stats('calls', 'file').print_stats()

#mp3_reader()