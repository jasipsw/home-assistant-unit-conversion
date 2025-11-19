"""Unit Conversion Filters for Home Assistant."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import TemplateEnvironment

_LOGGER = logging.getLogger(__name__)

DOMAIN = "unit_conversions"


# Power conversion filters
def w(value, from_unit="W"):
    """Convert power to Watts."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "")
        
        if from_unit in ["W", "WATT", "WATTS"]:
            return value
        elif from_unit in ["KW", "KILOWATT", "KILOWATTS"]:
            return value * 1000
        else:
            _LOGGER.warning(f"Unknown power unit '{from_unit}', assuming Watts")
            return value
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for watts conversion: {value}")
        return None


def kw(value, from_unit="W"):
    """Convert power to Kilowatts."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "")
        
        if from_unit in ["KW", "KILOWATT", "KILOWATTS"]:
            return value
        elif from_unit in ["W", "WATT", "WATTS"]:
            return value / 1000
        else:
            _LOGGER.warning(f"Unknown power unit '{from_unit}', assuming Watts")
            return value / 1000
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for kilowatts conversion: {value}")
        return None


# Energy conversion filters
def wh(value, from_unit="Wh"):
    """Convert energy to Watt-hours."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "").replace("-", "")
        
        # Conversion factors to Wh
        conversions = {
            "WH": 1,
            "WATTHOUR": 1,
            "WATTHOURS": 1,
            "KWH": 1000,
            "KILOWATTHOUR": 1000,
            "KILOWATTHOURS": 1000,
            "J": 1 / 3600,
            "JOULE": 1 / 3600,
            "JOULES": 1 / 3600,
            "KJ": 1000 / 3600,
            "KILOJOULE": 1000 / 3600,
            "KILOJOULES": 1000 / 3600,
            "MJ": 1000000 / 3600,
            "MEGAJOULE": 1000000 / 3600,
            "MEGAJOULES": 1000000 / 3600,
            "GJ": 1000000000 / 3600,
            "GIGAJOULE": 1000000000 / 3600,
            "GIGAJOULES": 1000000000 / 3600,
            "BTU": 1 / 3.41214,
            "BTUS": 1 / 3.41214,
            "BRITISHTHERMALUNIT": 1 / 3.41214,
            "BRITISHTHERMALUNITS": 1 / 3.41214,
        }
        
        factor = conversions.get(from_unit)
        if factor is None:
            _LOGGER.warning(f"Unknown energy unit '{from_unit}', assuming Wh")
            return value
        
        return value * factor
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for watt-hours conversion: {value}")
        return None


def kwh(value, from_unit="kWh"):
    """Convert energy to Kilowatt-hours."""
    try:
        wh_value = wh(value, from_unit)
        if wh_value is None:
            return None
        return wh_value / 1000
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for kilowatt-hours conversion: {value}")
        return None


def j(value, from_unit="J"):
    """Convert energy to Joules."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "").replace("-", "")
        
        # Conversion factors to J
        conversions = {
            "J": 1,
            "JOULE": 1,
            "JOULES": 1,
            "KJ": 1000,
            "KILOJOULE": 1000,
            "KILOJOULES": 1000,
            "MJ": 1000000,
            "MEGAJOULE": 1000000,
            "MEGAJOULES": 1000000,
            "GJ": 1000000000,
            "GIGAJOULE": 1000000000,
            "GIGAJOULES": 1000000000,
            "WH": 3600,
            "WATTHOUR": 3600,
            "WATTHOURS": 3600,
            "KWH": 3600000,
            "KILOWATTHOUR": 3600000,
            "KILOWATTHOURS": 3600000,
            "BTU": 1055.06,
            "BTUS": 1055.06,
            "BRITISHTHERMALUNIT": 1055.06,
            "BRITISHTHERMALUNITS": 1055.06,
        }
        
        factor = conversions.get(from_unit)
        if factor is None:
            _LOGGER.warning(f"Unknown energy unit '{from_unit}', assuming J")
            return value
        
        return value * factor
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for joules conversion: {value}")
        return None


def btu(value, from_unit="BTU"):
    """Convert energy to BTU."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "").replace("-", "")
        
        # Conversion factors to BTU
        conversions = {
            "BTU": 1,
            "BTUS": 1,
            "BRITISHTHERMALUNIT": 1,
            "BRITISHTHERMALUNITS": 1,
            "WH": 3.41214,
            "WATTHOUR": 3.41214,
            "WATTHOURS": 3.41214,
            "KWH": 3412.14,
            "KILOWATTHOUR": 3412.14,
            "KILOWATTHOURS": 3412.14,
            "J": 1 / 1055.06,
            "JOULE": 1 / 1055.06,
            "JOULES": 1 / 1055.06,
            "KJ": 1000 / 1055.06,
            "KILOJOULE": 1000 / 1055.06,
            "KILOJOULES": 1000 / 1055.06,
            "MJ": 1000000 / 1055.06,
            "MEGAJOULE": 1000000 / 1055.06,
            "MEGAJOULES": 1000000 / 1055.06,
            "GJ": 1000000000 / 1055.06,
            "GIGAJOULE": 1000000000 / 1055.06,
            "GIGAJOULES": 1000000000 / 1055.06,
        }
        
        factor = conversions.get(from_unit)
        if factor is None:
            _LOGGER.warning(f"Unknown energy unit '{from_unit}', assuming BTU")
            return value
        
        return value * factor
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for BTU conversion: {value}")
        return None


# Flow conversion filters
def lpm(value, from_unit="L/MIN"):
    """Convert flow rate to Liters per Minute."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "").replace("/", "").replace("-", "")
        
        if from_unit in ["LMIN", "LPM", "LPERMIN"]:
            return value
        elif from_unit in ["GPM", "GALMIN", "GALPERMIN"]:
            return value * 3.78541
        else:
            _LOGGER.warning(f"Unknown flow unit '{from_unit}', assuming L/MIN")
            return value
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for liters per minute conversion: {value}")
        return None


def gpm(value, from_unit="GPM"):
    """Convert flow rate to Gallons per Minute."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace(" ", "").replace("/", "").replace("-", "")
        
        if from_unit in ["GPM", "GALMIN", "GALPERMIN"]:
            return value
        elif from_unit in ["LMIN", "LPM", "LPERMIN"]:
            return value / 3.78541
        else:
            _LOGGER.warning(f"Unknown flow unit '{from_unit}', assuming GPM")
            return value
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for gallons per minute conversion: {value}")
        return None


# Temperature conversion filters
def c(value, from_unit="C"):
    """Convert temperature to Celsius."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace("°", "")
        
        if from_unit in ["C", "CELSIUS"]:
            return value
        elif from_unit in ["F", "FAHRENHEIT"]:
            return (value - 32) * 5 / 9
        elif from_unit in ["K", "KELVIN"]:
            return value - 273.15
        else:
            _LOGGER.warning(f"Unknown temperature unit '{from_unit}', assuming Celsius")
            return value
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for celsius conversion: {value}")
        return None


def f(value, from_unit="C"):
    """Convert temperature to Fahrenheit."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace("°", "")
        
        if from_unit in ["F", "FAHRENHEIT"]:
            return value
        elif from_unit in ["C", "CELSIUS"]:
            return (value * 9 / 5) + 32
        elif from_unit in ["K", "KELVIN"]:
            return (value - 273.15) * 9 / 5 + 32
        else:
            _LOGGER.warning(f"Unknown temperature unit '{from_unit}', assuming Celsius")
            return (value * 9 / 5) + 32
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for fahrenheit conversion: {value}")
        return None


def k(value, from_unit="C"):
    """Convert temperature to Kelvin."""
    try:
        value = float(value)
        from_unit = str(from_unit).upper().replace("°", "")
        
        if from_unit in ["K", "KELVIN"]:
            return value
        elif from_unit in ["C", "CELSIUS"]:
            return value + 273.15
        elif from_unit in ["F", "FAHRENHEIT"]:
            return (value - 32) * 5 / 9 + 273.15
        else:
            _LOGGER.warning(f"Unknown temperature unit '{from_unit}', assuming Celsius")
            return value + 273.15
    except (ValueError, TypeError):
        _LOGGER.error(f"Invalid value for kelvin conversion: {value}")
        return None


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the unit conversions component."""
    _LOGGER.info("Setting up unit conversions filters")
    
    # Get the Jinja2 environment from hass
    env: TemplateEnvironment = hass.data.get("template")
    
    if env is None:
        _LOGGER.error("Could not find template environment in hass.data")
        return False
    
    # Register all filters
    env.filters.update({
        # Power filters
        'w': w,
        'kw': kw,
        # Energy filters
        'wh': wh,
        'kwh': kwh,
        'j': j,
        'btu': btu,
        # Flow filters
        'lpm': lpm,
        'gpm': gpm,
        # Temperature filters
        'c': c,
        'f': f,
        'k': k,
    })
    
    _LOGGER.info("Unit conversion filters registered successfully")
    return True