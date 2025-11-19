# Example Home Assistant Dashboard Card

This markdown card demonstrates all available unit conversion filters with both constant values and real sensor examples.

## Usage

1. Copy the YAML code below
2. In Home Assistant, add a new card to your dashboard
3. Select "Manual" card type
4. Paste the YAML code
5. Save the card

## Dashboard Card YAML

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
  - 2 kW = {{ 2 | horsepower('kW') | round(2) }} HP
  
  #### Energy Conversions (using constants)
  - 1 kWh = {{ 1 | joules('kWh') }} J
  - 3600 J = {{ 3600 | watt_hours('J') }} Wh
  - 1000 Wh = {{ 1000 | kilowatt_hours('Wh') }} kWh
  - 1 kWh = {{ 1 | btu_energy('kWh') | round(2) }} BTU
  - 4184 J = {{ 4184 | calories('J') | round(2) }} Cal
  
  ---
  
  #### Real Sensor Examples
  
  **Flow Conversion**  
  Pump Flow: {{ states('sensor.cx50_pump_flow_gpm') | float(0) }} GPM = 
  {{ states('sensor.cx50_pump_flow_gpm') | float(0) | l_per_min('GPM') | round(2) }} L/min
  
  **Temperature Conversion**  
  Outlet Temp: {{ states('sensor.cx50_outlet_temp') | float(0) }}°F = 
  {{ states('sensor.cx50_outlet_temp') | float(0) | celsius('F') | round(2) }}°C
  
  **Power Conversions**  
  Thermal Output: {{ states('sensor.heat_pump_thermal_power_output') | float(0) }} kW =
  - {{ states('sensor.heat_pump_thermal_power_output') | float(0) | watts('kW') | round(0) }} W
  - {{ states('sensor.heat_pump_thermal_power_output') | float(0) | horsepower('kW') | round(2) }} HP
  - {{ states('sensor.heat_pump_thermal_power_output') | float(0) | btu_per_hour('kW') | round(0) }} BTU/hr
  
  **Energy Conversions**  
  Power Interval: {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) }} kWh =
  - {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) | joules('kWh') | round(0) }} J
  - {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) | watt_hours('kWh') | round(2) }} Wh
  - {{ states('sensor.heat_pump_output_power_interval_kwh') | float(0) | btu_energy('kWh') | round(2) }} BTU
  
  {% else %}
  ### ⚠️ Unit Conversion Filters Not Detected
  
  The unit conversion custom component may not be installed or active.
  
  #### Installation Steps:
  
  **Via HACS (Recommended):**
  1. Open HACS in Home Assistant
  2. Go to **Integrations**
  3. Click the **⋮** menu (top right) → **Custom repositories**
  4. Add repository URL: `https://github.com/jasipsw/home-assistant-unit-conversion`
  5. Select category: **Integration**
  6. Click **Add**
  7. Find **Unit Conversions** in the list and click **Download**
  8. **Restart Home Assistant**
  9. Refresh this dashboard
  
  **Manual Installation:**
  1. Download the `custom_components/unit_conversions` folder
  2. Copy to your Home Assistant `config/custom_components/` directory
  3. **Restart Home Assistant**
  4. Refresh this dashboard
  
  #### Troubleshooting:
  - Ensure the integration is in `config/custom_components/unit_conversions/`
  - Check Home Assistant logs for any errors
  - Verify the component loaded: Configuration → Logs → Search for "unit_conversions"
  
  {% endif %}
title: Unit Conversion Filter Demo
```

## Notes

### Integration Detection

The card uses the `default` filter pattern to detect if the unit conversion filters are available:

```jinja2
{% if states.sensor.cx50_pump_flow_gpm is defined %}
```

This checks for the existence of a specific sensor. If your sensors have different names, you can:

1. **Replace sensor names** with your actual sensor entities
2. **Use a test value** to check filter availability:
   ```jinja2
   {% set test_filter = 100 | watts('kW') | default(None) %}
   {% if test_filter is not none %}
   ```

### Sensor Examples

The card demonstrates conversions using these example sensors:
- `sensor.cx50_pump_flow_gpm` - Flow in GPM
- `sensor.cx50_outlet_temp` - Temperature in Fahrenheit
- `sensor.heat_pump_thermal_power_output` - Power in kW
- `sensor.heat_pump_output_power_interval_kwh` - Energy in kWh

**To use your own sensors:**
Replace these entity IDs with your actual sensor names throughout the card.

### Best Practices Demonstrated

1. **Safe value extraction**: `| float(0)` provides a default if sensor is unavailable
2. **Rounding for readability**: `| round(2)` formats to 2 decimal places
3. **Filter chaining**: Combine multiple filters for complex transformations
4. **User-friendly fallbacks**: Show installation instructions when filters aren't available
5. **Clear section headers**: Organize by conversion type for easy reference

### Customization Ideas

- **Add more conversions**: Include additional unit types as they're added
- **Filter by availability**: Only show sections for sensors that exist
- **Add timestamps**: Include `{{ now() }}` to show last update time
- **Style with Markdown**: Use tables, headers, and formatting for better presentation
- **Create separate cards**: Split into multiple cards by conversion type

## Testing

After adding the card:

1. Verify constant conversions display correctly
2. Check that sensor conversions show real values (if sensors exist)
3. Test the fallback message (temporarily rename the component to see it)
4. Ensure all filters work with various unit inputs

## Troubleshooting

**Card shows "⚠️ Not Detected" message:**
- Integration not installed → Follow installation steps
- Integration not loaded → Check HA logs
- Sensor check incorrect → Update sensor entity IDs

**Conversions show wrong values:**
- Verify source unit parameter matches sensor's actual unit
- Check sensor state is numeric (not "unknown" or "unavailable")
- Use `| float(0)` to handle non-numeric states

**Card won't save:**
- Check YAML syntax (indentation must be exact)
- Ensure Jinja2 syntax is valid
- Look for unmatched braces `{{ }}` or `{% %}`
