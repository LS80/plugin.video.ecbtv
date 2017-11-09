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

import functools


PAGE_SIZE = 9

plugin = Plugin()


def categories():
    yield {'label': '[B]{}[/B]'.format(plugin.get_string(30002)),
           'path': plugin.url_for('show_all_videos_first_page')}
    yield {'label': '[B]{}[/B]'.format(plugin.get_string(30001)),
           'path': plugin.url_for('search')}
    yield {'label': 'England',
           'path': plugin.url_for('show_videos_first_page', reference=api.england().reference)}
    yield {'label': 'Counties',
           'path': plugin.url_for('show_counties')}
    yield {'label': 'Players',
           'path': plugin.url_for('show_player_categories')}


def subcategories(generator, route):
    for category in generator():
        yield {'label': category,
               'path': plugin.url_for(route, category=category)}


def entities(generator):
    for entity in generator():
        yield {'label': entity.name,
               'thumbnail': entity.thumbnail,
               'path': plugin.url_for('show_videos_first_page', reference=entity.reference)}


def items(func, route, page, **kwargs):
    videos, npages = func(page=page, page_size=PAGE_SIZE, **kwargs)

    if page > 1:
        yield {
            'label': u"<< {} ({})".format(plugin.get_string(30003), page - 1),
            'path': plugin.url_for(route, page=page - 1, **kwargs)
        }
    if page < npages:
        yield {
            'label': u"{} ({}) >>".format(plugin.get_string(30004), page + 1),
            'path': plugin.url_for(route, page=page + 1, **kwargs)
        }

    for video in videos:
        yield {
            'label': video.title,
            'thumbnail': video.thumbnail,
            'path': video.url,
            'info': {
                'date': video.date.strftime('%d.%m.%Y'),
                'duration': video.duration
            },
            'is_playable': True
        }


def show(func, route, page, **kwargs):
    return plugin.finish(
        items(func, route, page, **kwargs),
        sort_methods=['playlist_order', 'date', 'title', 'duration'],
        update_listing=page > 1
    )


@plugin.route('/')
def index():
    return plugin.finish(list(categories()))


@plugin.route('/counties')
def show_counties():
    return plugin.finish(entities(api.counties), sort_methods=['label'])


@plugin.route('/players')
def show_player_categories():
    return plugin.finish(
        subcategories(api.player_categories, 'show_players'),
        sort_methods=['label']
    )


@plugin.route('/players/<category>')
def show_players(category):
    return plugin.finish(
        entities(functools.partial(api.players, category)),
        sort_methods=['label']
    )


@plugin.route('/videos/all', name='show_all_videos_first_page')
@plugin.route('/videos/all/<page>')
def show_all_videos(page='1'):
    return show(api.videos, 'show_all_videos', int(page))


@plugin.route('/videos/<reference>', name='show_videos_first_page')
@plugin.route('/videos/<reference>/<page>')
def show_videos(reference, page='1'):
    return show(api.videos, 'show_videos', int(page), reference=reference)


@plugin.route('/search')
def search():
    term = plugin.keyboard(heading=plugin.get_string(30001))
    if term:
        url = plugin.url_for('show_search_results_first_page', term=term)
        plugin.redirect(url)


@plugin.route('/search/<term>', name='show_search_results_first_page')
@plugin.route('/search/<term>/<page>')
def show_search_results(term, page='1'):
    return show(api.search_results, 'show_search_results', int(page), term=term)


if __name__ == '__main__':
    plugin.run()
