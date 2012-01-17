import httplib2
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer

#declare
base_url = "http://pastebin.com"
keywords = ['password','hack']

def clean(val):
    if type(val) is not str: val = str(val)
    val = re.sub(r'<.*?>', '', val) #remove tags
    return val.strip() #remove leading & trailing whitespace

def save_url(url):
	tracker = open("tracker.txt","a")
	tracker.write(str(url) + "\n")
	tracker.close()

def check_url(url):
	tracker = open("tracker.txt","r+")
	lines = tracker.readlines()
	for line in lines:
		m = re.search(url,line)
		if m:
			return False
	return True

http = httplib2.Http()
status, response = http.request('http://pastebin.com/archive')
product = SoupStrainer("td",{"class":"icon"})
soup = BeautifulSoup(response,parseOnlyThese=product)
for link in soup.findAll("a"):
	app = link["href"]
	if check_url(app):
		save_url(app)
		tmper = base_url + app
		status, response = http.request(tmper)
		feast = BeautifulSoup(response,parseOnlyThese=SoupStrainer("textarea")) #appears to only have one textarea
		m = re.search('|'.join(keywords),str(feast))
		if m:
			print tmper + " matched " +  m.group()
