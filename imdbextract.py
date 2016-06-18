import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import time

print "Start : %s" % time.ctime()
html = urlopen("http://www.imdb.com/chart/top")
soup = BeautifulSoup(html.read())
poster_columns = soup.findAll('td', {'class':'posterColumn'})
print "script generates the top250 data from imdb and write output to xml file"
print "to get data of: ",len(poster_columns)
count=1
movies = Element('movies')
for poster in poster_columns:
            x = poster.findNextSibling('td')
            y = x.findNextSibling('td')
            title = x.a.text
	    movie = SubElement(movies, 'movie')
	    SubElement(movie,'title',name='title').text=title
            hover_text = x.a['title']
	    hover_text = hover_text.split('(dir.)', 1)[0]
	    SubElement(movie,'director',name='director').text=hover_text
	    movie_url = 'http://www.imdb.com/'+str(poster.a['href'])
	    mv_url_id = movie_url.split('/?', 1)[0]
	    SubElement(movie,'movieurl',name='movieurl').text=mv_url_id
	    print  'accessign ',count,"::", title ,'from',  mv_url_id
	    html1 = urlopen(movie_url)
	    mpage = BeautifulSoup(html1.read())
	    #to find summary
	    mov_sum =  mpage.find('div',{'class':'summary_text'}).text
	    SubElement(movie,'summary',name='summary').text=mov_sum
	    #to find year
	    mov_year = mpage.find('span',{'id':'titleYear'}).a.text
	    SubElement(movie,'titleyear',name='titleyear').text=mov_year
	    #to find ratings
	    mov_rating = mpage.find('span',{'itemprop':'ratingValue'}).text
	    SubElement(movie,'ratingvalue',name='ratingvalue').text=mov_rating
	    mov_ratingcount = mpage.find('span',{'itemprop':'ratingCount'}).text
	    SubElement(movie,'ratingcount',name='ratingcount').text=mov_ratingcount
	    #to find genre
	    mov_genre = mpage.findAll('span',{'itemprop':'genre'})
	    genres = SubElement( movie,'genres')
	    for mov_genre_each in mov_genre:
		SubElement(genres,'genre',name='genre').text=mov_genre_each.text
		#print mov_genre_each.text
	
	    #to get other details
	    mov_details = mpage.find('div',{'id':'titleDetails'})
	    mov_x = mov_details.findNext('div',{'class':'txt-block'})
	    mov_y = mov_x.findNext('div',{'class':'txt-block'})
	    mov_country = mov_y.a.text
	    mov_z = mov_y.findNext('div',{'class':'txt-block'})
	    mov_z_as = mov_z.findAll('a')
	    #prints all languages
	    langs = SubElement(movie,'Languages')
	    for mov_z_a in mov_z_as:
		SubElement(langs,'Language').text=mov_z_a.text
		#print mov_z_a.text

	    #duration of movie
	    mov_time = mpage.find('time',{'itemprop':'duration'}).text
#	    print mov_time	
	    SubElement(movie,'duration',name='duration').text=mov_time
#	    print mov_country	
	    SubElement(movie,'country',name='country').text=mov_country

            img_url = poster.a.img['src']
            rating = y.strong.text
            no_of_votes = str(y.strong['title']).split(' ')[3]
            #print count,'.', title, '\n\t', hover_text, '\n\t', movie_url, '\n\trating:', rating, '\n'

	    #to find cast list 
	    casts = SubElement( movie,'casts')
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
		td2text = td2text.split('(', 1)[0]
		cast = SubElement(casts,'character')
		SubElement( cast,'charactername',name='charactername').text = td2text

		SubElement( cast,'actorname',name='actorname').text = td1.text

	    #related keyword link
	    rel_link = mv_url_id+str('/keywords?ref_=tt_stry_kw')
            html3 = urlopen(rel_link)
            relpage = BeautifulSoup(html3.read())
	    relkeywords = SubElement(movie,'RelatedKeywords');
            rel_list = relpage.findAll('div',{'class':'sodatext'})
            for rel_item in rel_list:
		reldata = rel_item.a.text
		SubElement(relkeywords,'keyword').text=reldata
	    count+=1
	    if count>=5 :
		break
	    time.sleep( 5 )	    
print "writing output to xml"
output_file = open( 'top250data.xml', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( movies ) )
output_file.close()
print "End : %s" % time.ctime()
