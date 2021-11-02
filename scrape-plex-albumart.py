import plexapi
import requests
import os
import urllib.request, urllib.parse, urllib.error

from plexapi.server import PlexServer
baseurl = 'http://0.0.0.0:32400'
token = ''
plex = PlexServer(baseurl, token)

library_name = 'Music'

music = plex.library.section(library_name)
for album in music.searchAlbums():    
    if album.thumb is not None:
        ## album directory. Very expensive call to determine as we must get all tracks. I can't find a better way right now.
        ## Help from https://old.reddit.com/r/PleX/comments/gbu32h/get_filepath_of_directory_where_movie_is_located/fp860d2/
        album_directory = os.path.dirname(album.tracks()[0].media[0].parts[0].file)
        if not os.path.isdir(album_directory[1:]):
            os.makedirs(album_directory[1:])

        album_jpeg_path = os.path.join(album_directory[1:], 'folder.jpg')
        if not os.path.isfile(album_jpeg_path):
            album_artwork_url = baseurl + album.thumb + "?X-Plex-Token=" + token
            r = requests.get(album_artwork_url)
            with open(album_jpeg_path, 'wb') as f:
                f.write(r.content)

