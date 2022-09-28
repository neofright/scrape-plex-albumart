#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import plexapi
from plexapi.myplex import MyPlexAccount
import re
import requests
import subprocess
import urllib.request, urllib.parse, urllib.error

def is_jpg_progressive(jpeg_file):
    cmd = ['identify', '-verbose', jpeg_file]
    sp = subprocess.Popen(cmd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    rc=sp.wait()
    out,err=sp.communicate()
    if re.search('Interlace: None', out):
        return True
    else:
        return False

def convert_progressive_jpg_to_baseline(jpeg_file):
    cmd = ['convert', jpeg_file, '-interlace', 'none', jpeg_file]
    sp = subprocess.Popen(cmd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    rc=sp.wait()
    if rc != 0:
        out,err=sp.communicate()
        print(err)

def scrape_plex_albumart(library_name):
    music = plex.library.section(library_name)
    for album in music.searchAlbums():
        if album.thumb is not None:
            ## album directory. Expensive call to determine as we must get all tracks. I can't find a better way right now.
            ## Help from https://old.reddit.com/r/PleX/comments/gbu32h/get_filepath_of_directory_where_movie_is_located/fp860d2/
            album_directory = os.path.dirname(album.tracks()[0].media[0].parts[0].file)
            if not os.path.isdir(album_directory[1:]):
                os.makedirs(album_directory[1:])

            album_jpeg_path = os.path.join(album_directory[1:], 'folder.jpg')
            if not os.path.isfile(album_jpeg_path):
                album_artwork_url = plex.transcodeImage(album.thumb, '320', '320')
                #album_artwork_url = baseurl + album.thumb + "?X-Plex-Token=" + token
                r = requests.get(album_artwork_url)
                with open(album_jpeg_path, 'wb') as f:
                    print('Writing ' + album_jpeg_path)
                    f.write(r.content)
                ## convert progressive jpeg to baseline.
                if is_jpg_progressive(album_jpeg_path):
                    print('Converting to baseline.')
                    convert_progressive_jpg_to_baseline(album_jpeg_path)

## https://codereview.stackexchange.com/a/257530
def input_yes_no(prompt: str) -> bool:
    full_prompt = f'{prompt} ([Y]/N): '
    while True:
        answer = input(full_prompt).strip()
        if answer == '':
            return True

        answer = answer[0].lower()
        if answer == 'y':
            return True
        if answer == 'n':
            return False
        print('ERROR')

if __name__ == "__main__":
    load_dotenv()
    #######################################
    mfa_enabled = input_yes_no('Does your Plex account use 2FA?')
    if mfa_enabled:
        mfa_token = input('Enter Plex TOTP token: ')
    else:
        mfa_token = ""
    #######################################
    account = MyPlexAccount(os.environ.get('plex_username'), os.environ.get('plex_password') + mfa_token)
    plex = account.resource(os.environ.get('plex_server')).connect()  # returns a PlexServer instance
    #token = account.authenticationToken
    #baseurl = plex._baseurl
    #######################################
    scrape_plex_albumart(os.environ.get('plex_library'))