# Reusable Widget Manual

## Widget Framework
The platform relies on modular widget payloads containing type descriptors, values, sparkline curves, trends, and status severity indicators.

## Widget Types
- **VALUE**: Displays simple formatted text value (e.g. `widget-health` -> `88.5/100`).
- **SPARKLINE**: Encloses complex metrics dictionary and numerical trend line data (e.g. `widget-revenue`).
- **BAR_CHART**: Defines labels and datasets for future occupancy/demand representation (e.g. `widget-forecast`).
- **PIE_CHART**: Slices operations turnarounds (e.g. `widget-room-status`).
- **LIST**: Tabulates alerts or active recommendations.
