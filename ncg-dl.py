#!/usr/bin/env python
import youtube_dl

DOWNLOAD_DIR = '/media/NETCODE-VIDEOS/%(title)s.%(ext)s'
with open('urls.txt', 'w+') as urls:
    with open('links.csv', 'r') as f:
        for line in f:
            print line
            if 'link,title' in line:
                print "link,title"
                continue
            url='http://player.vimeo.com/video/{id}\n'.format(id=line.split(',')[0])
            print url
            urls.write(url)
        
youtube_dl.main([url,'-a', 'urls.txt', '-o', DOWNLOAD_DIR])
	
