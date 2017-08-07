Gist Database
===============

Today's project will combine Github's API with Databases.

## TODO

**Write docs for:**

* Write about `import_gists_to_database`
 * Explain a little bit of requests

* Write about `search_gists`
 * Should return an iterator
 * This is the interface, although I'd leave it with `**kwargs`:

```python
def search_gists(
    db_connection, gist_id=None, public=None,
    created__gt=None, created__gte=None, created_lt=None, created_lte=None,
    updated__gt=None, updated__gte=None, updated_lt=None, updated_lte=None,
    comments=None):
    pass
```

These are the available gists in the Database:

Gist ID                          |      Created At      |     Updated At
---------------------------------|----------------------|---------------------
4232a4cdad00bd92a7a64cf3e2795820 | 2017-05-16T16:02:54Z | 2017-05-16T16:02:54Z
86beaced733b7dbf2d034e56edb8d37e | 2016-07-30T19:04:22Z | 2016-08-02T17:05:33Z
ef201fe313719305c4c7             | 2015-08-28T22:47:25Z | 2015-08-28T23:52:30Z
c669398c67386e9fb43e             | 2014-12-05T21:01:50Z | 2015-08-29T14:10:51Z
291bfcfe70d2f9582331             | 2014-11-27T06:03:45Z | 2015-08-29T14:10:24Z
1adb5bee99400ce615a5             | 2014-11-26T19:59:20Z | 2015-08-29T14:10:23Z
18bdf248a679155f1381             | 2014-05-03T20:26:08Z | 2017-02-17T18:06:12Z


**Strip down files**

* `search.py` should only contain the empty `search_gists` function and the import line. Everything else are our own utilities.
* `import_gists_to_database` should only contain the bare `import_gists_to_database` function.

**Add tests:**

* [DONE] Test for search wit gist_id `search_gists(gist_id=XXX)`.
* [DONE] Test with multiple AND conditions `search_gists(created_at__gt=d, comments=1, public=True))`
* [DONE] Test with multiple dates `search_gists(created_at__gt=d1, updated_at__lt=d2))`
* [DONE] Test `models.py`
