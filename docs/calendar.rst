Calendars
---------

.. automodule:: trakt.calendar
    :members:
    :undoc-members:


Example Usage
^^^^^^^^^^^^^
All four Calendar types :class:`PremiereCalendar`, :class:`ShowCalendar`, and
:class:`SeasonCalendar` and :class:`MovieCalendar` behave similarly, the only
fundamental difference is in the data they represent. They all accept optional
date and days parameters which specify the start date and length of the Calendar.
Below are some examples of these calendars in action.
::

    >>> from trakt.calendar import PremiereCalendar
    >>> p_calendar = PremiereCalendar(days=1)
    >>> len(p_calendar)
    21
    >>> p_calendar
    [<TVEpisode>: Return to Amish S1E1 Pilot,
     <TVEpisode>: The Next Food Network Star S10E10 Hollywood Calling,
     <TVEpisode>: Sladkaya Zhizn S1E1 Серия 1,
     <TVEpisode>: Ladies of London S1E1 ,
     <TVEpisode>: Longmire S3E3 The White Warrior,
     <TVEpisode>: Famous in 12 S1E1 Pilot,
     <TVEpisode>: Top Gear (US) S5E5 American Muscle,
     <TVEpisode>: Jennifer Falls S1E1 Pilot,
     <TVEpisode>: Orange Is the New Black S2E2 TBA,
     ...

You can also iterate over the Calendar itself
::

    >>> for episode in p_calendar:
    ...     print(episode)
    <TVEpisode>: Return to Amish S1E1 Pilot
    <TVEpisode>: The Next Food Network Star S10E10 Hollywood Calling
    <TVEpisode>: Sladkaya Zhizn S1E1 Серия 1
    <TVEpisode>: Ladies of London S1E1
    <TVEpisode>: Longmire S3E3 The White Warrior
    <TVEpisode>: Famous in 12 S1E1 Pilot
    <TVEpisode>: Top Gear (US) S5E5 American Muscle
    <TVEpisode>: Jennifer Falls S1E1 Pilot
    <TVEpisode>: Orange Is the New Black S2E2 TBA
    ...

