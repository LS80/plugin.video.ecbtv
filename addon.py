# coding=utf-8
##########################################################################
#
#  Copyright 2014-2017 Lee Smith
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

from kodiswift import Plugin

from resources.lib import api


plugin = Plugin()


def items(path):
    for video in api.videos(path):
        yield {
            'label': video.title,
            'thumbnail': video.thumbnail,
            'path': video.url,
            'info': {
                'title': video.title,
                'date': video.date.strftime('%d.%m.%Y')
            },
            'stream_info': {'video': {'duration': video.duration}},
            'is_playable': True
        }


def categories():
    for title, path in api.categories():
        yield {'label': title, 'path': plugin.url_for('show_videos', path=path)}


@plugin.route('/')
def index():
    return plugin.finish(categories())


@plugin.route('/category/<path>')
def show_videos(path):
    return plugin.finish(items(path), sort_methods=['playlist_order', 'date', 'title', 'duration'])


if __name__ == '__main__':
    plugin.run()
