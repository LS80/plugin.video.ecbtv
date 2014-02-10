# coding=utf-8
##########################################################################
#
#  Copyright 2014 Lee Smith
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################

import os
import re
from urlparse import urlparse, urlunparse, urljoin
from datetime import date, timedelta
import time

from xbmcswift2 import Plugin
from bs4 import BeautifulSoup
import requests


HOST = "http://www.ecbtv.co.uk"
BASE_URL = HOST

VIDEO_ID_RE = re.compile("/video/i/(\d+)/") 

VIDEO_XML_FMT = (u"http://www.ecbtv.co.uk/page/sva/xmlHttpRequest/submit.xml"
                 "?type=18&sites=11617&clipId={}")

HEADERS = {'User-agent': "Mozilla/5.0"}


plugin = Plugin()

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, 'html5lib')

def get_videos(soup):
    for video in soup('div', 'videoListItem'):
        video_id = VIDEO_ID_RE.match(video.a['href']).group(1)
        img = video.find('img', 'videoListItemImage')
        title = img['title']
        thumb = img['src']
        date_str = video.find('span', 'videoListItemDate').string.strip()
        duration_str = video.find('span', 'videoLength').string.split()[0]
        
        video_date = date(*(time.strptime(date_str, "%d %b %Y")[0:3]))
        
        minutes, seconds = duration_str.split(':')
        duration = timedelta(minutes=int(minutes), seconds=int(seconds))
        
        item = {'label': title,
                'thumbnail': BASE_URL + thumb,
                'is_playable': True,
                'path': plugin.url_for('play_video', video_id=video_id),
                'info': {'title': title,
                         'date': video_date.strftime("%d.%m.%Y")
                         },
                'stream_info': {'video': {'duration': duration.seconds}}
                }

        yield item

@plugin.route('/')
def index():
    soup = get_soup(BASE_URL)
    return plugin.finish(get_videos(soup),
                         sort_methods=['playlist_order', 'date', 'duration', 'title'])
    
@plugin.route('/video/<video_id>')
def play_video(video_id):
    soup = get_soup(BASE_URL + "/video/i/{}".format(video_id))
    clip_id = soup.find('div', id='videoPlayer')['data-clipid']

    soup = get_soup(VIDEO_XML_FMT.format(clip_id))
    url = soup.find('file', formatid='133')['externalpath']

    return plugin.set_resolved_url(url)

if __name__ == '__main__':
    plugin.run()
