## Environment
```
MacOS Catalina v10.15.1
Python 3.7
```

### Dependency
```
pandas==0.25.1
sklearn==0.21.3
numpy==1.17.2
```

## Installation
```
python(version adequately) -m pip install --user -Iv '__package_name__==__version__'
```

## File Structure
├── Readme.md
├── __pycache__
│   └── preprocess.cpython-37.pyc
├── data
│   ├── Documentation
│   │   ├── bike_trips_data_documentation.txt
│   │   └── weather_data_documentation.pdf
│   ├── hubway_stations.csv
│   └── hubway_trips.csv
├── model.p
├── models.py
├── preprocess.py
├── run.sh
├── setup.py
└──  trips_data.csv

## Test

*For Argparse' end-to-end model generation:
```
./run.sh
```

## setup.py

