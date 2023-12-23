"""Constats for the PyVeSync package."""


API_BASE_URL = 'https://smartapi.vesync.com'
API_RATE_LIMIT = 30
# If device is out of reach, the cloud api sends a timeout response after 7 seconds,
# using 8 here so there is time enough to catch that message
API_TIMEOUT = 8
USER_AGENT = ("VeSync/3.2.39 (com.etekcity.vesyncPlatform;"
              " build:5; iOS 15.5.0) Alamofire/5.2.1")

DEFAULT_TZ = 'America/New_York'
DEFAULT_REGION = 'US'

APP_VERSION = '2.8.6'
PHONE_BRAND = 'SM N9005'
PHONE_OS = 'Android'
MOBILE_ID = '1234567890123456'
USER_TYPE = '1'
BYPASS_APP_V = "VeSync 3.0.51"
CLIENT_TYPE = 'vesyncApp'
CLIENT_INFO = 'iOS 15.5.0'
CLIENT_VERSION = "5.0.20"
