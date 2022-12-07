# scrape-plex-albumart

I needed a way to get accurate album art for Rockbox on my iPod6g. Seeing as I already had my library indexed in Plex and the albumart scraping has been very reliable I decided to export the album art this way.

If your music library on your Plex server looks something like this on-disk:

```/mnt/Music/albums/artist/album/track.ext```

Then this script will create a mirrored directory structure in its working directory like this:

```/path/to/wherever/you/are/running/this/from/mnt/Music/albums/artist/album/folder.jpg```

etc.

This allows you to manually merge the directory trees and you can decide if you want to overwrite files etc.

For my use case - I just rsync this album art tree to my iPod over USB.

I have not made any attempt to allow this to run from Windows (it assumes *NIX server and client) but could be made to work if you take care of the path separators.

Supports 2FA and will convert progressive scan images to baseline for compatibility with Rockbox.

## Usage:
Create a .env file with the following contents (substituting real values):

    plex_server = ''
    plex_username = ''
    plex_password = ''
    plex_library = 'Music,Music DnB'

Note that `plex_server` is the server _name_ and not the URL.

## Requirements:
ImageMagick (identify and convert)

plexapi

python-dotenv

## Update 2022:
This repo is now archived in favor of [neofright/scrape-plex-albumart-bash](https://github.com/neofright/scrape-plex-albumart-bash)
