# Home Assistant Unit Conversion Filters

A Home Assistant custom component that provides comprehensive Jinja2 template filters for unit conversions. This HACS-compatible integration makes it easy to convert between different units in your templates, automations, and custom sensors.

## Features

### Power Conversions
- **`watts`** - Convert to Watts (W) from W or kW
- **`kilowatts`** - Convert to Kilowatts (kW) from W or kW

### Energy Conversions
- **`watt_hours`** - Convert to Watt-hours (Wh) from Wh, kWh, J, kJ, MJ, GJ
- **`kilowatt_hours`** - Convert to Kilowatt-hours (kWh) from Wh, kWh, J, kJ, MJ, GJ
- **`joules`** - Convert to Joules (J) from J, kJ, MJ, GJ, Wh, kWh

### Flow Conversions
- **`l_per_min`** - Convert to Liters per Minute from L/min or GPM
- **`gpm`** - Convert to Gallons per Minute from L/min or GPM

### Temperature Conversions
- **`celsius`** - Convert to Celsius (°C) from C, F, or K
- **`fahrenheit`** - Convert to Fahrenheit (°F) from C, F, or K
- **`kelvin`** - Convert to Kelvin (K) from C, F, or K

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

## Usage Examples

### Power Conversions

```yaml
# Convert 5 kW to Watts
{{ 5 | watts('kW') }}
# Result: 5000.0

# Convert 1000 W to Kilowatts
{{ 1000 | kilowatts('W') }}
# Result: 1.0
```

### Energy Conversions

```yaml
# Convert 1 kWh to Watt-hours
{{ 1 | watt_hours('kWh') }}
# Result: 1000.0

# Convert 3.6 MJ to Kilowatt-hours
{{ 3.6 | kilowatt_hours('MJ') }}
# Result: 1.0

# Convert 1 kWh to Joules
{{ 1 | joules('kWh') }}
# Result: 3600000.0
```

### Flow Conversions

```yaml
# Convert 1 GPM to Liters per Minute
{{ 1 | l_per_min('GPM') }}
# Result: 3.78541

# Convert 10 L/min to Gallons per Minute
{{ 10 | gpm('L/MIN') }}
# Result: 2.64172
```

### Temperature Conversions

```yaml
# Convert 32°F to Celsius
{{ 32 | celsius('F') }}
# Result: 0.0

# Convert 0°C to Fahrenheit
{{ 0 | fahrenheit('C') }}
# Result: 32.0

# Convert 0°C to Kelvin
{{ 0 | kelvin('C') }}
# Result: 273.15
```

### Using with Sensors

Create template sensors that automatically convert units:

```yaml
template:
  - sensor:
      - name: "Power in Kilowatts"
        unit_of_measurement: "kW"
        state: >
          {{ states('sensor.power_meter') | float | kilowatts('W') }}

      - name: "Flow in GPM"
        unit_of_measurement: "GPM"
        state: >
          {{ states('sensor.water_flow') | float | gpm('L/MIN') }}

      - name: "Temperature in Fahrenheit"
        unit_of_measurement: "°F"
        state: >
          {{ states('sensor.outdoor_temp') | float | fahrenheit('C') }}
```

## Testing

### Verification Card

Add this markdown card to your dashboard to verify the filters are working:

```yaml
type: markdown
content: |
  # Unit Conversion Tests
  
  ## Power Conversions
  - 5 kW → W: {{ 5 | watts('kW') }} W
  - 1000 W → kW: {{ 1000 | kilowatts('W') }} kW
  
  ## Energy Conversions
  - 1 kWh → Wh: {{ 1 | watt_hours('kWh') }} Wh
  - 1000 Wh → kWh: {{ 1000 | kilowatt_hours('Wh') }} kWh
  - 3.6 MJ → kWh: {{ 3.6 | kilowatt_hours('MJ') }} kWh
  - 1 kWh → J: {{ 1 | joules('kWh') }} J
  
  ## Flow Conversions
  - 1 GPM → L/min: {{ 1 | l_per_min('GPM') }} L/min
  - 10 L/min → GPM: {{ 10 | gpm('L/MIN') }} GPM
  
  ## Temperature Conversions
  - 32°F → °C: {{ 32 | celsius('F') }} °C
  - 0°C → °F: {{ 0 | fahrenheit('C') }} °F
  - 0°C → K: {{ 0 | kelvin('C') }} K
  - 273.15 K → °C: {{ 273.15 | celsius('K') }} °C
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
  - In kW: {{ states('sensor.power_meter') | float | kilowatts('W') }} kW
  
  ## Energy Sensor Example
  - Current: {{ states('sensor.energy_meter') }} kWh
  - In Wh: {{ states('sensor.energy_meter') | float | watt_hours('kWh') }} Wh
  - In J: {{ states('sensor.energy_meter') | float | joules('kWh') }} J
  
  ## Temperature Sensor Example
  - Current: {{ states('sensor.outdoor_temperature') }} °C
  - In °F: {{ states('sensor.outdoor_temperature') | float | fahrenheit('C') }} °F
  - In K: {{ states('sensor.outdoor_temperature') | float | kelvin('C') }} K
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

### Flow Units
- Liters per Minute: `L/MIN`, `LPM`, `LMIN`, `LPERMIN`
- Gallons per Minute: `GPM`, `GAL/MIN`, `GALMIN`, `GALPERMIN`

### Temperature Units
- Celsius: `C`, `°C`, `CELSIUS`
- Fahrenheit: `F`, `°F`, `FAHRENHEIT`
- Kelvin: `K`, `KELVIN`

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
