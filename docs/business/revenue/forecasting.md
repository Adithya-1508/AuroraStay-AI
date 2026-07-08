# Occupancy & Demand Forecasting Service

The `ForecastingService` performs predictive analytics over a configurable-horizon to estimate future room occupancies, guest demands, and expected revenues.

## Occupancy Forecast
- **Method**: Queries active reservation volumes against total available room capacities.
- **Fallbacks**: Computes baseline historical averages (e.g. 65% baseline) if active booking data is sparse.
- **Intervals**: Formulates confidence intervals (upper/lower bounds) indicating predictive variance.

## Demand Forecast
- **Components**: Separates expected guest bookings, walk-ins, cancellations, and no-show probabilities.
- **Seasonality**: Adjusts predictions dynamically using seasonal modifiers (e.g. summer/holiday peaks vs winter lulls).

## Revenue Forecast
- **Metrics**: Computes Average Daily Rate (ADR) and Revenue Per Available Room (RevPAR) forecasts.
