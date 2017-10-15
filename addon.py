###############################################################################
#
# MIT License
#
# Copyright (c) 2017 Lee Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###############################################################################

from kodiswift import Plugin

from resources.lib import api


plugin = Plugin()


def items(path):
    for video in api.videos(path):
        yield {
            'thumbnail': video.thumbnail,
            'path': video.url,
            'info': {
                'title': video.title,
                'date': video.date.strftime('%d.%m.%Y'),
                'duration': video.duration
            },
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
