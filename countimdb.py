import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

html = urlopen("http://www.imdb.com/chart/top")
soup = BeautifulSoup(html.read())
poster_columns = soup.findAll('td', {'class':'posterColumn'})
print len(poster_columns)
count=1
for poster in poster_columns:
            x = poster.findNextSibling('td')
            y = x.findNextSibling('td')
            title = x.a.text
            hover_text = x.a['title']
            movie_url = 'http://www.imdb.com/'+str(poster.a['href'])
	    mv_url_id = movie_url.split('/?', 1)[0]
	    print mv_url_id
	    html1 = urlopen(movie_url)
	    mpage = BeautifulSoup(html1.read())
	    #to find summary
	    mov_sum =  mpage.find('div',{'class':'summary_text'}).text

	    #to find year
	    mov_year = mpage.find('span',{'id':'titleYear'}).a.text

	    #to find ratings
	    mov_rating = mpage.find('span',{'itemprop':'ratingValue'}).text
	    mov_ratingcount = mpage.find('span',{'itemprop':'ratingCount'}).text

	    #to find genre
	    mov_genre = mpage.findAll('span',{'itemprop':'genre'})
	    for mov_genre_each in mov_genre:
		print mov_genre_each.text
	   
	    #to get other details
	    mov_details = mpage.find('div',{'id':'titleDetails'})
	    mov_x = mov_details.findNext('div',{'class':'txt-block'})
	    mov_y = mov_x.findNext('div',{'class':'txt-block'})
	    mov_country = mov_y.a.text
	    mov_z = mov_y.findNext('div',{'class':'txt-block'})
	    mov_z_as = mov_z.findAll('a')
	    #prints all languages
	    for mov_z_a in mov_z_as:
		print mov_z_a.text

	    #duration of movie
	    mov_time = mpage.find('time',{'itemprop':'duration'}).text

	    
	    print mov_time
	    print mov_country
	    print mov_rating
	    print mov_ratingcount

	    print mov_year
	    print mov_sum
            img_url = poster.a.img['src']
            rating = y.strong.text
            no_of_votes = str(y.strong['title']).split(' ')[3]
            print count,'.', title, '\n\t', hover_text, '\n\t', movie_url, '\n\trating:', rating, '\n'

	    #to find cast list 
	    cast_link = mv_url_id+str('/fullcredits?ref_=tt_cl_sm#cast')
	    html2 = urlopen(cast_link)
            castpage = BeautifulSoup(html2.read())
	    cast_list = castpage.find('table',{'class':'cast_list'})
	    cast_tr = cast_list.findAll('tr')
	    for cast_td in cast_tr:
		td1 = cast_td.find('span',{'class':'itemprop'})
		if td1 is None: #some thing was none in between
			continue
		td1text = td1.text
		td2 = cast_td.find('td',{'class':'character'})
		td2text = td2.text
		print '\n\t\t'
		print "charname : ", td2text, " actorname : ", td1.text

	    #related keyword link
	    rel_link = mv_url_id+str('/keywords?ref_=tt_stry_kw')
	    print '\n\t realted data keywords @', rel_link
            html3 = urlopen(rel_link)
            relpage = BeautifulSoup(html3.read())
            rel_list = relpage.findAll('div',{'class':'sodatext'})
            for rel_item in rel_list:
		reldata = rel_item.a.text
		print '\n\t\t', reldata
	    count+=1
