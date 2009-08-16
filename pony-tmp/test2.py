# -*- coding: utf-8 -*-

import cProfile, pstats

from mutagen.apev2 import APEv2
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.asf import ASF
from mutagen.id3 import ID3
import re, getopt, sys, os

try:
     import pygtk
     pygtk.require("2.16")
except:
      pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)



class App:

    def __init__(self):
        # Загружаем файл интерфейса
        self.gladefile = "Second.glade"
        # дерево элементов интерфейса

        self.widgetsTree = gtk.glade.XML(self.gladefile)
        # Словарик, задающий связи событий с функциями-обработчиками
        dic = { 
        "button1_clicked_cb" : self.text_operation,
                "button2_clicked_cb": self.text_operation,
          }
        # Магическая команда, соединяющая сигналы с обработчиками
        self.widgetsTree.signal_autoconnect(dic)
        # Соединяем событие закрытия окна с функцией завершения приложения￿
        self.window = self.widgetsTree.get_widget("window1")
        if (self.window):
            self.window.connect("destroy", self.close_app)
        # А это уже логика приложения. Задём маршруты обработки текста для каждой кнопки.
        # Первый элемент - имя виджета-источника текста, второй - имя виджета-получателя  
        self.routes = {'button1': ('textview1','textview2'),
                   'button2': ('textview2','textview1')}

    def text_operation(self,widget):
        "Функция, которая перебрасывает текст туда-сюда"
        # виджет-источник
        source = self.widgetsTree.get_widget(self.routes[widget.name][0])
        # виджет-получатель
        destination = self.widgetsTree.get_widget(self.routes[widget.name][1])
        # текстовый буфер источника
        source_text_buffer = source.get_buffer()
        # массив итераторов границ текста в текстовом буфере источника (начало и конец)
        source_text_buffer_bounds = source_text_buffer.get_bounds()
        # собственно текст
        source_text = source_text_buffer.get_text(source_text_buffer_bounds[0],
                                                  source_text_buffer_bounds[1])
        # устанавливаем текст в текстовом буфере виджета-получателя￿
        destination.get_buffer().set_text(source_text)
        # очищаем текстовый буфер источника
        source_text_buffer.set_text('')
           
    def close_app(self, widget):    
        gtk.main_quit()   

#class Troll():
#    
#    def test(path):   
#        mp3_audio = MP3(path)
#        print mp3_audio.items()
#            
#def main():
#    #ape_audio = APEv2("E:/Test/Red Sparowes - At The Soundless Dawn.ape")
#    #ogg_audio = OggVorbis('E:\\Test\\01 - Austin TV - Ana No Te Fall.ogg')
#    #flac_audio = FLAC('E:/Test/Test2/05 - God Is An astronaut - First Day of Sun.flac')
#    #wma_audio = ASF(u"E:/Test/Test2/13 - Harvest Rain - Glowing Across.wma")
#    troll = Troll()   
#    troll.test()
    
if __name__ == "__main__":
    app = App()
    gtk.main()




