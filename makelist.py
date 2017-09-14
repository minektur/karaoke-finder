#!/usr/bin/env python

from subprocess import check_output


#output format looks like this with tabs between the fields 

#Dir     Pathname        Artist  Title
#999     10,000 Maniacs - Because The Night .cdg 10,000 Maniacs  Because The Night 
#999     10,000 Maniacs - More Than This .cdg    10,000 Maniacs  More Than This 
#999     10,000 Maniacs - These Are The Days .cdg        10,000 Maniacs  These Are The Days 
#999     10,000 Maniacs - Trouble Me .cdg        10,000 Maniacs  Trouble Me 
#999     10 Cc - Donna .cdg      10 Cc   Donna 
#999     10 Cc - Dreadlock Holiday .cdg  10 Cc   Dreadlock Holiday 


fl = check_output(["sh", "-c", "cd ~/Downloads/kar/all; find [A-Z] 999 | grep -i cdg | sort"]).decode("utf-8").split("\n")

of = open("/usr/local/fred/kar/karaoke-finder/filelist.tsv", 'w')

of.write("Dir\tPathname\tArtist\tTitle\n")

for f in fl:
    if len(f.strip()) == 0:
        continue
    directory, pathname = f.split('/', 1)
    artist , rest = pathname.split(' - ', 1)
    title, rest = rest.split('.cdg')  
    if len(rest) > 0:
        print ("%s: messed up" % f)

    directory = directory.strip()
    artist = artist.strip()
    title = title.strip()
    pathname = pathname.strip()
    of.write("%s\t%s\t%s\t%s\n" % (directory, pathname, artist, title))

    

#cp /usr/local/fred/kar/karaoke-finder/filelist.tsv ~/Downloads/


