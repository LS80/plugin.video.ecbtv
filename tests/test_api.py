from resources.lib import api


def test_county_videos():
    counties = list(api.counties())
    assert len(counties) == 18
    for county in counties:
        print county.name, county.id
        videos, num_pages = api.videos(county.reference)
        assert num_pages > 0
        assert list(videos)


def test_england_videos():
    videos, num_pages = api.videos(api.england().reference)
    assert num_pages > 0
    assert list(videos)


def test_search_results():
    videos, num_pages = api.search_results('test')
    assert num_pages > 0
    assert list(videos)


def test_player_categories():
    categories = [c.name for c in api.player_categories()]
    assert 'Test' in categories
    assert 'ODI' in categories
    assert 'T20I' in categories


def test_players():
    players = api.players(category='Test')
    assert players
    for player in players:
        print player.name
        videos, num_pages = api.videos(player.reference)
        assert num_pages > 0
        assert list(videos)


def test_england_tournaments():
    tournaments = api.england_tournaments()
    for tournament in tournaments:
        print tournament.name
        videos, num_pages = api.videos(tournament.reference)
        assert num_pages >= 0
        if num_pages > 0:
            assert list(videos)


def test_county_tournaments():
    tournaments = api.county_tournaments()
    for tournament in tournaments:
        print tournament.name
        videos, num_pages = api.videos(tournament.reference)
        assert num_pages >= 0
        if num_pages > 0:
            assert list(videos)
