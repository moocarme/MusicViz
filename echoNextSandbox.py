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
from pyechonest import track
import matplotlib.pyplot as plt
import oauth2 as oauth
import sys
import os

config.ECHO_NEST_API_KEY="J0ILER0LQESUBJQZC"
consumer_key = '78b970296e8236154d826f956189e336'
consumer_secret = 'Koge26dJQDSzzSOLPSDvEg'
consumer = oauth.Consumer(consumer_key, consumer_secret)

# Oauth didnt work for this website ===========================================
#
#
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

# Helper functions ============================================================

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


def get_tempo(artist, title):
#    "gets the tempo for a song"
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        return results[0].audio_summary['tempo']
    else:
        return None

def get_allData(artist, title):
#    gets the various data for a song
# Use help(song.search) for other useful data
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        tempo = results[0].audio_summary['tempo']
        energy = results[0].audio_summary['energy']
        valence = results[0].audio_summary['valence']
        acousticness = results[0].audio_summary['acousticness']
        return tempo, energy, valence, acousticness
    else:
        return None
def get_energy(artist, title):
#    "gets the tempo for a song"
    results = song.search(artist=artist, title=title, results=1, buckets=['audio_summary'])
    if len(results) > 0:
        return results[0].audio_summary['energy']
    else:
        return None
        
# =============================================================================       
AUDIO_EXTENSIONS = set(['mp3', 'm4a', 'wav', 'ogg', 'au', 'mp4'])

# Example of song searching for song ==========================================
#ss_results = song.search(artist='the national', title='slow show', buckets=['id:7digital-US', 'tracks'], limit=True)
#slow_show = ss_results[0]
#ss_tracks = slow_show.get_tracks('7digital-US')
#print ss_tracks[0].get('preview_url')
#bk = artist.Artist('bikini kill')
#print "Artists similar to: %s:" % (bk.name,)
#for similar_artist in bk.similar: print "\t%s" % (similar_artist.name,)



#Can only search 100 at a time=================================================
# searching for country artists
#d1 = artist.search(style = 'country', results = 100)
#d2 = artist.search(style = 'country', start = 100, results = 100)

# searching for country songs
#s1 = song.search(style = 'country', results = 100)
#s2 = song.search(style = 'country', start = 100, results = 100)
#==============================================================================
tempo, energy, valence, acousticness, liveness, speechiness, keys, mM, danceability = [], [], [], [], [], [], [], [], []

# Need to go through each year as can only get 100 entries per search
noResults = 1000
for i in range(noResults/100):
    songs = song.search(style = 'country', buckets = 'audio_summary', start = i*100, results = 100, \
        artist_start_year_after = 1990, artist_start_year_before = 1995)
    for theSong in songs:
        tempo.append(theSong.audio_summary['tempo'])
        energy.append(theSong.audio_summary['energy'])
        valence.append(theSong.audio_summary['valence'])
        acousticness.append(theSong.audio_summary['acousticness'])
        liveness.append(theSong.audio_summary['liveness'])
        speechiness.append(theSong.audio_summary['speechiness'])
        keys.append(theSong.audio_summary['key'])
        mM.append(theSong.audio_summary['mode'])
        danceability.append(theSong.audio_summary['danceability'])
        
plt.figure(200); plt.clf()
plt.hist(acousticness, bins = 10)