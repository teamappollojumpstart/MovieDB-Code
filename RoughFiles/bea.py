import sys
import string
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
 
html = """http://www.imdb.com/title/tt0071562/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=09AA9CTBTM483FF9TCBA&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_3"""
mpage = BeautifulSoup(html.read())
td1 = mpage.find('span',{'class':'itemprop'}).text
print td1

