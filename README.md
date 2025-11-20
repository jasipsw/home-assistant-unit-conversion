# Home Assistant Unit Conversion Filters

A Home Assistant custom component that provides comprehensive Jinja2 template filters for unit conversions. This HACS-compatible integration makes it easy to convert between different units in your templates, automations, and custom sensors.

## Features

### Power Conversions
- **`w`** - Convert to Watts (W) from W or kW
- **`kw`** - Convert to Kilowatts (kW) from W or kW

### Energy Conversions
- **`wh`** - Convert to Watt-hours (Wh) from Wh, kWh, J, kJ, MJ, GJ, BTU
- **`kwh`** - Convert to Kilowatt-hours (kWh) from Wh, kWh, J, kJ, MJ, GJ, BTU
- **`j`** - Convert to Joules (J) from J, kJ, MJ, GJ, Wh, kWh, BTU
- **`btu`** - Convert to BTU (British Thermal Units) from J, kJ, MJ, GJ, Wh, kWh, BTU

### Flow Conversions
- **`lpm`** - Convert to Liters per Minute from L/min or GPM
- **`gpm`** - Convert to Gallons per Minute from L/min or GPM

### Temperature Conversions
- **`c`** - Convert to Celsius (°C) from C, F, or K
- **`f`** - Convert to Fahrenheit (°F) from C, F, or K
- **`k`** - Convert to Kelvin (K) from C, F, or K

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add the repository URL: `https://github.com/jasipsw/home-assistant-unit-conversion`
6. Select category: "Integration"
7. Click "Add"
8. Click "Install" on the Unit Conversions card
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/unit_conversions` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

After installation, add the integration to your `configuration.yaml`:

```yaml
unit_conversions:
```

Then restart Home Assistant. The filters will be automatically available in all Jinja2 templates.

## Features

### Direct Sensor Support (New!)

All filters now support passing sensor entity IDs directly! The filter will:
- Automatically retrieve the sensor's current value
- Use the sensor's `unit_of_measurement` as the source unit (if not explicitly specified)
- Convert to your target unit

```yaml
# Automatically uses sensor's unit_of_measurement
{{ 'sensor.power_meter' | kw }}

# Or explicitly specify the source unit
{{ 'sensor.power_meter' | kw('W') }}

# Both numeric values and entity IDs work
{{ 5 | kw('W') }}  # Direct value
{{ 'sensor.power_meter' | kw }}  # Entity ID
```

## Usage Examples

### Power Conversions

```yaml
# Convert 5 kW to Watts
{{ 5 | w('kW') }}
# Result: 5000.0

# Convert 1000 W to Kilowatts
{{ 1000 | kw('W') }}
# Result: 1.0

# Use sensor entity ID directly
{{ 'sensor.power_consumption' | kw }}
# Automatically converts using sensor's unit
```

### Energy Conversions

```yaml
# Watt-hours
{{ 1 | wh('kWh') }}
# Result: 1000.0

{{ 3.6 | kwh('MJ') }}
# Result: 1.0

# Convert 1 kWh to Joules
{{ 1 | j('kWh') }}
# Result: 3600000.0

# BTU Conversions
{{ 3412.14 | kwh('BTU') }}
# Result: 1.0 (BTU to kWh)

{{ 3.41214 | wh('BTU') }}
# Result: 1.0 (BTU to Wh)

{{ 1 | j('BTU') }}
# Result: 1055.06 (BTU to Joules)

{{ 1 | btu('kWh') }}
# Result: 3412.14 (kWh to BTU)

{{ 1 | btu('Wh') }}
# Result: 3.41214 (Wh to BTU)

{{ 10550.6 | btu('J') }}
# Result: 10.0 (Joules to BTU)
```

### Flow Conversions

```yaml
# Convert 1 GPM to Liters per Minute
{{ 1 | lpm('GPM') }}
# Result: 3.78541

# Convert 10 L/min to Gallons per Minute
{{ 10 | gpm('L/MIN') }}
# Result: 2.64172
```

### Temperature Conversions

```yaml
# Convert 32°F to Celsius
{{ 32 | c('F') }}
# Result: 0.0

# Convert 0°C to Fahrenheit
{{ 0 | f('C') }}
# Result: 32.0

# Convert 0°C to Kelvin
{{ 0 | k('C') }}
# Result: 273.15
```

### Using with Sensors

The filters can now directly accept sensor entity IDs! When you pass an entity ID (like `sensor.power_meter`), the filter will automatically:
1. Retrieve the current sensor value
2. Use the sensor's `unit_of_measurement` attribute as the source unit (if not explicitly specified)
3. Convert to the target unit

**New simplified syntax (recommended):**

```yaml
template:
  - sensor:
      - name: "Power in Kilowatts"
        unit_of_measurement: "kW"
        state: >
          {{ 'sensor.power_meter' | kw }}

      - name: "Energy in Watt-hours"
        unit_of_measurement: "Wh"
        state: >
          {{ 'sensor.energy_meter' | wh }}

      - name: "Flow in GPM"
        unit_of_measurement: "GPM"
        state: >
          {{ 'sensor.water_flow' | gpm }}

      - name: "Temperature in Fahrenheit"
        unit_of_measurement: "°F"
        state: >
          {{ 'sensor.outdoor_temp' | f }}
```

**Traditional syntax (still supported):**

```yaml
template:
  - sensor:
      - name: "Power in Kilowatts"
        unit_of_measurement: "kW"
        state: >
          {{ states('sensor.power_meter') | float | kw('W') }}

      - name: "Energy in Watt-hours"
        unit_of_measurement: "Wh"
        state: >
          {{ states('sensor.energy_meter') | float | wh('kWh') }}

      - name: "Flow in GPM"
        unit_of_measurement: "GPM"
        state: >
          {{ states('sensor.water_flow') | float | gpm('L/MIN') }}

      - name: "Temperature in Fahrenheit"
        unit_of_measurement: "°F"
        state: >
          {{ states('sensor.outdoor_temp') | float | f('C') }}
```

Both approaches work, but the new syntax is cleaner and automatically uses the sensor's unit!

## Testing

### Verification Card

Add this markdown card to your dashboard to verify the filters are working:

```yaml
type: markdown
content: |
  # Unit Conversion Tests
  
  ## Power Conversions
  - 5 kW → W: {{ 5 | w('kW') }} W
  - 1000 W → kW: {{ 1000 | kw('W') }} kW
  
  ## Energy Conversions
  - 1 kWh → Wh: {{ 1 | wh('kWh') }} Wh
  - 1000 Wh → kWh: {{ 1000 | kwh('Wh') }} kWh
  - 3.6 MJ → kWh: {{ 3.6 | kwh('MJ') }} kWh
  - 1 kWh → J: {{ 1 | j('kWh') }} J
  
  ## Flow Conversions
  - 1 GPM → L/min: {{ 1 | lpm('GPM') }} L/min
  - 10 L/min → GPM: {{ 10 | gpm('L/MIN') }} GPM
  
  ## Temperature Conversions
  - 32°F → °C: {{ 32 | c('F') }} °C
  - 0°C → °F: {{ 0 | f('C') }} °F
  - 0°C → K: {{ 0 | k('C') }} K
  - 273.15 K → °C: {{ 273.15 | c('K') }} °C
```

Expected results:
- 5 kW → W: **5000.0** W
- 1000 W → kW: **1.0** kW
- 1 kWh → Wh: **1000.0** Wh
- 1000 Wh → kWh: **1.0** kWh
- 3.6 MJ → kWh: **1.0** kWh
- 1 kWh → J: **3600000.0** J
- 1 GPM → L/min: **3.78541** L/min
- 10 L/min → GPM: **2.64172** GPM
- 32°F → °C: **0.0** °C
- 0°C → °F: **32.0** °F
- 0°C → K: **273.15** K
- 273.15 K → °C: **0.0** °C

### Using Real Sensors

Test with actual sensor entities in your Home Assistant:

```yaml
type: markdown
content: |
  # Real Sensor Conversions
  
  ## Power Sensor Example
  - Current: {{ states('sensor.power_meter') }} W
  - In kW: {{ states('sensor.power_meter') | float | kw('W') }} kW
  
  ## Energy Sensor Example
  - Current: {{ states('sensor.energy_meter') }} kWh
  - In Wh: {{ states('sensor.energy_meter') | float | wh('kWh') }} Wh
  - In J: {{ states('sensor.energy_meter') | float | j('kWh') }} J
  
  ## Temperature Sensor Example
  - Current: {{ states('sensor.outdoor_temperature') }} °C
  - In °F: {{ states('sensor.outdoor_temperature') | float | f('C') }} °F
  - In K: {{ states('sensor.outdoor_temperature') | float | k('C') }} K
```

## Supported Unit Variations

The filters support multiple variations of unit names for convenience:

### Power Units
- Watts: `W`, `WATT`, `WATTS`
- Kilowatts: `kW`, `KW`, `KILOWATT`, `KILOWATTS`

### Energy Units
- Watt-hours: `Wh`, `WH`, `WATTHOUR`, `WATTHOURS`
- Kilowatt-hours: `kWh`, `KWH`, `KILOWATTHOUR`, `KILOWATTHOURS`
- Joules: `J`, `JOULE`, `JOULES`
- Kilojoules: `kJ`, `KJ`, `KILOJOULE`, `KILOJOULES`
- Megajoules: `MJ`, `MEGAJOULE`, `MEGAJOULES`
- Gigajoules: `GJ`, `GIGAJOULE`, `GIGAJOULES`
- BTU: `BTU`, `BTUS`, `BRITISHTHERMALUNIT`, `BRITISHTHERMALUNITS`

### Flow Units
- Liters per Minute: `L/MIN`, `LPM`, `LMIN`, `LPERMIN`
- Gallons per Minute: `GPM`, `GAL/MIN`, `GALMIN`, `GALPERMIN`

### Temperature Units
- Celsius: `C`, `°C`, `CELSIUS`
- Fahrenheit: `F`, `°F`, `FAHRENHEIT`
- Kelvin: `K`, `KELVIN`

## Energy Conversion Reference Table

Quick reference for BTU and other energy unit conversions:

| From | To | Multiply by | Example |
|------|-----|-------------|---------|
| BTU | Wh | ÷ 3.41214 | `{{ 3.41214 \| wh('BTU') }}` = 1.0 |
| BTU | kWh | ÷ 3412.14 | `{{ 3412.14 \| kwh('BTU') }}` = 1.0 |
| BTU | J | × 1055.06 | `{{ 1 \| j('BTU') }}` = 1055.06 |
| Wh | BTU | × 3.41214 | `{{ 1 \| btu('Wh') }}` = 3.41214 |
| kWh | BTU | × 3412.14 | `{{ 1 \| btu('kWh') }}` = 3412.14 |
| J | BTU | ÷ 1055.06 | `{{ 1055.06 \| btu('J') }}` = 1.0 |
| kWh | Wh | × 1000 | `{{ 1 \| wh('kWh') }}` = 1000.0 |
| kWh | J | × 3,600,000 | `{{ 1 \| j('kWh') }}` = 3600000.0 |
| MJ | kWh | ÷ 3.6 | `{{ 3.6 \| kwh('MJ') }}` = 1.0 |

## Error Handling

All filters include robust error handling:
- Invalid numeric values return `None`
- Unknown units trigger a warning and assume a default unit
- All errors are logged for debugging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or feature requests, please use the [GitHub issue tracker](https://github.com/jasipsw/home-assistant-unit-conversion/issues).
