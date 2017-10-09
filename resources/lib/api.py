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

'''
Module for extracting video links from the England and Wales Cricket Board website
'''

import json
import os
from urlparse import urljoin
from datetime import datetime
import time
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

HOST = 'http://www.ecb.co.uk'
BASE_URL = urljoin(HOST, 'tv/')

HLS_HOST = 'https://secure.brightcove.com/'
HLS_URL_FMT = urljoin(HLS_HOST, 'services/mobile/streaming/index/master.m3u8?videoId={}')

Video = namedtuple('Video', 'title url thumbnail date duration')


def _soup(path=''):
    '''Returns a BeautifulSoup tree for the specified path'''
    url = urljoin(BASE_URL, path)
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def _date(media_item):
    '''Returns a date object from the media item.
       datetime.strptime is avoided due to a Python issue in Kodi'''
    date_str = media_item.find('time', 'media__sub-meta').string
    return datetime(*(time.strptime(date_str, '%d %B %Y')[0:6])).date()


def categories():
    '''Generator for category names and links, excluding all that appear before Home'''
    start = False
    for submenu_link in _soup()('a', 'submenu__link'):
        title = submenu_link.string.strip()
        if start and title != 'All Categories':
            yield title, os.path.basename(submenu_link['href'])
        if title == 'Home':
            start = True


def videos(path):
    '''Generator for all videos from a particular page'''
    for media_item in _soup(path)('a', 'media__item'):
        video = json.loads(media_item['data-ui-args'])
        yield Video(
            media_item.find('span', 'media__title').string,
            HLS_URL_FMT.format(video['mediaId']),
            media_item.picture.img['data-highres-img'],
            _date(media_item),
            int(video['duration'].replace(',', ''))
        )


def _main():
    '''Test function to print all categories and videos'''
    for title, path in categories():
        print title, path
        for video in videos(path):
            print '\t', video


if __name__ == '__main__':
    _main()
