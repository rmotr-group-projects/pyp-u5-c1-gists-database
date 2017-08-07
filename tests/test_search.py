from datetime import datetime
from gists_database.search import search_gists, build_query

from .fixtures import populated_gists_database as db
#
# q1 = "SELECT * FROM gists WHERE datetime(created_at) > datetime(:created_at__gt)"
# q2 = "SELECT * FROM gists WHERE datetime(created_at) > datetime(:created_at__gt) AND public = :public"
#
# def test_queries():
#     # assert build_query(created_at__gt='2017-05-10')[0] == q1
#     assert build_query(created_at__gt='2017-05-10', public=True)[0] == q2

def test_search_without_parameters_returns_all_gists(db):
    gists_iterator = search_gists(db)
    gists = [g for g in iter(gists_iterator)]
    assert len(gists) == 7


def test_search_with_created_date_gt(db):
    d = datetime(2017, 5, 10)
    gists_iterator = search_gists(db, created_at__gt=d)
    gists = [g for g in iter(gists_iterator)]
    assert len(gists) == 1

    gist = gists[0]
    assert gist.github_id == '4232a4cdad00bd92a7a64cf3e2795820'


def test_search_with_created_date_gte(db):
    d = datetime(2017, 5, 10, 16, 2, 54)
    gists_iterator = search_gists(db, created_at__gte=d)
    gists = [g for g in iter(gists_iterator)]
    assert len(gists) == 1

    gist = gists[0]
    assert gist.github_id == '4232a4cdad00bd92a7a64cf3e2795820'


def test_search_with_created_date_lt(db):
    d = datetime(2014, 11, 28)
    gists_iterator = search_gists(db, created_at__lt=d)
    gists = [g for g in iter(gists_iterator)]
    assert len(gists) == 3

    gist = gists[0]
    assert gist.github_id == '291bfcfe70d2f9582331'

    gist = gists[1]
    assert gist.github_id == '1adb5bee99400ce615a5'

    gist = gists[2]
    assert gist.github_id == '18bdf248a679155f1381'


def test_search_with_created_date_lte(db):
    d = datetime(2014, 5, 3, 20, 26, 8)
    gists_iterator = search_gists(db, created_at__lte=d)
    gists = [g for g in iter(gists_iterator)]
    assert len(gists) == 1

    gist = gists[0]
    assert gist.github_id == '18bdf248a679155f1381'
