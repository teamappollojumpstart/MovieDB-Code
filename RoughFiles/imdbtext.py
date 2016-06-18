import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
 
try:
    with open('imdb.txt') as f: pass
    print "File (imdb.txt) already exists."
except IOError as e:
    print "Generating new file (imdb.txt)."
    try:
        text = urlopen('imdb.htm').read()
	print "inside loop" 
        soup = BeautifulSoup(text)
 
        f = open("imdb.txt", "w")
 
        table = soup.find('table')
 
        links = table.findAll('a')
        for item in links:
            f.write(item.string + '\n')
	    print "inside" 
        f.close()
    except:
        print "Target file (imdb250.htm) could not be found."
