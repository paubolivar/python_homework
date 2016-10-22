
# Python course day 4 exercise
# Paulina 


###########################################################################
#Import internal modules
###########################################################################

import webbrowser
import os

###########################################################################
#Define Class Song
###########################################################################

class Songs(object):
    """It's a class that describes the songs and has titel, artis, durtion as attributes"""
    def __init__(self, title = None, artist = None, duration = None): 
        self.title = title
        self.artist = artist
        self.duration = duration
        try:
            self.duration = int(duration)
            if self.duration < 0:
                raise Exception("The duration of the song is a negative number. Please check the duration of this song.") 
        except ValueError:  
            self.duration = 0
            print "Warning: the duration of the song - %s - is 0. Check the duration is a number" % self.title        
            

    def pretty_duration(self):
        """Returns a nice string describing the duration. For instance if the duration is 3611, this methods takes \
        no input and returns "01 hours 00 minutes 11 seconds" as a string."""
        m, s = divmod(self.duration, 60)
        h, m = divmod(m, 60)
        return "%02d hours %02d minutes %02d seconds" % (h, m, s)
        
    def play(self):
        """Automatically opens a youtube search for the title on your computer browser."""
        url = "http://youtube.com/results?search_query=%s" % self.title
        webbrowser.open(url)



###########################################################################
#Import file with songs and make each line an instance of the class Song()
###########################################################################

path = os.environ["HOME"] + "/"
f = open(path + "lulu_mix_16.csv")
next(f)
songs_list = [line.strip().split(",") for line in f]

songs = []
for s in songs_list: 
    song = Songs(artist = s[1], title = s[0], duration = s[2])
    songs.append(song)

    
for s in songs: print s.artist  
for s in songs: print s.pretty_duration()    
print sum(s.duration for s in songs), "seconds in total"    
songs[6].play()                      

