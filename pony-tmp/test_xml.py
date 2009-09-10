import xml.dom.minidom
   
def my_xml():
    doc = xml.dom.minidom.Document()
    
    media_info_el = doc.createElement("MediaInfo")
    doc.appendChild(media_info_el)
    
    album_info_el = doc.createElement("AlbumInfo")
    media_info_el.appendChild(album_info_el)
    
    artist_el = doc.createElement("Artist")
    album_info_el.appendChild(artist_el)
    artist_txt = doc.createTextNode("Skyfire")
    artist_el.appendChild(artist_txt)
    
    album_el = doc.createElement("Album")
    album_info_el.appendChild(album_el)   
    alb_txt = doc.createTextNode("Fractal")
    album_el.appendChild(alb_txt)
    
    year_el = doc.createElement("Year")
    album_info_el.appendChild(year_el)  
    year_txt = doc.createTextNode("2009")
    year_el.appendChild(year_txt)
    
    genre_el = doc.createElement("Genre")
    album_info_el.appendChild(genre_el)  
    genre_txt = doc.createTextNode("Melodic-Death Metal")
    genre_el.appendChild(genre_txt)
    
    bitr_el = doc.createElement("Bitrate")
    album_info_el.appendChild(bitr_el)  
    bitr_txt = doc.createTextNode("320")
    bitr_el.appendChild(bitr_txt)
    
    fmt_el = doc.createElement("Format")
    album_info_el.appendChild(fmt_el)  
    fmt_txt = doc.createTextNode("mp3")
    fmt_el.appendChild(fmt_txt)
    
    size_el = doc.createElement("Size")
    album_info_el.appendChild(size_el)  
    size_txt = doc.createTextNode("5.78")
    size_el.appendChild(size_txt)
    
    comm_el = doc.createElement("Comment")
    album_info_el.appendChild(comm_el)  
    comm_txt = doc.createTextNode("Germany")
    comm_el.appendChild(comm_txt)
    
    f = open('output.xml', "w")
    doc.writexml(f, newl="\n", addindent="    ", encoding="UTF-8")
    f.close()

my_xml()