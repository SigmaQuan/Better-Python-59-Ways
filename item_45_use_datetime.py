# Item 45: Use datetime instead of time for local clocks


# Coordinate Universal Time (CUT) is the standard, time-zone-independent
# representation of time. UTC works great for computers that represent time as
# seconds since the UNIX epoch. But UTC isn't ideal for humans. Humans
# reference time relative to where they're currently located. People say
# "noon" or "8 am" instead of "UTC 15:00 minus 7 hours." If your program
# handles times, you'll probably fin yourself converting time between UTC and
# local clocks to make it easier for humans to understand.

# Python provides two ways of accomplishing time zone conversation. The old
# way, using the time built-in module, is disastrously error prone. The new
# way, using the datetime built-in module, works great with some help from
# the community-built package named pytz.

# You should be acquainted with both time and datetime to thoroughly
# understand why datetime is the best choice and time should be avoided.


# The time Module

# The localtime function from the time built-in module lets you convert a UNIX
# timestamp (seconds since the UNIX epoch in UTC) to a local time that matches
# the host computer's time zone (Pacific Daylight Time, in my case).

from time import localtime, strftime

now = 1407694710
local_tuple = localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = strftime(time_format, local_tuple)
print(time_str)
# 2014-08-11 02:18:30

# You'll often need to go the other way as well, starting with user input in
# local time and converting it to UTC time. You can do this by using the
# strptime function to parse the time string, then call mktime to convert
# local time to a UNIX timestamp.

from time import mktime, strptime

time_tuple = strptime(time_str, time_format)
utc_now = mktime(time_tuple)
print(utc_now)
# 1407694710.0

# How do you convert local time in one time zone to local time in another? For
# example, say you are taking a flight between San Francisco and New York, and
# want to know what time it will be in San Francisco once you've arrived in
# New York.

# Directly manipulating the return values from the time, localtime, and
# strptime functions to do time zone conversations is a bad idea. Time zones
# change all the time due to local laws. It's too complicated to manage
# yourself, especially if you want to handle every global city for flight
# departure and arrival.

# Many operating systems have configuration files that keep up with the time
# zone changes automatically. Python lets you use these time zones through the
# time module. For example, here I parse the departure time from the San
# Francisco time zone of Pacific Daylight Time:

parse_format = '%Y-%m-%d %H:%M:%S'
depart_sfo = '2014-05-01 15:45:16'
# parse_format = '%Y-%m-%d %H:%M:%S %Z'
# depart_sfo = '2014-05-01 15:45:16 PDT'
time_tuple = strptime(depart_sfo, parse_format)
time_str = strftime(time_format, time_tuple)
print(time_str)
# 2014-05-01 15:45:16
# ValueError: time data '2014-05-01 15:45:16 PDT' does not match format '%Y-%m-%d %H:%M:%S %Z'

# After seeing that PDT works with the strptime function, you might also
# assume that time zones known to my computer will also work. Unfortunately,
# this isn't the case. Instead, strptime raises an exception when it sees
# Eastern Daylight Time (the time zone for New York).

arrival_nyc = '2014-05-01 23:33:24 EDT'
# time_tuple = strptime(arrival_nyc, time_format)
# ValueError: unconverted data remains:  EDT

# The problem here is the platform-dependent nature of the time module. Its
# actual behavior is determined by how the underlying C functions work with
# the host operating system. This makes the funcionality of the time module
# unreliable in Python. The time module fails to consistently work properly
# for multiple local times. Thus, you should avoid the time module for this
# purpose. If you must use time, only use it to convert between UTC and the
# host computer's local time. For all other types of conversations, use the
# datetime module.


# The datetime Module

# The second option for representing times in Python is the datetime class
# from the datetime built-in module. Like the time module, datetime can be
# used to convert from the current time in UTC to local time.

# Here, I take the present time in UTC and convert it to my computer's local
# time (Pacific Dayligh Time):

from datetime import datetime, timezone

now = datetime(2014, 8, 10, 18, 18, 30)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)
# 2014-08-11 02:18:30+08:00

# The datetime module can also easily convert a local time back to a UNIX
# timestamp in UTC.

time_str = '2014-08-10 11:18:30'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = mktime(time_tuple)
print(utc_now)
# 1407640710.0

# Unlike the time module, the datetime module has facilities for reliably
# converting from one local time to another local time. However, datetime
# only provides the machinery for time zone operations with its tzinfo class
# and related methods. What's missing are the time zone definitions basides
# UTC.

# Luckily, the Python community has addressed this gap with the pytz module
# that's available for download from the Python Package Index
# (https://pypi.python.org/pypi/pytz/). pytz contains a full database of every
# time zone definition you might need.

# To use pytz effectively, you should always convert local times to UTC first.
# Perform any datetime operations you need on the UTC values (such as
# offsetting). Then, convert to local times as a final step.

# For example, here I convert an NYC flight arrival time to a UTC datetime.
# Although some of these calls seem redundant, all of them are necessary when
# using pytz.

import pytz

arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt)
# 2014-05-02 03:33:24+00:00

# Once I have a UTC datetime, I can convert it to San Francisco local time.

pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt)
# 2014-05-01 20:33:24-07:00

# Just as easily, I can convert it to the local time in Nepal.

nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(nepal_dt)
# 2014-05-02 09:18:24+05:45

# With datetime and pytz, these conversations are consistent across all
# environments regardless of what operating system the host computer is
# running.


# Things to remember

# 1. Avoid using the time module for translating between different time zones.
# 2. Use the datetime built-in module along with the pytz module to reliably
#    convert between times in different time zones.
# 3. Always represent time in UTC and do conversations to local time as the
#    final step before presentation.
