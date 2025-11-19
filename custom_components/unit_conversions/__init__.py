"""
Home Assistant Custom Filters: Unit Conversions
Provides global Jinja2 filters for flow, temperature, power, and energy conversions.
Supports common units with robust handling of case variations and punctuation.
"""

from homeassistant.core import HomeAssistant

def l_per_min(value, from_unit="L/MIN"):
    """Convert value to Liters per Minute from L/min or GPM."""
    try:
        v = float(value)
    except (ValueError, TypeError):
        return None
    u = str(from_unit or "").replace(" ", "").replace("/", "").replace("_", "").upper()
    if u in ("LPM", "LMIN", "L/MIN"):
        return v
    elif u in ("GPM", "GALMIN", "GAL/MIN"):
        return v * 3.78541
    return v

def gpm(value, from_unit="L/MIN"):
    """Convert value to Gallons per Minute from L/min or GPM."""
    try:
        v = float(value)
    except (ValueError, TypeError):
        return None
    u = str(from_unit or "").replace(" ", "").replace("/", "").replace("_", "").upper()
    if u in ("GPM", "GALMIN", "GAL/MIN"):
        return v
    elif u in ("LPM", "LMIN", "L/MIN"):
        return v * 0.264172
    return v

def celsius(value, from_unit="C"):
    """Convert value to Celsius from Celsius or Fahrenheit."""
    try:
        v = float(value)
    except (ValueError, TypeError):
        return None
    u = str(from_unit or "C").replace("°", "").upper().strip()
    if u in ("C", "CELSIUS"):
        return v
    elif u in ("F", "FAHRENHEIT"):
        return (v - 32) * 5 / 9
    return v

def fahrenheit(value, from_unit="C"):
    """Convert value to Fahrenheit from Celsius or Fahrenheit."""
    try:
        v = float(value)
    except (ValueError, TypeError):
        return None
    u = str(from_unit or "C").replace("°", "").upper().strip()
    if u in ("F", "FAHRENHEIT"):
        return v
    elif u in ("C", "CELSIUS"):
        return v * 9 / 5 + 32
    return v

# ============================================================================
# POWER CONVERSION FILTERS
# ============================================================================

def watts(value, from_unit="W"):
    """
    Convert value to Watts from various power units.
    
    Supported input units:
    - Watts: W, WATT, WATTS
    - Kilowatts: kW, KW, KILOWATT, KILOWATTS
    - Horsepower (mechanical): HP, HORSEPOWER
    - BTU per hour: BTU/H, BTU/HR, BTUH, BTUHR, BTU_PER_HOUR
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "W")
        
    Returns:
        Value in Watts, or None if conversion fails
        
    Example:
        {{ 5 | watts('kW') }}  # Returns 5000.0
        {{ 1 | watts('HP') }}  # Returns 745.7
    """
    try:
        v = float(value)
    except (ValueError, TypeError):
        return None
    
    # Normalize unit string: remove spaces, slashes, underscores, convert to uppercase
    u = str(from_unit or "W").replace(" ", "").replace("/", "").replace("_", "").upper()
    
    # Watts (base unit)
    if u in ("W", "WATT", "WATTS"):
        return v
    # Kilowatts to Watts
    elif u in ("KW", "KILOWATT", "KILOWATTS"):
        return v * 1000.0
    # Horsepower (mechanical) to Watts
    elif u in ("HP", "HORSEPOWER"):
        return v * 745.699872
    # BTU/hr to Watts
    elif u in ("BTUH", "BTUHR", "BTUPERHOUR", "BTUPERH"):
        return v * 0.29307107
    
    # If unit not recognized, assume it's already in Watts
    return v

def kilowatts(value, from_unit="W"):
    """
    Convert value to Kilowatts from various power units.
    
    Supported input units:
    - Watts: W, WATT, WATTS
    - Kilowatts: kW, KW, KILOWATT, KILOWATTS
    - Horsepower (mechanical): HP, HORSEPOWER
    - BTU per hour: BTU/H, BTU/HR, BTUH, BTUHR, BTU_PER_HOUR
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "W")
        
    Returns:
        Value in Kilowatts, or None if conversion fails
        
    Example:
        {{ 1500 | kilowatts('W') }}  # Returns 1.5
        {{ 2 | kilowatts('HP') }}    # Returns ~1.49
    """
    watts_value = watts(value, from_unit)
    if watts_value is None:
        return None
    return watts_value / 1000.0

def horsepower(value, from_unit="W"):
    """
    Convert value to Horsepower (mechanical) from various power units.
    
    Supported input units:
    - Watts: W, WATT, WATTS
    - Kilowatts: kW, KW, KILOWATT, KILOWATTS
    - Horsepower (mechanical): HP, HORSEPOWER
    - BTU per hour: BTU/H, BTU/HR, BTUH, BTUHR, BTU_PER_HOUR
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "W")
        
    Returns:
        Value in Horsepower, or None if conversion fails
        
    Example:
        {{ 745.7 | horsepower('W') }}   # Returns ~1.0
        {{ 1 | horsepower('kW') }}      # Returns ~1.34
    """
    watts_value = watts(value, from_unit)
    if watts_value is None:
        return None
    return watts_value / 745.699872

def btu_per_hour(value, from_unit="W"):
    """
    Convert value to BTU per hour from various power units.
    
    Supported input units:
    - Watts: W, WATT, WATTS
    - Kilowatts: kW, KW, KILOWATT, KILOWATTS
    - Horsepower (mechanical): HP, HORSEPOWER
    - BTU per hour: BTU/H, BTU/HR, BTUH, BTUHR, BTU_PER_HOUR
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "W")
        
    Returns:
        Value in BTU/hr, or None if conversion fails
        
    Example:
        {{ 1000 | btu_per_hour('W') }}  # Returns ~3412.14
        {{ 1 | btu_per_hour('kW') }}    # Returns ~3412.14
    """
    watts_value = watts(value, from_unit)
    if watts_value is None:
        return None
    return watts_value / 0.29307107

# ============================================================================
# ENERGY CONVERSION FILTERS
# ============================================================================

def joules(value, from_unit="J"):
    """
    Convert value to Joules from various energy units.
    
    Supported input units:
    - Joules: J, JOULE, JOULES
    - Watt-hours: Wh, WH, WATTHOUR, WATTHOURS
    - Kilowatt-hours: kWh, KWH, KILOWATTHOUR, KILOWATTHOURS
    - BTU: BTU, BRITISHTHERMALUNIT
    - Calories: CAL, CALORIE, CALORIES (thermochemical)
    - Kilocalories: KCAL, KILOCALORIE, KILOCALORIES
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "J")
        
    Returns:
        Value in Joules, or None if conversion fails
        
    Example:
        {{ 1 | joules('kWh') }}  # Returns 3600000.0
        {{ 1 | joules('Cal') }}  # Returns 4.184
    """
    try:
        v = float(value)
    except (ValueError, TypeError):
        return None
    
    # Normalize unit string
    u = str(from_unit or "J").replace(" ", "").replace("/", "").replace("_", "").replace("-", "").upper()
    
    # Joules (base unit)
    if u in ("J", "JOULE", "JOULES"):
        return v
    # Watt-hours to Joules
    elif u in ("WH", "WATTHOUR", "WATTHOURS"):
        return v * 3600.0
    # Kilowatt-hours to Joules
    elif u in ("KWH", "KILOWATTHOUR", "KILOWATTHOURS"):
        return v * 3600000.0
    # BTU to Joules (International Table BTU)
    elif u in ("BTU", "BRITISHTHERMALUNIT", "BRITISHTHERMALUNITS"):
        return v * 1055.05585262
    # Calories (thermochemical) to Joules
    elif u in ("CAL", "CALORIE", "CALORIES"):
        return v * 4.184
    # Kilocalories to Joules
    elif u in ("KCAL", "KILOCALORIE", "KILOCALORIES"):
        return v * 4184.0
    
    # If unit not recognized, assume it's already in Joules
    return v

def watt_hours(value, from_unit="J"):
    """
    Convert value to Watt-hours from various energy units.
    
    Supported input units:
    - Joules: J, JOULE, JOULES
    - Watt-hours: Wh, WH, WATTHOUR, WATTHOURS
    - Kilowatt-hours: kWh, KWH, KILOWATTHOUR, KILOWATTHOURS
    - BTU: BTU, BRITISHTHERMALUNIT
    - Calories: CAL, CALORIE, CALORIES (thermochemical)
    - Kilocalories: KCAL, KILOCALORIE, KILOCALORIES
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "J")
        
    Returns:
        Value in Watt-hours, or None if conversion fails
        
    Example:
        {{ 3600 | watt_hours('J') }}   # Returns 1.0
        {{ 1 | watt_hours('kWh') }}    # Returns 1000.0
    """
    joules_value = joules(value, from_unit)
    if joules_value is None:
        return None
    return joules_value / 3600.0

def kilowatt_hours(value, from_unit="J"):
    """
    Convert value to Kilowatt-hours from various energy units.
    
    Supported input units:
    - Joules: J, JOULE, JOULES
    - Watt-hours: Wh, WH, WATTHOUR, WATTHOURS
    - Kilowatt-hours: kWh, KWH, KILOWATTHOUR, KILOWATTHOURS
    - BTU: BTU, BRITISHTHERMALUNIT
    - Calories: CAL, CALORIE, CALORIES (thermochemical)
    - Kilocalories: KCAL, KILOCALORIE, KILOCALORIES
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "J")
        
    Returns:
        Value in Kilowatt-hours, or None if conversion fails
        
    Example:
        {{ 3600000 | kilowatt_hours('J') }}  # Returns 1.0
        {{ 1000 | kilowatt_hours('Wh') }}    # Returns 1.0
    """
    joules_value = joules(value, from_unit)
    if joules_value is None:
        return None
    return joules_value / 3600000.0

def btu_energy(value, from_unit="J"):
    """
    Convert value to BTU (British Thermal Units) from various energy units.
    
    Supported input units:
    - Joules: J, JOULE, JOULES
    - Watt-hours: Wh, WH, WATTHOUR, WATTHOURS
    - Kilowatt-hours: kWh, KWH, KILOWATTHOUR, KILOWATTHOURS
    - BTU: BTU, BRITISHTHERMALUNIT
    - Calories: CAL, CALORIE, CALORIES (thermochemical)
    - Kilocalories: KCAL, KILOCALORIE, KILOCALORIES
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "J")
        
    Returns:
        Value in BTU, or None if conversion fails
        
    Example:
        {{ 1055.06 | btu_energy('J') }}  # Returns ~1.0
        {{ 1 | btu_energy('kWh') }}      # Returns ~3412.14
    """
    joules_value = joules(value, from_unit)
    if joules_value is None:
        return None
    return joules_value / 1055.05585262

def calories(value, from_unit="J"):
    """
    Convert value to Calories (thermochemical) from various energy units.
    
    Supported input units:
    - Joules: J, JOULE, JOULES
    - Watt-hours: Wh, WH, WATTHOUR, WATTHOURS
    - Kilowatt-hours: kWh, KWH, KILOWATTHOUR, KILOWATTHOURS
    - BTU: BTU, BRITISHTHERMALUNIT
    - Calories: CAL, CALORIE, CALORIES (thermochemical)
    - Kilocalories: KCAL, KILOCALORIE, KILOCALORIES
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit (default: "J")
        
    Returns:
        Value in Calories, or None if conversion fails
        
    Example:
        {{ 4.184 | calories('J') }}   # Returns ~1.0
        {{ 1 | calories('kCal') }}    # Returns 1000.0
    """
    joules_value = joules(value, from_unit)
    if joules_value is None:
        return None
    return joules_value / 4.184

async def async_setup(hass: HomeAssistant, config: dict):
    """
    Set up global Jinja filters for unit conversions.
    
    Registers the following filters:
    - Flow: l_per_min, gpm
    - Temperature: celsius, fahrenheit
    - Power: watts, kilowatts, horsepower, btu_per_hour
    - Energy: joules, watt_hours, kilowatt_hours, btu_energy, calories
    """
    # Flow conversions
    hass.helpers.template.global_filters["l_per_min"] = l_per_min
    hass.helpers.template.global_filters["gpm"] = gpm
    
    # Temperature conversions
    hass.helpers.template.global_filters["celsius"] = celsius
    hass.helpers.template.global_filters["fahrenheit"] = fahrenheit
    
    # Power conversions
    hass.helpers.template.global_filters["watts"] = watts
    hass.helpers.template.global_filters["kilowatts"] = kilowatts
    hass.helpers.template.global_filters["horsepower"] = horsepower
    hass.helpers.template.global_filters["btu_per_hour"] = btu_per_hour
    
    # Energy conversions
    hass.helpers.template.global_filters["joules"] = joules
    hass.helpers.template.global_filters["watt_hours"] = watt_hours
    hass.helpers.template.global_filters["kilowatt_hours"] = kilowatt_hours
    hass.helpers.template.global_filters["btu_energy"] = btu_energy
    hass.helpers.template.global_filters["calories"] = calories
    
    return True
