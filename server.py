#!/usr/bin/env python

import os
import shutil

from bottle import route, run, template, error, static_file

#Where the web stuff lives
basedir = "webroot"

#where the karaoke files live
karbase = "/home/chronos/user/Downloads/kar/all"


def find_usb():
    """ use a variety of heuristics to find the mounted usb drive.
      In particular, it's drive lable should be KARAOKE and there 
      should be a 0 length file in the root dir named 'ktmp'
      
      returns a tuple of (device, mounted-path)
          e.g. ("/dev/sdb1", "/Volumes/KARAOKE") 
    """
    #do something smart here with fdisk -l or df or both
    #return("/dev/sdb1", "/Volumes/KARAOKE")
    return("/dev/sdb1", "/media/removable/KARAOKE")


#@error(404)
#def fourofour(obj):
#    return root()

#https://www.appsheet.com/start/8c032ee2-7eb2-490e-9059-26a9c650bb04
#https://www.appsheet.com/preview/8c032ee2-7eb2-490e-9059-26a9c650bb04

@route("/")
def root():
    return """<html> Return to the song search by closing this tab, or click here <a href="https://www.appsheet.com/start/8c032ee2-7eb2-490e-9059-26a9c650bb04"> Karaoke Song Finder </a></html>"""


@route("/unmount")
def unmount():
   dev, usbpath = find_usb() 
   # do nothing for now - no command-line way to eject usb for chromeos
   


def copy_failure(msg):
    return template("Error: {{mmm}}", mmm=msg)

def copy_success(track):
    return """<html> <h1> Song<br><br>%s<br><br>successfully copied.  Return to  <a href="https://www.appsheet.com/preview/8c032ee2-7eb2-490e-9059-26a9c650bb04"> Karaoke Song Finder </a></h1></html>""" % (track)


@route("/copyfile/<filedir>/<track>")
def copyfile(filedir='', track=''):
    """ takes a directory (e.g. "B") and a track name 
    (e.g. "Banarama - Venus.cdg")
    and validates a bunch of things, then checks to see if destination USB
    is mounted, copies the file.
    """
    #cleanse filename
    if ".." in os.path.join(filedir, track):
        return copy_failure("Invalid File Name")

    #allow only cdg files
    if not track.endswith(".cdg"):
        return copy_failure("CDG files only")

    # no starting slash
    if filedir.startswith("/"):
        return copy_failure("relative paths only")

    #stat dir
    sourcedir = os.path.join(karbase, filedir)
    if not os.path.isdir(sourcedir):
        return copy_failure("dir not found")

    #stat file
    sourcefile = os.path.join(sourcedir, track)
    if not os.path.isfile(sourcefile):
        return copy_failure("track not found")

    #check for good usb with magic token in parent dir
    dev, mount = find_usb()
    if os.path.basename(mount) != 'KARAOKE':
        return copy_failure("Could not find USB named KARAOKE " + mount)

    checkfile = os.path.join(mount,"ktmp")
    if not os.path.isfile(checkfile):
        return copy_failure("Can't find ktmp file " + checkfile)

    #success?  then copy the files and return success template
    shutil.copy(sourcefile, mount)

    sourcefile2 = os.path.splitext(sourcefile)[0]+".mp3"
    shutil.copy(sourcefile2, mount)
    
    return copy_success(track)

@route("/playfile/<filedir>/<track>")
def playfile(filedir='', track=''):
    """ takes a directory and track name and sends/plays/streams it as mp3 """ 
    #cleanse filename
    if ".." in os.path.join(filedir, track):
        return copy_failure("Invalid File Name")

    #allow only cdg files
    if not track.endswith(".cdg"):
        return copy_failure("cdg files only")

    # no starting slash
    if filedir.startswith("/"):
        return copy_failure("relative paths only")

    #stat dir
    sourcedir = os.path.join(karbase, filedir)
    if not os.path.isdir(sourcedir):
        return copy_failure("dir not found")

    #stat file
    sourcefile = os.path.join(sourcedir, track)
    if not os.path.isfile(sourcefile):
        return copy_failure("track not found")

    return static_file(track.replace(".cdg",".mp3"), sourcedir,  mimetype="audio/mpeg")
    #return static_file("null", "dev",  mimetype="audio/mpeg")


run(host='localhost', port=2222, debug=True)
