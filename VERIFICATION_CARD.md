# Unit Conversion Verification Card

This markdown card can be added to your Home Assistant dashboard to verify that all unit conversion filters are working correctly.

## Installation

1. Go to your Home Assistant dashboard
2. Click "Edit Dashboard" (three dots in top right)
3. Click "+ Add Card"
4. Search for "Markdown" and select it
5. Paste the YAML content below into the card configuration
6. Click "Save"

## Basic Verification Card

This card tests all constant conversions to verify the filters are working:

```yaml
type: markdown
content: |
  # Unit Conversion Tests
  
  ## Power Conversions
  - 5 kW → W: {{ 5 | watts('kW') }} W ✓ (expected: 5000.0)
  - 1000 W → kW: {{ 1000 | kilowatts('W') }} kW ✓ (expected: 1.0)
  - 2.5 kW → W: {{ 2.5 | watts('kW') }} W ✓ (expected: 2500.0)
  
  ## Energy Conversions
  - 1 kWh → Wh: {{ 1 | watt_hours('kWh') }} Wh ✓ (expected: 1000.0)
  - 1000 Wh → kWh: {{ 1000 | kilowatt_hours('Wh') }} kWh ✓ (expected: 1.0)
  - 3.6 MJ → kWh: {{ 3.6 | kilowatt_hours('MJ') }} kWh ✓ (expected: 1.0)
  - 1 kWh → J: {{ 1 | joules('kWh') }} J ✓ (expected: 3600000.0)
  - 3600 J → Wh: {{ 3600 | watt_hours('J') }} Wh ✓ (expected: 1.0)
  - 1 kJ → J: {{ 1 | joules('kJ') }} J ✓ (expected: 1000.0)
  
  ## Flow Conversions
  - 1 GPM → L/min: {{ 1 | l_per_min('GPM') }} L/min ✓ (expected: 3.78541)
  - 10 L/min → GPM: {{ 10 | gpm('L/MIN') }} GPM ✓ (expected: 2.64172)
  - 5 GPM → L/min: {{ 5 | l_per_min('GPM') }} L/min ✓ (expected: 18.92705)
  
  ## Temperature Conversions
  - 32°F → °C: {{ 32 | celsius('F') }} °C ✓ (expected: 0.0)
  - 0°C → °F: {{ 0 | fahrenheit('C') }} °F ✓ (expected: 32.0)
  - 0°C → K: {{ 0 | kelvin('C') }} K ✓ (expected: 273.15)
  - 273.15 K → °C: {{ 273.15 | celsius('K') }} °C ✓ (expected: 0.0)
  - 100°C → °F: {{ 100 | fahrenheit('C') }} °F ✓ (expected: 212.0)
  - 212°F → °C: {{ 212 | celsius('F') }} °C ✓ (expected: 100.0)
  - 373.15 K → °F: {{ 373.15 | fahrenheit('K') }} °F ✓ (expected: 212.0)
  
  ---
  **All conversions working correctly if values match expected results**
```

## Real Sensor Verification Card

Replace the sensor entity IDs below with your actual sensors to test with real data:

```yaml
type: markdown
content: |
  # Real Sensor Unit Conversions
  
  ## Power Sensor
  Replace `sensor.power_meter` with your power sensor entity ID:
  
  - Original: {{ states('sensor.power_meter') }} W
  - In kW: {{ states('sensor.power_meter') | float(0) | kilowatts('W') | round(2) }} kW
  
  ## Energy Sensor
  Replace `sensor.energy_meter` with your energy sensor entity ID:
  
  - Original: {{ states('sensor.energy_meter') }} kWh
  - In Wh: {{ states('sensor.energy_meter') | float(0) | watt_hours('kWh') | round(2) }} Wh
  - In J: {{ states('sensor.energy_meter') | float(0) | joules('kWh') | round(0) }} J
  - In MJ: {{ (states('sensor.energy_meter') | float(0) | joules('kWh') / 1000000) | round(2) }} MJ
  
  ## Temperature Sensor
  Replace `sensor.outdoor_temperature` with your temperature sensor entity ID:
  
  - Original: {{ states('sensor.outdoor_temperature') }} °C
  - In °F: {{ states('sensor.outdoor_temperature') | float(0) | fahrenheit('C') | round(1) }} °F
  - In K: {{ states('sensor.outdoor_temperature') | float(0) | kelvin('C') | round(2) }} K
  
  ## Flow Sensor
  Replace `sensor.water_flow` with your flow sensor entity ID:
  
  - Original: {{ states('sensor.water_flow') }} L/min
  - In GPM: {{ states('sensor.water_flow') | float(0) | gpm('L/MIN') | round(2) }} GPM
```

## Advanced Multi-Sensor Dashboard Card

This comprehensive card shows multiple conversions side-by-side:

```yaml
type: markdown
content: |
  # Complete Unit Conversion Dashboard
  
  ## Constant Tests (Verification)
  
  | Test | Result | Expected | Status |
  |------|--------|----------|--------|
  | 5 kW → W | {{ 5 \| watts('kW') }} | 5000.0 | ✓ |
  | 1 kWh → Wh | {{ 1 \| watt_hours('kWh') }} | 1000.0 | ✓ |
  | 1 GPM → L/min | {{ 1 \| l_per_min('GPM') }} | 3.78541 | ✓ |
  | 32°F → °C | {{ 32 \| celsius('F') }} | 0.0 | ✓ |
  
  ## Real Sensor Examples
  
  ### Power Monitoring
  - **Current Power**: {{ states('sensor.power_meter') | float(0) | round(1) }} W
  - **Power (kW)**: {{ states('sensor.power_meter') | float(0) | kilowatts('W') | round(3) }} kW
  
  ### Energy Tracking
  - **Total Energy**: {{ states('sensor.energy_meter') | float(0) | round(2) }} kWh
  - **Energy (Wh)**: {{ states('sensor.energy_meter') | float(0) | watt_hours('kWh') | round(0) }} Wh
  - **Energy (MJ)**: {{ (states('sensor.energy_meter') | float(0) * 3.6) | round(2) }} MJ
  
  ### Temperature Monitoring
  - **Temperature**: {{ states('sensor.outdoor_temperature') | float(0) | round(1) }} °C
  - **Temp (°F)**: {{ states('sensor.outdoor_temperature') | float(0) | fahrenheit('C') | round(1) }} °F
  - **Temp (K)**: {{ states('sensor.outdoor_temperature') | float(0) | kelvin('C') | round(2) }} K
  
  ---
  *Last updated: {{ now().strftime('%Y-%m-%d %H:%M:%S') }}*
```

## Troubleshooting

If the card shows errors or unexpected values:

1. **Check Integration Status**
   - Go to Settings → Devices & Services
   - Verify "Unit Conversions" is listed and loaded

2. **Verify Configuration**
   - Ensure `unit_conversions:` is in your `configuration.yaml`
   - Restart Home Assistant after adding

3. **Check Logs**
   - Go to Settings → System → Logs
   - Look for warnings or errors related to "unit_conversions"

4. **Test Simple Conversion**
   - Try a simple card first:
     ```yaml
     type: markdown
     content: |
       Test: {{ 5 | watts('kW') }}
     ```
   - Should show: `Test: 5000.0`

5. **Replace Sensor IDs**
   - Replace example sensor IDs with your actual entities
   - Use Developer Tools → States to find correct entity IDs

## Tips for Custom Cards

- Use `| float(0)` to provide a default value if sensor is unavailable
- Use `| round(2)` to limit decimal places for readability
- Combine multiple conversions in template sensors for complex calculations
- Add units in the display text for clarity

## Example Integration with Energy Dashboard

Create template sensors for the Energy Dashboard:

```yaml
template:
  - sensor:
      - name: "Solar Power (kW)"
        unique_id: solar_power_kw
        unit_of_measurement: "kW"
        device_class: power
        state_class: measurement
        state: >
          {{ states('sensor.solar_power') | float(0) | kilowatts('W') | round(3) }}
      
      - name: "Daily Energy (MJ)"
        unique_id: daily_energy_mj
        unit_of_measurement: "MJ"
        device_class: energy
        state_class: total_increasing
        state: >
          {{ (states('sensor.daily_energy') | float(0) * 3.6) | round(2) }}
```