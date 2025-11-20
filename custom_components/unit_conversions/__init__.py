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
from jinja2 import Environment
import logging
from homeassistant.helpers import template

_LOGGER = logging.getLogger(__name__)

# Global reference to Home Assistant instance for use in filters
_hass_instance = None

def _get_entity_state(entity_id):
    """
    Retrieve the state and unit of measurement for an entity.
    
    Args:
        entity_id: The entity ID (e.g., 'sensor.power_meter')
    
    Returns:
        Tuple of (value, unit) or (None, None) if entity not found
    """
    if _hass_instance is None:
        _LOGGER.warning("Home Assistant instance not available")
        return None, None
    
    state = _hass_instance.states.get(entity_id)
    if state is None:
        _LOGGER.warning("Entity '%s' not found", entity_id)
        return None, None
    
    try:
        value = float(state.state)
    except (ValueError, TypeError):
        _LOGGER.warning("Entity '%s' state '%s' is not numeric", entity_id, state.state)
        return None, None
    
    unit = state.attributes.get('unit_of_measurement')
    return value, unit

def _resolve_value_and_unit(value, from_unit):
    """
    Resolve value and unit, handling both direct values and entity IDs.
    
    Args:
        value: Either a numeric value or an entity ID string
        from_unit: The unit to convert from (can be None)
    
    Returns:
        Tuple of (resolved_value, resolved_unit)
    """
    # Check if value is a string that looks like an entity ID
    if isinstance(value, str) and '.' in value:
        # Try to get entity state
        entity_value, entity_unit = _get_entity_state(value)
        if entity_value is not None:
            # Use entity's unit if from_unit not specified
            resolved_unit = from_unit if from_unit is not None else entity_unit
            return entity_value, resolved_unit
    
    # Value is not an entity ID, use as-is
    return value, from_unit

# ========== POWER CONVERSIONS ==========

def watts(value, from_unit=None):
    """
    Convert value to Watts from various power units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.power_meter')
        from_unit: Source unit (W, KW, KILOWATTS, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Watts, or None if conversion fails
    
    Example:
        {{ 5 | watts('kW') }}  -> 5000.0
        {{ 1000 | watts('W') }} -> 1000.0
        {{ 'sensor.power_meter' | watts }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("watts: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "W").replace(" ", "").replace("_", "").upper()
    
    if u in ("W", "WATT", "WATTS"):
        return v
    elif u in ("KW", "KILOWATT", "KILOWATTS"):
        return v * 1000.0
    else:
        _LOGGER.warning("watts: Unknown unit '%s', treating as Watts", u_str)
        return v

def kilowatts(value, from_unit=None):
    """
    Convert value to Kilowatts from various power units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.power_meter')
        from_unit: Source unit (W, KW, KILOWATTS, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Kilowatts, or None if conversion fails
    
    Example:
        {{ 5000 | kilowatts('W') }}  -> 5.0
        {{ 2 | kilowatts('kW') }} -> 2.0
        {{ 'sensor.power_meter' | kilowatts }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("kilowatts: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "W").replace(" ", "").replace("_", "").upper()
    
    if u in ("KW", "KILOWATT", "KILOWATTS"):
        return v
    elif u in ("W", "WATT", "WATTS"):
        return v / 1000.0
    else:
        _LOGGER.warning("kilowatts: Unknown unit '%s', treating as Watts", u_str)
        return v / 1000.0

# ========== ENERGY CONVERSIONS ==========

def watt_hours(value, from_unit=None):
    """
    Convert value to Watt-hours from various energy units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.energy_meter')
        from_unit: Source unit (Wh, kWh, J, kJ, MJ, GJ, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Watt-hours, or None if conversion fails
    
    Example:
        {{ 1 | watt_hours('kWh') }}  -> 1000.0
        {{ 3600 | watt_hours('J') }} -> 1.0
        {{ 'sensor.energy_meter' | watt_hours }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("watt_hours: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "Wh").replace(" ", "").replace("_", "").replace("-", "").upper()
    
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
        _LOGGER.warning("watt_hours: Unknown unit '%s', treating as Watt-hours", u_str)
        return v

def kilowatt_hours(value, from_unit=None):
    """
    Convert value to Kilowatt-hours from various energy units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.energy_meter')
        from_unit: Source unit (Wh, kWh, J, kJ, MJ, GJ, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Kilowatt-hours, or None if conversion fails
    
    Example:
        {{ 1000 | kilowatt_hours('Wh') }}  -> 1.0
        {{ 3.6 | kilowatt_hours('MJ') }} -> 1.0
        {{ 'sensor.energy_meter' | kilowatt_hours }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("kilowatt_hours: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "Wh").replace(" ", "").replace("_", "").replace("-", "").upper()
    
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
        _LOGGER.warning("kilowatt_hours: Unknown unit '%s', treating as Watt-hours", u_str)
        return v / 1000.0

def joules(value, from_unit=None):
    """
    Convert value to Joules from various energy units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.energy_meter')
        from_unit: Source unit (J, kJ, MJ, GJ, Wh, kWh, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Joules, or None if conversion fails
    
    Example:
        {{ 1 | joules('kJ') }}  -> 1000.0
        {{ 1 | joules('Wh') }} -> 3600.0
        {{ 'sensor.energy_meter' | joules }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("joules: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "J").replace(" ", "").replace("_", "").replace("-", "").upper()
    
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
        _LOGGER.warning("joules: Unknown unit '%s', treating as Joules", u_str)
        return v

def btu_energy(value, from_unit=None):
    """
    Convert value to BTU (British Thermal Units) from various energy units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.energy_meter')
        from_unit: Source unit (J, kJ, MJ, GJ, Wh, kWh, BTU, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in BTU, or None if conversion fails
    
    Example:
        {{ 1055.06 | btu_energy('J') }}  -> 1.0
        {{ 1 | btu_energy('kWh') }} -> 3412.14
        {{ 'sensor.energy_meter' | btu_energy }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("btu_energy: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "J").replace(" ", "").replace("_", "").replace("-", "").upper()
    
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
        _LOGGER.warning("btu_energy: Unknown unit '%s', treating as Joules", u_str)
        return v / 1055.06

# ========== FLOW CONVERSIONS ==========

def l_per_min(value, from_unit=None):
    """
    Convert value to Liters per Minute from various flow units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.water_flow')
        from_unit: Source unit (L/MIN, GPM, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Liters per Minute, or None if conversion fails
    
    Example:
        {{ 1 | l_per_min('GPM') }}  -> 3.78541
        {{ 10 | l_per_min('L/MIN') }} -> 10.0
        {{ 'sensor.water_flow' | l_per_min }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("l_per_min: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "L/MIN").replace(" ", "").replace("/", "").replace("_", "").upper()
    
    if u in ("LPM", "LMIN", "L/MIN", "LPERMIN"):
        return v
    elif u in ("GPM", "GALMIN", "GAL/MIN", "GALPERMIN"):
        return v * 3.78541  # 1 GPM = 3.78541 L/min
    else:
        _LOGGER.warning("l_per_min: Unknown unit '%s', treating as L/min", u_str)
        return v

def gpm(value, from_unit=None):
    """
    Convert value to Gallons per Minute from various flow units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.water_flow')
        from_unit: Source unit (L/MIN, GPM, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Gallons per Minute, or None if conversion fails
    
    Example:
        {{ 3.78541 | gpm('L/MIN') }}  -> 1.0
        {{ 5 | gpm('GPM') }} -> 5.0
        {{ 'sensor.water_flow' | gpm }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("gpm: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "L/MIN").replace(" ", "").replace("/", "").replace("_", "").upper()
    
    if u in ("GPM", "GALMIN", "GAL/MIN", "GALPERMIN"):
        return v
    elif u in ("LPM", "LMIN", "L/MIN", "LPERMIN"):
        return v * 0.264172  # 1 L/min = 0.264172 GPM
    else:
        _LOGGER.warning("gpm: Unknown unit '%s', treating as L/min", u_str)
        return v * 0.264172

# ========== TEMPERATURE CONVERSIONS ==========

def celsius(value, from_unit="F"):
    """
    Convert value to Celsius from various temperature units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.outdoor_temperature')
        from_unit: Source unit (C, F, K, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Celsius, or None if conversion fails
    
    Example:
        {{ 32 | celsius('F') }}  -> 0.0
        {{ 273.15 | celsius('K') }} -> 0.0
        {{ 'sensor.outdoor_temperature' | celsius }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("celsius: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "C").replace("°", "").replace(" ", "").upper().strip()
    
    if u in ("C", "CELSIUS"):
        return v
    elif u in ("F", "FAHRENHEIT"):
        return (v - 32.0) * 5.0 / 9.0
    elif u in ("K", "KELVIN"):
        return v - 273.15
    else:
        _LOGGER.warning("celsius: Unknown unit '%s', treating as Celsius", u_str)
        return v

def fahrenheit(value, from_unit=None):
    """
    Convert value to Fahrenheit from various temperature units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.outdoor_temperature')
        from_unit: Source unit (C, F, K, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Fahrenheit, or None if conversion fails
    
    Example:
        {{ 0 | fahrenheit('C') }}  -> 32.0
        {{ 273.15 | fahrenheit('K') }} -> 32.0
        {{ 'sensor.outdoor_temperature' | fahrenheit }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("fahrenheit: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "C").replace("°", "").replace(" ", "").upper().strip()
    
    if u in ("F", "FAHRENHEIT"):
        return v
    elif u in ("C", "CELSIUS"):
        return v * 9.0 / 5.0 + 32.0
    elif u in ("K", "KELVIN"):
        return (v - 273.15) * 9.0 / 5.0 + 32.0
    else:
        _LOGGER.warning("fahrenheit: Unknown unit '%s', treating as Celsius", u_str)
        return v * 9.0 / 5.0 + 32.0

def kelvin(value, from_unit=None):
    """
    Convert value to Kelvin from various temperature units.
    
    Args:
        value: Numeric value to convert or entity ID (e.g., 'sensor.outdoor_temperature')
        from_unit: Source unit (C, F, K, etc.). If None and value is an entity ID,
                   uses the entity's unit_of_measurement
    
    Returns:
        Converted value in Kelvin, or None if conversion fails
    
    Example:
        {{ 0 | kelvin('C') }}  -> 273.15
        {{ 32 | kelvin('F') }} -> 273.15
        {{ 'sensor.outdoor_temperature' | kelvin }}  -> converts using sensor's unit
    """
    # Resolve entity ID to value and unit if applicable
    v, u_str = _resolve_value_and_unit(value, from_unit)
    
    try:
        v = float(v)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("kelvin: Unable to convert value '%s' to float: %s", value, e)
        return None
    
    # Normalize unit string
    u = str(u_str or "C").replace("°", "").replace(" ", "").upper().strip()
    
    if u in ("K", "KELVIN"):
        return v
    elif u in ("C", "CELSIUS"):
        return v + 273.15
    elif u in ("F", "FAHRENHEIT"):
        return (v - 32.0) * 5.0 / 9.0 + 273.15
    else:
        _LOGGER.warning("kelvin: Unknown unit '%s', treating as Celsius", u_str)
        return v + 273.15

# ========== HOME ASSISTANT SETUP ==========
# Array of functions to add as custom filters. Creates a filter and a global macro using the functions name.
# You can also supply a dict with "name" and "function" keys to specify a custom name for the filter/macro.
custom_filters = [
    {"name": "w", "function": watts},
    {"name": "watts", "function": watts},
    {"name": "kw", "function": kilowatts},
    {"name": "kilowatts", "function": kilowatts},
    {"name": "wh", "function": watt_hours},
    {"name": "kwh", "function": kilowatt_hours},
    {"name": "j", "function": joules},
    {"name": "joules", "function": joules},
    {"name": "btu", "function": btu_energy},
    {"name": "lpm", "function": l_per_min},
    {"name": "l_per_min", "function": l_per_min},
    {"name": "gpm", "function": gpm},
    {"name": "g_per_min", "function": gpm},
    {"name": "c", "function": celsius},
    {"name": "celsius", "function": celsius},
    {"name": "f", "function": fahrenheit},
    {"name": "fahrenheit", "function": fahrenheit},
    {"name": "k", "function": kelvin},
    {"name": "kelvin", "function": kelvin},
]

def add_custom_filter_function(custom_filter, *environments):
    """Add a custom filter/macro to one or more Jinja2 environments"""
    name = custom_filter["name"] if isinstance(custom_filter, dict) else custom_filter.__name__
    function = custom_filter["function"] if isinstance(custom_filter, dict) else custom_filter
    for env in environments:
        env.globals[name] = env.filters[name] = function

def init(*args):
    """Initialize filters"""
    env = _TemplateEnvironment(*args)
    
    for f in custom_filters:
        add_custom_filter_function(f, env)

    return env


template.TemplateEnvironment = init
for f in custom_filters:
    add_custom_filter_function(f, template._NO_HASS_ENV)

async def async_setup(hass, hass_config):
    """
    Set up the Unit Conversions component.
    
    Registers all conversion filters as global Jinja2 template filters
    for use throughout Home Assistant.
    
    Returns:
        True if setup successful
    """
    config = hass_config.get("unit_conversions", {})

    tpl = template.Template("", hass)

    for f in custom_filters:
        add_custom_filter_function(f, tpl._env)

    _LOGGER.info("Unit Conversions filters registered successfully")
    return True
