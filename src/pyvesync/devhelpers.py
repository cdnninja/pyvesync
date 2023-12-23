"""Device helper methods.

Include features Enums for devices

- FANFEATURES
- BULBFEATURES
- SWITCHFEATURES
- FANMODES
"""
import time
import logging
import json
from typing import NamedTuple, Optional, Union, Any
from enum import Enum
import colorsys
from attrs import define, field
from pyvesync.vsconfig import VeSyncConfig

logger = logging.getLogger(__name__)

NUMERIC_T = Optional[Union[int, float, str]]


class FANFEATURES(Enum):
    """Fan features Enum."""

    NIGHTLIGHT = "nightlight"
    WARM_MIST = "warm_mist"
    AIR_QUALITY = "air_quality"


class BULBFEATURES(Enum):
    """Bulb features Enum."""

    DIMMABLE = "dimmable"
    COLOR_TEMP = "color_temp"
    RGB_SHIFT = "rgb_shift"


class SWITCHFEATURES(Enum):
    """Switch features Enum."""

    DIMMABLE = "dimmable"


class FANMODES(Enum):
    """Fan modes Enum."""

    AUTO = "auto"
    MANUAL = "manual"
    SLEEP = "sleep"
    HUMIDITY = "humidity"
    OFF = "off"
    PET = "pet"


def between_values(value: NUMERIC_T,
                   min_val: NUMERIC_T,
                   max_val: NUMERIC_T) -> Union[int, float]:
    """Set value between min and max and return min or max if below or above.

    Will gracefully try to convert numeric strings if possible.
    """
    value_num = numberfy(value)
    min_num = numberfy(min_val)
    max_num = numberfy(max_val)
    return max(min(max_num, value_num), min_num)


def numberfy(val: NUMERIC_T) -> Union[int, float]:
    """Convert value to numeric type.

    Attempts to detect float or int in string to maintain type.
    """
    if val is None:
        return 0
    try:
        if isinstance(val, str):
            if "." in val:
                return float(val)
            return int(val)
    except ValueError:
        logging.debug("Unable to convert %s to numeric type", val)
        return 0
    return val


def device_debug_helper(config: dict, manager: Any):
    """Print device info for unknown devices."""
    config_entry = VeSyncConfig.get_device_specs(manager, config['configModule'])
    if config_entry is None:
        logger.debug("No device configuration found from API")
    else:
        logger.debug("Device configuration found from API - ")
        logger.debug(json.dumps(config_entry, indent=4))
    logger.debug("Device list config - ")
    logger.debug(json.dumps(config, indent=4))
    logger.debug("Device linkage properties - %s", json.dumps(
        get_device_linkage(config['configModule'], manager), indent=4))


def get_device_linkage(config_module: str, manager: Any) -> dict:
    """Get device linkage from config module."""
    config_entry = VeSyncConfig.get_linkage(manager, config_module)
    if config_entry is None:
        return {}
    return config_entry.get('linkage', {})


class DeviceConfig:
    """Class to parse device features & configuration from dictionaries."""

    @staticmethod
    def model_dict(feature_dict: dict) -> dict:
        """Return a dictionary with config_module keys and class names as values."""
        model_modules = {}
        for dev_dict in feature_dict.values():
            for model in dev_dict['config_modules']:
                model_modules[model] = dev_dict['module']
        return model_modules

    @classmethod
    def get_features(cls, config_module: str, feature_dict: dict) -> list:
        """Get list of features based on config module."""
        return cls.device_config_by_key('features', config_module, feature_dict)

    @classmethod
    def get_modes(cls, config_module: str, feature_dict: dict) -> list:
        """Get list of modes based on config module."""
        return cls.device_config_by_key('modes', config_module, feature_dict)

    @staticmethod
    def device_config_by_key(key, config_module, feature_dict) -> list:
        """Get key from device dict based on config module."""
        for dev_dict in feature_dict.values():
            if config_module in dev_dict['config_modules']:
                return dev_dict.get(key, [])
        return []

    @staticmethod
    def get_config_dict(config_module: str, feature_dict: dict) -> dict:
        """Get config dict based on config module."""
        for dev_dict in feature_dict.values():
            if config_module in dev_dict['config_modules']:
                return dev_dict
        return {}


class Converters:
    """Unit converters."""

    @staticmethod
    def percent_to_kelvin(percent: int) -> int:
        """Convert percent to kelvin."""
        return int((percent / 100) * 255)


@define
class Timer:
    """Dataclass for timers.

    Parameters
    ----------
    timer_duration : int
        Length of timer in seconds
    action : str
        Action to perform when timer is done
    id: int
        ID of timer, defaults to 1

    Attributes
    ----------
    update_time : int
        Timestamp of last update

    Properties
    ----------
    status : str
        Status of timer, one of 'active', 'paused', 'done'
    time_remaining : int
        Time remaining on timer in seconds
    running : bool
        True if timer is running
    paused : bool
        True if timer is paused
    done : bool
        True if timer is done

    Methods
    -------
    start()
        Restarts paused timer
    end()
        Ends timer
    pause()
        Pauses timer
    update(time_remaining: Optional[int] = None, status: Optional[str] = None)
        Updates timer with new time remaining and/or status
    """

    timer_duration: int
    action: str
    id: int = 1
    remaining: Optional[int] = field(default=None)
    _status: str = 'active'
    _remain: int = 0
    update_time: Optional[int] = int(time.time())

    def __attrs_post_init__(self) -> None:
        """Set remaining time if provided."""
        if self.remaining is not None:
            self._remain = self.remaining
        else:
            self._remain = self.timer_duration

    @property
    def status(self) -> str:
        """Return status of timer."""
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        """Set status of timer."""
        if status not in ['active', 'paused', 'done']:
            raise ValueError(f'Invalid status {status}')
        self._internal_update()
        if status == 'done' or self._status == 'done':
            return self.end()
        if self.status == 'paused' and status == 'active':
            self.update_time = int(time.time())
        if self.status == 'active' and status == 'paused':
            self.update_time = None
        self._status = status

    @property
    def _seconds_since_check(self) -> int:
        """Return seconds since last update."""
        if self.update_time is None:
            return 0
        return int(time.time()) - self.update_time

    @property
    def time_remaining(self) -> int:
        """Return remaining seconds."""
        self._internal_update()
        return self._remain

    @time_remaining.setter
    def time_remaining(self, remaining: int) -> None:
        """Set time remaining in seconds."""
        if remaining <= 0:
            return self.end()
        self._remain = remaining
        if self._status == 'done':
            self.status = 'paused'
        self.update_time = None
        self._internal_update()

    def _internal_update(self) -> None:
        """Use time remaining update status."""
        if self._status == 'paused':
            self.update_time = None
            return
        if self._status == 'done' or (self._seconds_since_check > self._remain
                                      and self._status == 'active'):
            self._status = 'done'
            self.update_time = None
            self._remain = 0
        if self._status == 'active':
            self._remain = self._remain - self._seconds_since_check
            self.update_time = int(time.time())

    @property
    def running(self) -> bool:
        """Check if timer is active."""
        if self.time_remaining > 0 and self.status == 'active':
            return True
        return False

    @property
    def paused(self) -> bool:
        """Check if timer is paused."""
        return bool(self.status == 'paused')

    @property
    def done(self) -> bool:
        """Check if timer is complete."""
        return bool(self.time_remaining <= 0 or self._status == 'done')

    def end(self) -> None:
        """Change status of timer to done."""
        self._status = 'done'
        self._remain = 0
        self.update_time = None

    def start(self) -> None:
        """Restart paused timer."""
        if self._status != 'paused':
            return
        self.update_time = int(time.time())
        self.status = 'active'

    def update(self, *, time_remaining: Optional[int] = None,
               status: Optional[str] = None) -> None:
        """Update timer.

        Accepts only KW args

        Parameters
        ----------
        time_remaining : int
            Time remaining on timer in seconds
        status : str
            Status of timer, can be active, paused, or done

        Returns
        -------
        None
        """
        if time_remaining is not None:
            self.time_remaining = time_remaining
        if status is not None:
            self.status = status

    def pause(self) -> None:
        """Pause timer. NOTE - this does not stop the timer via API only locally."""
        self._internal_update()
        if self.status == 'done':
            return
        self.status = 'paused'
        self.update_time = None


class HSV(NamedTuple):
    """HSV color space."""

    hue: float
    saturation: float
    value: float


class RGB(NamedTuple):
    """RGB color space."""

    red: float
    green: float
    blue: float


@define
class Color:
    """Dataclass for color values.

    For HSV, pass hue as value in degrees 0-360, saturation and value as values
    between 0 and 100.

    For RGB, pass red, green and blue as values between 0 and 255.

    To instantiate pass kw arguments for colors hue, saturation and value or
    red, green and blue.

    Instance attributes are:
    hsv (nameduple) : hue (0-360), saturation (0-100), value (0-100)

    rgb (namedtuple) : red (0-255), green (0-255), blue

    """

    hsv: HSV = field(default=None)
    rgb: RGB = field(default=None)

    def __attrs_post_init__(self):
        """Check HSV or RGB Values and create named tuples."""
        if self.rgb is None and self.hsv is None:
            raise ValueError('No color values provided')
        if self.rgb is None:
            self.rgb = self.hsv_to_rgb(self.hsv.hue, self.hsv.saturation, self.hsv.value)
        if self.hsv is None:
            self.hsv = self.rgb_to_hsv(self.rgb.red, self.rgb.green, self.rgb.blue)

    @classmethod
    def from_hsv(cls, hue: NUMERIC_T, saturation: NUMERIC_T,
                 value: NUMERIC_T) -> 'Color':
        """Create Color object from HSV values."""
        return cls(hsv=HSV(between_values(hue, 0, 360),
                           between_values(saturation, 0, 100),
                           between_values(value, 0, 100)))

    @classmethod
    def from_rgb(cls, red: NUMERIC_T, green: NUMERIC_T,
                 blue: NUMERIC_T) -> 'Color':
        """Create Color object from RGB values."""
        return cls(rgb=RGB(between_values(red, 0, 255),
                           between_values(green, 0, 255),
                           between_values(blue, 0, 255)))

    @staticmethod
    def hsv_to_rgb(hue, saturation, value) -> RGB:
        """Convert HSV to RGB."""
        return RGB(
            *tuple(round(i * 255, 0) for i in colorsys.hsv_to_rgb(
                hue / 360,
                saturation / 100,
                value / 100
            ))
        )

    @staticmethod
    def rgb_to_hsv(red, green, blue) -> HSV:
        """Convert RGB to HSV."""
        hsv_tuple = colorsys.rgb_to_hsv(
                red / 255,
                green / 255,
                blue / 255
            )
        hsv_factors = [360, 100, 100]

        return HSV(
            float(round(hsv_tuple[0] * hsv_factors[0], 2)),
            float(round(hsv_tuple[1] * hsv_factors[1], 2)),
            float(round(hsv_tuple[2] * hsv_factors[2], 0)),
        )
