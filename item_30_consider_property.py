# Item 30: Consider @property instead of refactoring attributes
from datetime import timedelta
import datetime


# The built-in @property decorator makes it easy for simple accesses of an
# instance's attributes to act smarter (see Item 29: "Use plain attributes
# instead of get and set methods"). One advanced but common use of @property
# is transitioning what was once a simple numerical attribute into an
# on-the-fly calculation. This is extremely helpful because it lets you
# migrate all existing usage of a class to have new behaviors without
# rewriting any of the call sites. It also provides an important stopgap for
# improving your interfaces over time.

# For example, say you want to implement a leaky bucket quota using plain
# Python objects. Here, the Bucket class represents how much quota remains
# and the duration for which the quota will be available:


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota


# The leaky bucket algorithm works by ensuring that, whenever the bucket is
# filled, the amount of quota does not carry over from one period to the next.


def fill(bucket, amount):
    now = datetime.datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


# Each time a quota consumer wants to do something, it first must ensure that
# it can deduct the amount of quota it needs to use.


def deduct(bucket, amount):
    now = datetime.datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


# To use this class, first I fill the bucket.

bucket = Bucket(60)
fill(bucket, 100)
print(bucket)
# Bucket(quota=100)

# Then, I deduct the quota that I need.


if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)
# Had 99 quota
# Bucket(quota=1)

# Eventually, I'm prevented from making progress because I try to deduct more
# quota than is available. In this case, the bucket's quota level remains
# unchanged.


if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)
# Not enough for 3 quota
# Bucket(quota=1)


# The problem with this implementation is that I never know that quota level
# the bucket started with. The quota is deducted over the course of the period
# until it reaches zero. At that point, deduct will always return False. When
# that happens, it would be useful to know whether callers to deduct are being
# blocked because the Bucket ran out of quota or because the Bucket never had
# quota in the first place.

# To fix this, I can change the class to keep track of the max_quota issued in
# the period and the quota_consumed in the period.


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                (self.max_quota, self.quota_consumed))

# I use a @property method to compute the current level of quota on-the-fly
# using these new attributes.
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

# When the quota attribute is assigned, I take special action matching the
# current interface of the class used by fill and decuct.
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            '''quota being reset for a new period'''
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            '''quota being filled for the new period'''
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            '''quota being consumed during the period'''
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


# Rerunning the demo code from above produces the same results.


bucket = Bucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print('Still', bucket)
# Initial Bucket(max_quota=0, quota_consumed=0)
# Filled Bucket(max_quota=100, quota_consumed=0)
# Had 99 quota
# Now Bucket(max_quota=100, quota_consumed=99)
# Not enough for 3 quota
# Still Bucket(max_quota=100, quota_consumed=99)

# The best part is that the code using Bucket.quota doesn't have to change or
# know that the class has changed. New usage of Bucket can do the right thing
# and access max_quota and quota_consumed directly.

# I especially like @property because it lets you make incremental progress
# toward a better data model over time. Reading the Bucket example above, you
# may have though to yourself, "fill and deduct should have been implemented
# as instance methods in the first place." Although you're probably right (see
# Item 22: "Prefer helper classes over bookkeeping with dictionaries and
# tuples"), in practice there are many situations in which objects start with
# poorly defined interfaces or act as dumb data containers. This happens when
# code grows over time, scope increases, multiple authors contribute without
# any one considering long-term hygiene, etc.

# @property is a tool to help you address problems you'll come across in real-
# world code. Don't overuse it. When you find yourself repeatedly extending
# @property methods, it's probably time to refactor your class instead of
# further paving over your code's poor design.


# Things to remember

# 1. Use @property to give existing instance attributes new functionality.
# 2. Make incremental progress toward better data models by using @property.
# 3. Consider refactoring a class and all call sites when you find yourself
#     using @property too heavily.
