# Australian Wildfire Dashboard

Interactive dashboard visualizing historical wildfire data in Australia using Python Dash and Plotly.

## Features

- **Region Selection**: Filter by Australian states (NSW, QL, SA, TA, VI, WA)
- **Year Selection**: Filter by year from 2005 onwards
- **Pie Chart**: Monthly average estimated fire area
- **Bar Chart**: Monthly average count of vegetation fire pixels

## Tech Stack

- **Python 3.x**
- **Dash** - Web dashboard framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation

## Installation

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
python Dash_wildfire.py
```

Then open http://127.0.0.1:8050 in your browser.

## Data Source

Historical wildfire data from IBM Skills Network (loaded automatically from cloud storage).
