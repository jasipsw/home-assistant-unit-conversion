"""Home Assistant Custom Filters: Unit & Temperature Conversions (L/min <-> GPM, F <-> C)"""

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

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up global Jinja filters for unit & temperature conversion."""
    hass.helpers.template.global_filters["l_per_min"] = l_per_min
    hass.helpers.template.global_filters["gpm"] = gpm
    hass.helpers.template.global_filters["celsius"] = celsius
    hass.helpers.template.global_filters["fahrenheit"] = fahrenheit
    return True
