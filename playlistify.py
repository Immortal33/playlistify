#!/usr/bin/env python

##########################################################################################
# Playlistify - A simple web parser for creating Spotify playlists 
# Files: 
#   playlistify.py - main script to parse HTML and make calls to Spotify API
#   spotify_secrets.py - file that contains your auth creds/keys for Spotify
#
# Eric Boyer
# November 2020
##########################################################################################

#Import required modules
from spotify_secrets import CLIENT_ID, CLIENT_SECRET
import spotipy

#test import
print(CLIENT_ID)
print(CLIENT_SECRET)
