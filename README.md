Muton
=====

Satus
-----

This is student project. Work in progress.


Description
-----------

Muton is a musical garbage collector. Vice versa.
It takes your collection and parses tags and content. 
In output - ordered playlists, you may order them 
yourself or trust the machine ;). 

Also Muton can compare musical collections and build 
playlists of differences. This feature is a cherry in
the chaos of your musical tastes.


Idea
----
 
 1. Very often our musical collection is unordered 
folder with some part of torrents etc.
 
 2. Always we try to collect musical garbage: 
 copying & moving files, tagging something.

 3. Stop it! Chaos doesn't matter now!

 4. Surprise! Playlists!

 5. Of course using correct tags.
 
 6. Playlist let us save meta information beyond music file.

 7. You don't have to edit file tags now.

 8. If file don't have a tag, Muton does it automatically.
	Of course, a bit of magic ;)

 9. Muton generates neat playlists: by genre, 
 	by artist, by album, by year, etc.
 10. Listen your collection, lazy :)


Features
--------

 1. If you wanna intersect your collection with friend, you can do that!
 	You use Muton to build the playlist of differences.

 1.1. You can copy the collection difference in one click.

 2. If your collection has lost, you always can repair collection description.


Package organization
--------------------

 * muton.py   - main controller;

 * vault.py   - backend for tags;

 * collect.py - collector of collection of tags;

 * autorec.py - find tags by musical fingerprint (ex.: PUID, AcoustID);

 * diffcol.py - build differences between two or more collections;

 * buildpl.py - build playlists in m3u format.
