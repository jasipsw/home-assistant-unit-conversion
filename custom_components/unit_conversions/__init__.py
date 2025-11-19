"""
Home Assistant Custom Component: Unit Conversions

Provides Jinja2 template filters for comprehensive unit conversions including:
- Power conversions (Watts, Kilowatts)
- Energy conversions (Wh, kWh, Joules, kJ, MJ, GJ)
- Flow conversions (Liters/min, Gallons/min)
- Temperature conversions (Celsius, Fahrenheit, Kelvin)

All filters include robust error handling and support multiple unit name variations.
"""

from homeassistant.core import HomeAssistant
import logging

_LOGGER = logging.getLogger(__name__)

# ========== POWER CONVERSIONS ==========

def watts(value, from_unit="W"):
    """
    Convert value to Watts from various power units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (W, KW, KILOWATTS, etc.)
    
    Returns:
        Converted value in Watts, or None if conversion fails
    
    Example:
        {{ 5 | watts('kW') }}  -> 5000.0
        {{ 1000 | watts('W') }} -> 1000.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("watts: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "W").replace(" ", "").replace("_", "").upper()
    
    if u in ("W", "WATT", "WATTS"):
        return v
    elif u in ("KW", "KILOWATT", "KILOWATTS"):
        return v * 1000.0
    else:
        _LOGGER.warning("watts: Unknown unit '%s', treating as Watts", from_unit)
        return v

def kilowatts(value, from_unit="W"):
    """
    Convert value to Kilowatts from various power units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (W, KW, KILOWATTS, etc.)
    
    Returns:
        Converted value in Kilowatts, or None if conversion fails
    
    Example:
        {{ 5000 | kilowatts('W') }}  -> 5.0
        {{ 2 | kilowatts('kW') }} -> 2.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("kilowatts: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "W").replace(" ", "").replace("_", "").upper()
    
    if u in ("KW", "KILOWATT", "KILOWATTS"):
        return v
    elif u in ("W", "WATT", "WATTS"):
        return v / 1000.0
    else:
        _LOGGER.warning("kilowatts: Unknown unit '%s', treating as Watts", from_unit)
        return v / 1000.0

# ========== ENERGY CONVERSIONS ==========

def watt_hours(value, from_unit="Wh"):
    """
    Convert value to Watt-hours from various energy units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (Wh, kWh, J, kJ, MJ, GJ, etc.)
    
    Returns:
        Converted value in Watt-hours, or None if conversion fails
    
    Example:
        {{ 1 | watt_hours('kWh') }}  -> 1000.0
        {{ 3600 | watt_hours('J') }} -> 1.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("watt_hours: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "Wh").replace(" ", "").replace("_", "").replace("-", "").upper()
    
    if u in ("WH", "WATTHOUR", "WATTHOURS"):
        return v
    elif u in ("KWH", "KILOWATTHOUR", "KILOWATTHOURS"):
        return v * 1000.0
    elif u in ("J", "JOULE", "JOULES"):
        return v / 3600.0  # 1 Wh = 3600 J
    elif u in ("KJ", "KILOJOULE", "KILOJOULES"):
        return v * 1000.0 / 3600.0
    elif u in ("MJ", "MEGAJOULE", "MEGAJOULES"):
        return v * 1000000.0 / 3600.0
    elif u in ("GJ", "GIGAJOULE", "GIGAJOULES"):
        return v * 1000000000.0 / 3600.0
    elif u in ("BTU", "BTUS", "BRITISHTHERMALUNIT", "BRITISHTHERMALUNITS"):
        return v / 3.41214  # 1 Wh = 3.41214 BTU
    else:
        _LOGGER.warning("watt_hours: Unknown unit '%s', treating as Watt-hours", from_unit)
        return v

def kilowatt_hours(value, from_unit="Wh"):
    """
    Convert value to Kilowatt-hours from various energy units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (Wh, kWh, J, kJ, MJ, GJ, etc.)
    
    Returns:
        Converted value in Kilowatt-hours, or None if conversion fails
    
    Example:
        {{ 1000 | kilowatt_hours('Wh') }}  -> 1.0
        {{ 3.6 | kilowatt_hours('MJ') }} -> 1.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("kilowatt_hours: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "Wh").replace(" ", "").replace("_", "").replace("-", "").upper()
    
    if u in ("KWH", "KILOWATTHOUR", "KILOWATTHOURS"):
        return v
    elif u in ("WH", "WATTHOUR", "WATTHOURS"):
        return v / 1000.0
    elif u in ("J", "JOULE", "JOULES"):
        return v / 3600000.0  # 1 kWh = 3,600,000 J
    elif u in ("KJ", "KILOJOULE", "KILOJOULES"):
        return v / 3600.0  # 1 kWh = 3,600 kJ
    elif u in ("MJ", "MEGAJOULE", "MEGAJOULES"):
        return v / 3.6  # 1 kWh = 3.6 MJ
    elif u in ("GJ", "GIGAJOULE", "GIGAJOULES"):
        return v * 1000.0 / 3.6  # 1 GJ = 277.78 kWh
    elif u in ("BTU", "BTUS", "BRITISHTHERMALUNIT", "BRITISHTHERMALUNITS"):
        return v / 3412.14  # 1 kWh = 3412.14 BTU
    else:
        _LOGGER.warning("kilowatt_hours: Unknown unit '%s', treating as Watt-hours", from_unit)
        return v / 1000.0

def joules(value, from_unit="J"):
    """
    Convert value to Joules from various energy units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (J, kJ, MJ, GJ, Wh, kWh, etc.)
    
    Returns:
        Converted value in Joules, or None if conversion fails
    
    Example:
        {{ 1 | joules('kJ') }}  -> 1000.0
        {{ 1 | joules('Wh') }} -> 3600.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("joules: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "J").replace(" ", "").replace("_", "").replace("-", "").upper()
    
    if u in ("J", "JOULE", "JOULES"):
        return v
    elif u in ("KJ", "KILOJOULE", "KILOJOULES"):
        return v * 1000.0
    elif u in ("MJ", "MEGAJOULE", "MEGAJOULES"):
        return v * 1000000.0
    elif u in ("GJ", "GIGAJOULE", "GIGAJOULES"):
        return v * 1000000000.0
    elif u in ("WH", "WATTHOUR", "WATTHOURS"):
        return v * 3600.0  # 1 Wh = 3600 J
    elif u in ("KWH", "KILOWATTHOUR", "KILOWATTHOURS"):
        return v * 3600000.0  # 1 kWh = 3,600,000 J
    elif u in ("BTU", "BTUS", "BRITISHTHERMALUNIT", "BRITISHTHERMALUNITS"):
        return v * 1055.06  # 1 BTU = 1055.06 J
    else:
        _LOGGER.warning("joules: Unknown unit '%s', treating as Joules", from_unit)
        return v

def btu_energy(value, from_unit="J"):
    """
    Convert value to BTU (British Thermal Units) from various energy units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (J, kJ, MJ, GJ, Wh, kWh, BTU, etc.)
    
    Returns:
        Converted value in BTU, or None if conversion fails
    
    Example:
        {{ 1055.06 | btu_energy('J') }}  -> 1.0
        {{ 1 | btu_energy('kWh') }} -> 3412.14
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("btu_energy: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "J").replace(" ", "").replace("_", "").replace("-", "").upper()
    
    if u in ("BTU", "BTUS", "BRITISHTHERMALUNIT", "BRITISHTHERMALUNITS"):
        return v
    elif u in ("J", "JOULE", "JOULES"):
        return v / 1055.06  # 1 BTU = 1055.06 J
    elif u in ("KJ", "KILOJOULE", "KILOJOULES"):
        return v * 1000.0 / 1055.06
    elif u in ("MJ", "MEGAJOULE", "MEGAJOULES"):
        return v * 1000000.0 / 1055.06
    elif u in ("GJ", "GIGAJOULE", "GIGAJOULES"):
        return v * 1000000000.0 / 1055.06
    elif u in ("WH", "WATTHOUR", "WATTHOURS"):
        return v * 3.41214  # 1 Wh = 3.41214 BTU
    elif u in ("KWH", "KILOWATTHOUR", "KILOWATTHOURS"):
        return v * 3412.14  # 1 kWh = 3412.14 BTU
    else:
        _LOGGER.warning("btu_energy: Unknown unit '%s', treating as Joules", from_unit)
        return v / 1055.06

# ========== FLOW CONVERSIONS ==========

def l_per_min(value, from_unit="L/MIN"):
    """
    Convert value to Liters per Minute from various flow units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (L/MIN, GPM, etc.)
    
    Returns:
        Converted value in Liters per Minute, or None if conversion fails
    
    Example:
        {{ 1 | l_per_min('GPM') }}  -> 3.78541
        {{ 10 | l_per_min('L/MIN') }} -> 10.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("l_per_min: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "L/MIN").replace(" ", "").replace("/", "").replace("_", "").upper()
    
    if u in ("LPM", "LMIN", "L/MIN", "LPERMIN"):
        return v
    elif u in ("GPM", "GALMIN", "GAL/MIN", "GALPERMIN"):
        return v * 3.78541  # 1 GPM = 3.78541 L/min
    else:
        _LOGGER.warning("l_per_min: Unknown unit '%s', treating as L/min", from_unit)
        return v

def gpm(value, from_unit="L/MIN"):
    """
    Convert value to Gallons per Minute from various flow units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (L/MIN, GPM, etc.)
    
    Returns:
        Converted value in Gallons per Minute, or None if conversion fails
    
    Example:
        {{ 3.78541 | gpm('L/MIN') }}  -> 1.0
        {{ 5 | gpm('GPM') }} -> 5.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("gpm: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "L/MIN").replace(" ", "").replace("/", "").replace("_", "").upper()
    
    if u in ("GPM", "GALMIN", "GAL/MIN", "GALPERMIN"):
        return v
    elif u in ("LPM", "LMIN", "L/MIN", "LPERMIN"):
        return v * 0.264172  # 1 L/min = 0.264172 GPM
    else:
        _LOGGER.warning("gpm: Unknown unit '%s', treating as L/min", from_unit)
        return v * 0.264172

# ========== TEMPERATURE CONVERSIONS ==========

def celsius(value, from_unit="C"):
    """
    Convert value to Celsius from various temperature units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (C, F, K, etc.)
    
    Returns:
        Converted value in Celsius, or None if conversion fails
    
    Example:
        {{ 32 | celsius('F') }}  -> 0.0
        {{ 273.15 | celsius('K') }} -> 0.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("celsius: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "C").replace("°", "").replace(" ", "").upper().strip()
    
    if u in ("C", "CELSIUS"):
        return v
    elif u in ("F", "FAHRENHEIT"):
        return (v - 32.0) * 5.0 / 9.0
    elif u in ("K", "KELVIN"):
        return v - 273.15
    else:
        _LOGGER.warning("celsius: Unknown unit '%s', treating as Celsius", from_unit)
        return v

def fahrenheit(value, from_unit="C"):
    """
    Convert value to Fahrenheit from various temperature units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (C, F, K, etc.)
    
    Returns:
        Converted value in Fahrenheit, or None if conversion fails
    
    Example:
        {{ 0 | fahrenheit('C') }}  -> 32.0
        {{ 273.15 | fahrenheit('K') }} -> 32.0
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("fahrenheit: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "C").replace("°", "").replace(" ", "").upper().strip()
    
    if u in ("F", "FAHRENHEIT"):
        return v
    elif u in ("C", "CELSIUS"):
        return v * 9.0 / 5.0 + 32.0
    elif u in ("K", "KELVIN"):
        return (v - 273.15) * 9.0 / 5.0 + 32.0
    else:
        _LOGGER.warning("fahrenheit: Unknown unit '%s', treating as Celsius", from_unit)
        return v * 9.0 / 5.0 + 32.0

def kelvin(value, from_unit="C"):
    """
    Convert value to Kelvin from various temperature units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (C, F, K, etc.)
    
    Returns:
        Converted value in Kelvin, or None if conversion fails
    
    Example:
        {{ 0 | kelvin('C') }}  -> 273.15
        {{ 32 | kelvin('F') }} -> 273.15
    """
    try:
        v = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("kelvin: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(from_unit or "C").replace("°", "").replace(" ", "").upper().strip()
    
    if u in ("K", "KELVIN"):
        return v
    elif u in ("C", "CELSIUS"):
        return v + 273.15
    elif u in ("F", "FAHRENHEIT"):
        return (v - 32.0) * 5.0 / 9.0 + 273.15
    else:
        _LOGGER.warning("kelvin: Unknown unit '%s', treating as Celsius", from_unit)
        return v + 273.15

# ========== HOME ASSISTANT SETUP ==========

async def async_setup(hass: HomeAssistant, config: dict):
    """
    Set up the Unit Conversions component.
    
    Registers all conversion filters as global Jinja2 template filters
    for use throughout Home Assistant.
    
    Returns:
        True if setup successful
    """
    _LOGGER.info("Setting up Unit Conversions filters")
    
    # Register Power conversion filters
    hass.helpers.template.global_filters["watts"] = watts
    hass.helpers.template.global_filters["kilowatts"] = kilowatts
    
    # Register Energy conversion filters - register both short and long names
    hass.helpers.template.global_filters["wh"] = watt_hours
    hass.helpers.template.global_filters["watt_hours"] = watt_hours
    hass.helpers.template.global_filters["kwh"] = kilowatt_hours
    hass.helpers.template.global_filters["kilowatt_hours"] = kilowatt_hours
    hass.helpers.template.global_filters["joules"] = joules
    hass.helpers.template.global_filters["btu"] = btu_energy
    hass.helpers.template.global_filters["btu_energy"] = btu_energy
    
    # Register Flow conversion filters
    hass.helpers.template.global_filters["l_per_min"] = l_per_min
    hass.helpers.template.global_filters["gpm"] = gpm
    
    # Register Temperature conversion filters
    hass.helpers.template.global_filters["celsius"] = celsius
    hass.helpers.template.global_filters["fahrenheit"] = fahrenheit
    hass.helpers.template.global_filters["kelvin"] = kelvin
    
    _LOGGER.info("Unit Conversions filters registered successfully")
    return True
