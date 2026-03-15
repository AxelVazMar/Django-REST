from rest_framework.throttling import UserRateThrottle

"""
A way to personalize the throttling classes, so we can use them in the settings.py 
file and set different rates for different scopes (burst and sustained).
"""

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustaninedRateThrottle(UserRateThrottle):
    scope = 'sustained'