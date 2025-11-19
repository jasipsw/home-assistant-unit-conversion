# Home Assistant Unit Conversion Filters

A Home Assistant HACS custom component that provides global Jinja2 filters for automatic unit conversions. Perfect for creating derivative sensors and custom templates with different unit systems.

## Features

- **Flow Conversions**: L/min ↔ GPM
- **Temperature Conversions**: Celsius ↔ Fahrenheit
- **Power Conversions**: Watts ↔ Kilowatts ↔ Horsepower ↔ BTU/hr
- **Energy Conversions**: Joules ↔ Wh ↔ kWh ↔ BTU ↔ Calories
- Robust handling of unit variations (case-insensitive, punctuation-tolerant)
- Simple, intuitive Jinja2 filter syntax

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/jasipsw/home-assistant-unit-conversion`
6. Select category: "Integration"
7. Click "Add"
8. Find "Unit Conversions" in the integration list and install it
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/unit_conversions` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Usage

All filters follow the same pattern:
```jinja2
{{ value | filter_name('source_unit') }}
```

### Flow Conversions

Convert between liters per minute and gallons per minute.

#### `l_per_min` - Convert to Liters per Minute

**Supported units**: L/min, LPM, L/MIN, GPM, GAL/MIN

```jinja2
{{ 10 | l_per_min('GPM') }}          # 37.8541 L/min
{{ 100 | l_per_min('L/min') }}       # 100.0 L/min
{{ states('sensor.cx50_pump_flow_gpm') | float | l_per_min('GPM') }}
```

#### `gpm` - Convert to Gallons per Minute

**Supported units**: L/min, LPM, L/MIN, GPM, GAL/MIN

```jinja2
{{ 37.8541 | gpm('L/min') }}         # 10.0 GPM
{{ 5 | gpm('GPM') }}                 # 5.0 GPM
{{ states('sensor.pump_flow') | float | gpm('L/min') }}
```

### Temperature Conversions

Convert between Celsius and Fahrenheit.

#### `celsius` - Convert to Celsius

**Supported units**: C, Celsius, F, Fahrenheit, °C, °F

```jinja2
{{ 32 | celsius('F') }}              # 0.0 °C
{{ 100 | celsius('F') }}             # 37.78 °C
{{ states('sensor.cx50_outlet_temp') | float | celsius('F') }}
```

#### `fahrenheit` - Convert to Fahrenheit

**Supported units**: C, Celsius, F, Fahrenheit, °C, °F

```jinja2
{{ 0 | fahrenheit('C') }}            # 32.0 °F
{{ 37 | fahrenheit('C') }}           # 98.6 °F
{{ states('sensor.outdoor_temp') | float | fahrenheit('C') }}
```

### Power Conversions

Convert between watts, kilowatts, horsepower, and BTU per hour.

#### `watts` - Convert to Watts

**Supported units**: W, Watts, kW, Kilowatts, HP, Horsepower, BTU/h, BTU/hr, BTUH

```jinja2
{{ 5 | watts('kW') }}                # 5000.0 W
{{ 1 | watts('HP') }}                # 745.7 W
{{ 1000 | watts('BTU/hr') }}         # 293.07 W
{{ states('sensor.heat_pump_thermal_power_output') | float | watts('kW') }}
```

#### `kilowatts` - Convert to Kilowatts

**Supported units**: W, Watts, kW, Kilowatts, HP, Horsepower, BTU/h, BTU/hr, BTUH

```jinja2
{{ 1500 | kilowatts('W') }}          # 1.5 kW
{{ 2 | kilowatts('HP') }}            # 1.49 kW
{{ 10000 | kilowatts('BTU/hr') }}    # 2.93 kW
{{ states('sensor.power_meter') | float | kilowatts('W') }}
```

#### `horsepower` - Convert to Horsepower

**Supported units**: W, Watts, kW, Kilowatts, HP, Horsepower, BTU/h, BTU/hr, BTUH

```jinja2
{{ 745.7 | horsepower('W') }}        # 1.0 HP
{{ 1 | horsepower('kW') }}           # 1.34 HP
{{ 2544.43 | horsepower('BTU/hr') }} # 1.0 HP
```

#### `btu_per_hour` - Convert to BTU per Hour

**Supported units**: W, Watts, kW, Kilowatts, HP, Horsepower, BTU/h, BTU/hr, BTUH

```jinja2
{{ 1000 | btu_per_hour('W') }}       # 3412.14 BTU/hr
{{ 1 | btu_per_hour('kW') }}         # 3412.14 BTU/hr
{{ 1 | btu_per_hour('HP') }}         # 2544.43 BTU/hr
```

### Energy Conversions

Convert between joules, watt-hours, kilowatt-hours, BTU, and calories.

#### `joules` - Convert to Joules

**Supported units**: J, Joules, Wh, Watt-hours, kWh, Kilowatt-hours, BTU, Cal, Calories, kCal, Kilocalories

```jinja2
{{ 1 | joules('kWh') }}              # 3600000.0 J
{{ 1 | joules('Wh') }}               # 3600.0 J
{{ 1 | joules('BTU') }}              # 1055.06 J
{{ 100 | joules('Cal') }}            # 418.4 J
```

#### `watt_hours` - Convert to Watt-hours

**Supported units**: J, Joules, Wh, Watt-hours, kWh, Kilowatt-hours, BTU, Cal, Calories, kCal, Kilocalories

```jinja2
{{ 3600 | watt_hours('J') }}         # 1.0 Wh
{{ 1 | watt_hours('kWh') }}          # 1000.0 Wh
{{ 1 | watt_hours('BTU') }}          # 0.293 Wh
{{ states('sensor.daily_energy') | float | watt_hours('J') }}
```

#### `kilowatt_hours` - Convert to Kilowatt-hours

**Supported units**: J, Joules, Wh, Watt-hours, kWh, Kilowatt-hours, BTU, Cal, Calories, kCal, Kilocalories

```jinja2
{{ 3600000 | kilowatt_hours('J') }}  # 1.0 kWh
{{ 1000 | kilowatt_hours('Wh') }}    # 1.0 kWh
{{ 3412.14 | kilowatt_hours('BTU') }}# 1.0 kWh
{{ states('sensor.heat_pump_output_power_interval_kwh') | float | kilowatt_hours('kWh') }}
```

#### `btu_energy` - Convert to BTU (Energy)

**Supported units**: J, Joules, Wh, Watt-hours, kWh, Kilowatt-hours, BTU, Cal, Calories, kCal, Kilocalories

```jinja2
{{ 1055.06 | btu_energy('J') }}      # 1.0 BTU
{{ 1 | btu_energy('kWh') }}          # 3412.14 BTU
{{ 0.293 | btu_energy('Wh') }}       # 1.0 BTU
```

#### `calories` - Convert to Calories

**Supported units**: J, Joules, Wh, Watt-hours, kWh, Kilowatt-hours, BTU, Cal, Calories, kCal, Kilocalories

```jinja2
{{ 4.184 | calories('J') }}          # 1.0 Cal
{{ 1 | calories('kCal') }}           # 1000.0 Cal
{{ 1.162 | calories('Wh') }}         # 1000.0 Cal (approx)
```

## Unit Variations

All filters handle common variations automatically:
- **Case insensitive**: `kW`, `KW`, `kw` all work
- **Punctuation tolerant**: `BTU/hr`, `BTU/h`, `BTUH`, `BTU_PER_HOUR` all work
- **Spaces ignored**: `L/min`, `L / min`, `LMIN` all work
- **Symbol support**: `°C`, `°F`, `C`, `F` all work for temperature

## Example Dashboard Card

Add this markdown card to your dashboard to test the filters:

```yaml
type: markdown
content: |
  ## Unit Conversion Filter Demo
  
  {% if states.sensor.cx50_pump_flow_gpm is defined %}
  ### ✅ Unit Conversion Filters Active
  
  #### Flow Conversions (using constants)
  - 10 GPM = {{ 10 | l_per_min('GPM') | round(2) }} L/min
  - 50 L/min = {{ 50 | gpm('L/min') | round(2) }} GPM
  
  #### Temperature Conversions (using constants)
  - 75°F = {{ 75 | celsius('F') | round(2) }}°C
  - 25°C = {{ 25 | fahrenheit('C') | round(2) }}°F
  
  #### Power Conversions (using constants)
  - 5 kW = {{ 5 | watts('kW') }} W
  - 1 HP = {{ 1 | watts('HP') | round(2) }} W
  - 1000 BTU/hr = {{ 1000 | watts('BTU/hr') | round(2) }} W
  
  #### Energy Conversions (using constants)
  - 1 kWh = {{ 1 | joules('kWh') }} J
  - 3600 J = {{ 3600 | watt_hours('J') }} Wh
  - 1000 Wh = {{ 1000 | kilowatt_hours('Wh') }} kWh
  
  ---
  
  #### Real Sensor Examples
  
  **Flow**: Pump = {{ states('sensor.cx50_pump_flow_gpm') | float(0) }} GPM = 
  {{ states('sensor.cx50_pump_flow_gpm') | float(0) | l_per_min('GPM') | round(2) }} L/min
  
  **Temperature**: Outlet = {{ states('sensor.cx50_outlet_temp') | float(0) }}°F = 
  {{ states('sensor.cx50_outlet_temp') | float(0) | celsius('F') | round(2) }}°C
  
  **Power**: Thermal Output = {{ states('sensor.heat_pump_thermal_power_output') | float(0) }} kW = 
  {{ states('sensor.heat_pump_thermal_power_output') | float(0) | watts('kW') | round(0) }} W = 
  {{ states('sensor.heat_pump_thermal_power_output') | float(0) | horsepower('kW') | round(2) }} HP
  
  **Energy**: Interval = {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) }} kWh = 
  {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) | watt_hours('kWh') | round(2) }} Wh = 
  {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) | btu_energy('kWh') | round(2) }} BTU
  
  {% else %}
  ### ⚠️ Unit Conversion Filters Not Detected
  
  The unit conversion custom component may not be installed or loaded.
  
  #### Installation Steps:
  1. Install via HACS:
     - Go to HACS → Integrations
     - Click menu → Custom repositories
     - Add: `https://github.com/jasipsw/home-assistant-unit-conversion`
     - Category: Integration
     - Install "Unit Conversions"
  2. Restart Home Assistant
  3. Refresh this dashboard
  
  #### Manual Installation:
  1. Copy `custom_components/unit_conversions` to your config
  2. Restart Home Assistant
  3. Refresh this dashboard
  {% endif %}
title: Unit Conversion Test
```

### Best Practices

1. **Always handle missing sensors with defaults**:
   ```jinja2
   {{ states('sensor.power') | float(0) | watts('kW') }}
   ```

2. **Use rounding for display**:
   ```jinja2
   {{ value | kilowatts('W') | round(2) }} kW
   ```

3. **Check filter availability** using the `default` filter or conditional checks:
   ```jinja2
   {% if 100 | watts('kW') | default(None) is not none %}
     Filters are working!
   {% endif %}
   ```

4. **Combine with other filters** for rich formatting:
   ```jinja2
   {{ states('sensor.power') | float(0) | kilowatts('W') | round(2) }} kW
   ```

## Supported Units Reference

### Flow
- **L/min**: L/min, LPM, LMIN, L/MIN
- **GPM**: GPM, GALMIN, GAL/MIN

### Temperature
- **Celsius**: C, CELSIUS, °C
- **Fahrenheit**: F, FAHRENHEIT, °F

### Power
- **Watts**: W, WATT, WATTS
- **Kilowatts**: kW, KW, KILOWATT, KILOWATTS
- **Horsepower**: HP, HORSEPOWER
- **BTU/hr**: BTU/H, BTU/HR, BTUH, BTUHR, BTU_PER_HOUR

### Energy
- **Joules**: J, JOULE, JOULES
- **Watt-hours**: Wh, WH, WATTHOUR, WATTHOURS
- **Kilowatt-hours**: kWh, KWH, KILOWATTHOUR, KILOWATTHOURS
- **BTU**: BTU, BRITISHTHERMALUNIT
- **Calories**: CAL, CALORIE, CALORIES
- **Kilocalories**: KCAL, KILOCALORIE, KILOCALORIES

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See the LICENSE file for details.
