#!/usr/bin/env python

#########################################################################################
# Playlistify - A simple web parser for creating Spotify playlists 
# Files: 
#   playlistify.py - main script to parse HTML and make calls to Spotify API
#   spotify_secrets.py - file that contains your auth creds/keys for Spotify
#
# Eric Boyer
# November 2020
##########################################################################################

# Import required modules
import spotipy
from spotify_secrets import client_id, client_secret, redirect_uri
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests
import re
import pprint

def gather_vars():
    # This function asks the user to supply the URL that they want to use to generate their new Spotify playlist,
    # as well as asking for a name for their new playlist. 
    print('\nWelcome to Playlistify!\n')
    source_url = input ('Enter the website URL that you want to pull Spotify URLs from to make the playlist: ')
    playlist_name = input('Enter the name of the playlist you wish to create: ')
    
    # Grab the HTML source for the supplied URL, return vars
    url = requests.get(source_url)
    return url, playlist_name

def parse_html(url):
    # This function takes the HTML from the previous function and parses it using BeautifulSoup
    data = url.text
    soup = BeautifulSoup(data, 'lxml')
    
    # We want to get only links, specifically only open.spotify.com/album/ links
    # Future updates could add different URL types 
    tags = soup.find_all('a', {'href': re.compile(r'open\.spotify\.com/album')})
    
    # Initialize album_url list 
    album_urls = []

    print('\nFound the following Spotify album URLs: \n')
    
    # We iterate through the list of URLs and remove any HTML tags and query strings,
    # and we return the list of URLs as output
    for tag in tags:
        tag = tag.get('href')
        split_string = tag.split('?',1)
        tag = split_string[0]
        album_urls.append(tag)
        print(tag)
    return album_urls

def create_playlist(playlist_name, album_urls):
    # This function takes the list of URLs and our playlist name that we gathered in the above two functions, and uses those to 
    # actually do the Spotify API calls needed to create the playlist and populate it with all of the tracks from the albums

    # Here we define the Spotify API endpoint that we'll reference in our API call, which defines the action we will take
    scope = "playlist-modify-public"
   
    # Here we initialize the authorization variables needed for us to connect to the Spotify Web API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,open_browser=False))
    user_id = sp.me()['id']
    
    # Spotipy function that makes the API call to make the playlist
    playlist_id_dict = sp.user_playlist_create(user_id, playlist_name)
    
    # We need to get the playlist ID of the playlist we just created
    playlist_id = playlist_id_dict['id']

    # Initialize list vars
    playlist_tracks = []
    track_dicts = []

    print('\nFound the following tracks to add to your playlist: \n')

    # There's probably a cleaner way to do this, but this works for now. We iterate through the album URLs and get the track
    # IDs for all tracks in all albums. 
    for album in album_urls:
        results = sp.album_tracks(album)
        track_dicts.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            track_dicts.extend(results['items'])
    for track in track_dicts:
        playlist_tracks.append(track['id'])
        print(track['name'])
    # Spotipy function that makes the API call to add our tracks to the playlist 
    for track in playlist_tracks:
        track_array = []
        track_array.append(track)
        sp.playlist_add_items(playlist_id, track_array)
        print('\nAdding track...\n')

def main():
    # The main function, which calls all of the previous functions.
    url,playlist_name = gather_vars()
    album_urls = parse_html(url)
    create_playlist(playlist_name, album_urls)
    print('\nPlaylist successfully added! Enjoy!\n')

# Here we run the main function. 
if __name__ == '__main__':
    main()

#END OF FILE
