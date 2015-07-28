import requests
import urllib
import cStringIO
import json
from PIL import Image
from pyquery import PyQuery as pq

#url = 'https://www.google.com/search?hl=en&site=imghp&tbm=isch&source=hp&q='
url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='
query = 'full house poker'
query_url = url + urllib.quote_plus(query)
print query_url
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'
r = requests.get(query_url, headers={'referer': 'https://google.com/', 'User-Agent': user_agent})
results = r.json()

for x in results['responseData']['results']:
    file = cStringIO.StringIO(urllib.urlopen(x['url']).read())
    img = Image.open(file)
    img.show()
    print x['url']
    