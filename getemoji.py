import requests
import urllib
import cStringIO
import json
from PIL import Image
from io import BytesIO

url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='
query = 'fog creek software'
query_url = url + urllib.quote_plus(query)
print query_url
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'
r = requests.get(query_url, headers={'referer': 'https://google.com/', 'User-Agent': user_agent})
results = r.json()

for x in results['responseData']['results']:
    file = cStringIO.StringIO(urllib.urlopen(x['url']).read())
    try:
        img = Image.open(file)
        (i_width, i_height) = img.size
        img.thumbnail((128, 128), Image.ANTIALIAS)
        img_file = BytesIO()
        img.save(img_file, 'png')
        img_size = img_file.tell()
        img.show()
        print 'url: %s size: %s orig_width: %s orig_height: %s' % (x['url'], img_size, i_width, i_height)
    except:
        pass
    
