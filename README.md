# Playlistify
A simple web parser to create Spotify playlists. As of v1.0.0, it's very rudimentary. There's basically no error checking/handling, and it only works if the website you're parsing has Spotify album links (not single tracks, etc). In later versions I hope to support other Spotify link types as well as cross-platform links (i.e. create a spotify playlist from a source of YouTube links), but that was outside of the scope of my Saturday project :).

# Background
Built using Python 3.7.3. 

To use this tool, you need the following:
- A linux machine (could be Windows/Mac with proper setup, but that's outside the scope of my intention for this)
- python3 and pip installed.

# Installation
First, lets setup some dependencies

pip install spotipy --upgrade
pip install beautifulsoup4

You also need to set up your Spotify account to be a developer account (see: https://developer.spotify.com/documentation/web-api/quick-start/) . Once that's done, you'll need to create an application. You can call it Playlistify, or whatever you want. Once you create the app you'll get your Client ID and Client Secret, which you'll need for later in the setup process. 

# Clone the Git repo
Once your environment is ready, clone the repo 

git clone https://github.com/Immortal33/Playlistify.git

# Edit the credentials file, update your application
In the repo there's a file called spotify_secrets.py. You will need to edit this file by adding your Client ID and Client Secret from your Spotify Application that you registered in the Installation phase above. 

You may notice that the file has the Spotify URI set to http:127.0.0.1:3333. You can set this to whatever URL you want (it doesn't have to be anything that resolves globally). However, at this point you need to go into your application in the Spotify dahsboard and make sure that the Redirect URI is set to the same URI that is configured in your spotify_secrets.py.  

# Running the script
At this point you should be able to run the script. The first time that you run it, you'll need to follow the instructions given by copying the URL it gives you into a web browser. This will authorize your app to make programatic changes to your Spotify account (i.e. adding playlists)
