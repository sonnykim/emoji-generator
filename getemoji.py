# Author: Sonny Kim @ sonnykim.com
# Repository: github.com/sonnykim/emoji-generator

import requests
import urllib
import cStringIO
import json
import traceback
import base64
import re
from PIL import Image
from io import BytesIO
from bottle import route, run, template, get, post, request

def getEmojis(query, start):
    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&rsz=4&q='
    query_url = url + urllib.quote_plus(query)
    query_url += '&start=' + start 
    print query_url
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'
    r = requests.get(query_url, headers={'referer': 'https://google.com/', 'User-Agent': user_agent})
    json_results = r.json()
    emojis = []
    for x in json_results['responseData']['results']:
        file = cStringIO.StringIO(urllib.urlopen(x['url']).read())
        # we can't do gifs it seems
        try:
            img = Image.open(file)
            (i_width, i_height) = img.size
            img.thumbnail((128, 128), Image.ANTIALIAS)
            img_file = BytesIO()
            img.save(img_file, 'png')
            img_size = img_file.tell()
            emojis.append(img_file)
            #img.show()
            print 'url: %s size: %s orig_width: %s orig_height: %s' % (x['url'], img_size, i_width, i_height)
        except Exception as e:
            print 'failed to touch up: %s' % x['url']
            print 'error: %s' % e
            pass
    
    return emojis
# end def getEmojis()

    
def getFormHtml():
    return '''
This is an emoji generator. It finds images and automatically resizes them to under 128px x 128px. Enjoy!
<p>
<form action="/egen" method="post">
<input name="query" type="text" />
<input value="generate" type="submit" />
</form>
</p>
'''
# end def getFormHtml()


@get('/egen')
def index():
    query = request.query.query
    start = request.query.start
    return generateHtml(query, start)
# end get('/egen')


@post('/egen')
def egen():
    query = request.forms.get('query')
    print query
    start = request.forms.get('start')
    print start
    return generateHtml(query, start)
# end post('/egen')

    
def generateHtml(query, start):
    html = getFormHtml()
    if query is None or query == '':
        return html
    if start is None or start == '':
        start = '0'
    original_query = query
    query = re.escape(query)    
    prefix = 'data:image/png;base64,'
    html += '<hr>'
    if query == '':
        return
    emojis = getEmojis(query, start) # emojis is a list of BytesIO image files
    html += '<table><tr>'
    for x in emojis:
        html += '<td><img src="'
        html += prefix
        html += base64.b64encode(x.getvalue())
        html += '"></td>'
    html += '</tr></table>'
    html += '<p><a href="'
    html = html + '/egen?query=' + original_query + '&start='
    html += str(int(start) + 4).strip(' ')
    html += '"'
    html += '>More...</a>'
    return html
# end def generateHtml

# start server command
run(host='localhost', port=8080, debug=True)
