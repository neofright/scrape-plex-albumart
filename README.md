# scrape-plex-albumart

I needed a way to get accurate album art for Rockbox on my iPod6g. Seeing as I already had my library indexed in Plex and the albumart scraping has been very reliable I decided to export the album art this way.

If your library on-disk of your Plex server looks something like:

```/mnt/Music/albums/artist/album/track.ext```

Then this script will create a mirrored directory structure in its working directory like this:

```/path/to/wherever/you/are/running/this/from/mnt/Music/albums/artist/artist/folder.jpg```

etc.

This allows you to manually merge the directory trees and you can decide if you want to overwrite files etc.

For my use case - I just copy this album art tree to my iPod over USB.

## Usage:
Change the contents of the `baseurl` and `token` variables and run the script. It is completely barebones with no args and nothing is printed to stdout.
