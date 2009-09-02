"""

Some experiments.

"""

class MediaFileInfo2(object):
    __slots__ = (
            'tag_error', 'rec_dates', 'artist', 
            'total_samples')
    
    def __init__(self, *args, **kwargs):
        pass

    def get_tags(self):
        """return list of all possible tags"""
        return self.__slots__
    
    def get_actual_tags(self):
        """return list of all initialized tags"""
        actual_tags = {}
        for tag in self.__slots__:
            try:
                actual_tags[tag] = self.__getattribute__(tag)
            except AttributeError:
                pass
        return actual_tags
    
    def get_tag(self, tag_name):
        """simple getter by tag_name"""
        try:        
            return self.__getattribute__(tag_name)
        except AttributeError:
            raise Exception("Tag with name '%s' does not exist." % tag_name)
            
        
instance = MediaFileInfo2()
instance.artist = 'b'
print instance.artist
print instance.get_tags()

print instance.get_tag('artis')
print instance.get_actual_tags()
#print dir(instance.__slots__)

#print instance.__getattribute__('artist')
