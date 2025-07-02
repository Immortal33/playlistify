#!/usr/bin/env python

#########################################################################################
# Playlistify - A simple web parser for creating Spotify playlists 
# Files: 
#   playlistify.py - main script to parse HTML and make calls to Spotify API
#   spotify_secrets.py - file that contains your auth creds/keys for Spotify
#
# Eric Boyer
# v2.0 February 2023
##########################################################################################

# Import required modules
import spotipy
from spotify_secrets import client_id, client_secret, redirect_uri
from spotipy.oauth2 import SpotifyOAuth
import cloudscraper
import re
from tqdm import tqdm  

def Find(string):
    # This function compiles the regex to look for spotify album URLs
    # Returns: list of spotify album URLs
    
    # Match on https://open.spotify.com and any characters until a backslash, because there are unicode escape sequences.
    # Should probably make this just match the total number of characters in a Spotify Album URL (always the same so far)
    # As of this writing we're parsing the content of the whole page instead of using BeautifulSoup as in previous versions.
    regex = r"https:\/\/open\.spotify\.com\/album\/.+?(?=\\|\s|\?)"
    url = re.findall(regex,string)      
    return [x for x in url]

def gather_vars():
    # This function asks the user to supply the URL that they want to use to generate their new Spotify playlist,
    # as well as asking for a name for their new playlist. 

    print('\nWelcome to Playlistify!\n')
    source_url = input('Enter the website URL that you want to pull Spotify URLs from to make the playlist: ')
    playlist_name = input('Enter the name of the playlist you wish to create: ')
    
    ## Grab the HTML source for the supplied URL, return vars
    return source_url, playlist_name

def parse_html(source_url):
    # This function takes the URL as input, parses the contents for Spotify Album URLs and returns a list of those URLs
    
    # To get around CloudFlare hosting issues, we use the Cloudscraper module to create a session object instead of requests/etc
    scraper = cloudscraper.create_scraper()
    
    # Do a GET within the session of the actual HTML/JS source
    data = scraper.get(source_url).text

    # Populate album_urls with the URLs
    album_urls = Find(data)

    print('\nFound the following Spotify album URLs: \n')
    print(*album_urls, sep='\n')

    # A conditional to exit the script if no URLs were found from the HTML source, but return that list otherwise
    if album_urls:
        number_of_albums = len(album_urls)
        print('\nFound a total of {} album URLs\n'.format(number_of_albums))
        return album_urls
    else:
        print('No compatible Spotify album URLs were found. Goodbye!')
        exit()

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

    print('\nAdding tracks to your playlist: \n')

    # There's probably a cleaner way to do this, but this works for now. We iterate through the album URLs and get the track
    # IDs for all tracks in all albums. 
    for album in album_urls:
        results = sp.album_tracks(album)
        track_dicts.extend(results['items'])
        while results['next']:
            results = sp.next(results)
            track_dicts.extend(results['items'])
    # print(track_dicts.keys())
    # print(track_dicts.values())
    # print(track_dicts.items())
    for track in track_dicts:
        playlist_tracks.append(track['id'])
        # print('Artist: ' + track['artist'] + ' - Album: ' + track['album'] + ' - Track: ' + track['name'])
        # print(track['name'])
    # Spotipy function that makes the API call to add our tracks to the playlist 
    for track in tqdm(playlist_tracks):
        track_array = []
        track_array.append(track)
        sp.playlist_add_items(playlist_id, track_array)
        # print('\nAdding track...\n')

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
