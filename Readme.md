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
+── Readme.md
+── data
│   +── Documentation
│   │   +── bike_trips_data_documentation.txt
│   │   +── weather_data_documentation.pdf
│   +── hubway_stations.csv
│   +── hubway_trips.csv
+-- ridetime_prediction
|   |-- models.py
|   |-- preprocess.py
|   |-- run.sh
|   +-- trips_data.csv
+-- setup.py
+-- tests


## Test

*For Argparse' end-to-end model generation:
```
./run.sh
```

## setup.py

