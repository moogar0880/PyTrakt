Release History
^^^^^^^^^^^^^^^
2.1.0 (2015-??-??)
++++++++++++++++++

* Add Trakt PIN Authentication mechanism

2.0.2 (2015-04-18)
++++++++++++++++++

* Fix CLIENT_SECRET assignment Bug (#16)

2.0.1 (2015-03-15)
++++++++++++++++++

* Fixed TVEpisode Scrobbling Bug (#13)
* Fixed DEBUG logging messages to properly reflect HTTP Methods
* Added a 400 HTTP Response Code Exception type

2.0.0 (2015-03-04)
++++++++++++++++++

* 2.0 Version bump due to incompatible API changes relating to the location of the trakt api_key attribute
* Add additional debug logging for API responses
* Add tmdb_id to the `TVShow.ids` attribute
* Fixed `trakt.init` to instruct users on how to create a new OAuth application
* * Fixed `TVSeason.to_json` to return accurately scoped season information
* Updated documentation on APIv2's Authentication patterns

1.0.3 (2015-02-28)
++++++++++++++++++

* Fixed a bug with `First Aired Date` datetime parsing

1.0.2 (2015-02-17)
++++++++++++++++++

* Fixes Generator issue detailed in #7
* Fixes Python 2x Unicode bug

1.0.1 (2015-02-15)
++++++++++++++++++

* PyTrakt now utilizes Trakt's new API 2.0
* API Keys can now obtained via the `trakt.init` function
* Note: POSTS have been hit or miss, but get's all appear to be working

0.3.6 (2015-01-15)
++++++++++++++++++

* Bug fix for the failure to process JSON API responses

0.3.4 (2014-08-12)
++++++++++++++++++

* Merged @stampedeboss changes from PR #1
* Some small stylistic changes for consistency

0.3.3 (2014-07-04)
++++++++++++++++++

* trakt.tv.TVShow improvements/changes
* Misc bug fixes in trakt.tv
* Import enhancements in trakt.movies
* Added community module
* Fixed/updated documentation


0.3.0 (2014-06-19)
++++++++++++++++++

* Initial Release

