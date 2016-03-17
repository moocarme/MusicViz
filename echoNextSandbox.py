# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 11:06:37 2016

to install the packages in Anaconda I opened the anaconda terminal and typed:
easy_install -U pyechonest
easy_install oauth2

@author: Matt
"""

from pyechonest import config
from pyechonest import artist
from pyechonest import song
import oauth2 as oauth

consumer_key = '78b970296e8236154d826f956189e336'
consumer_secret = 'Koge26dJQDSzzSOLPSDvEg'
consumer = oauth.Consumer(consumer_key, consumer_secret)

# Oauth didnt work for this website
#request_url = "http://previews.7digital.com/clip/123456"

#req = oauth.Request(method="GET", url=request_url,is_form_encoded=True)
#
#req['oauth_timestamp'] = oauth.Request.make_timestamp()
#req['oauth_nonce'] = oauth.Request.make_nonce()
#sig_method = oauth.SignatureMethod_HMAC_SHA1()
#
#req.sign_request(sig_method, consumer, token=None)
#
#print req.to_url()

config.ECHO_NEST_API_KEY="J0ILER0LQESUBJQZC"

ss_results = song.search(artist='the national', title='slow show', buckets=['id:7digital-US', 'tracks'], limit=True)
slow_show = ss_results[0]
ss_tracks = slow_show.get_tracks('7digital-US')
print ss_tracks[0].get('preview_url')
#bk = artist.Artist('bikini kill')
#print "Artists similar to: %s:" % (bk.name,)
#for similar_artist in bk.similar: print "\t%s" % (similar_artist.name,)

import sys
import os

from pyechonest import track

AUDIO_EXTENSIONS = set(['mp3', 'm4a', 'wav', 'ogg', 'au', 'mp4'])

def _bar(val, ref=100, char='='):
    if val:
        num_chars = int(val * float(ref))
        return char * max(1, num_chars)
    else:
        return char

def _is_audio(f):
    _, ext = os.path.splitext(f)
    ext = ext[1:] # drop leading '.'
    return ext in AUDIO_EXTENSIONS
    
def _show_one(audio_file):
    "given an audio file, print out the artist, title and some audio attributes of the song"
    print 'File:        ', audio_file
    pytrack = track.track_from_filename(audio_file)
    print 'Artist:      ', pytrack.artist if hasattr(pytrack, 'artist') else 'Unknown'
    print 'Title:       ', pytrack.title if hasattr(pytrack, 'title') else 'Unknown'
    print 'Track ID:    ', pytrack.id
    print 'Tempo:       ', pytrack.tempo
    print 'Energy:       %1.3f %s' % (pytrack.energy, _bar(pytrack.energy))
    if not pytrack.valence:
        # Track hasn't had latest attributes computed. Force an upload.
        pytrack = track.track_from_filename(audio_file, force_upload=True)
    print 'Valence:      %1.3f %s' % (pytrack.valence, _bar(pytrack.valence)) 
    print 'Acousticness: %1.3f %s' % (pytrack.acousticness, _bar(pytrack.acousticness))
    print


def show_attrs(directory):
    "print out the tempo for each audio file in the given directory"
    for f in os.listdir(directory):
        if _is_audio(f):
            path = os.path.join(directory, f)
            _show_one(path)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'usage: python show_tempos.py path'
    else:
        show_attrs(sys.argv[1])
def get_tempo(artist, title):
#    "gets the tempo for a song"
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        return results[0].audio_summary['tempo']
    else:
        return None

def get_energy(artist, title):
#    "gets the tempo for a song"
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        return results[0].audio_summary['energy']
    else:
        return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python tempo.py 'artist name' 'song title'"
    else:
        tempo = get_tempo(sys.argv[1], sys.argv[2])
        if tempo:
            print 'Tempo for', sys.argv[1], sys.argv[2], 'is', tempo
        else:
            print "Can't find Tempo for artist:", sys.argv[1], 'song:', sys.argv[2]