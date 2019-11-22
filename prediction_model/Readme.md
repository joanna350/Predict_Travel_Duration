### Environment
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

### Installation
```
python(version adequately) -m pip install --user -Iv '__package_name__==__version__'
```

### File Structure
```
|setup.py
|prediction_model/
|── Readme.md
|-─ __init__.py
|-─ data/
│   |-─ Documentation/
│   │   |-─ bike_trips_data_documentation.txt
│   │   └── weather_data_documentation.pdf
│   |-─ hubway_stations.csv
│   └── hubway_trips.csv
|-- models.py
|-- preprocess.py
|-- run.sh
└── tests/
```

### How to Test

* For Argparse' end-to-end model generation:
* The first line may better be removed depending on the user

```
./run.sh
```

### Package

* Go to the directory where there is `setup.py`
* Then run:
```
python -m pip install --user .
```
* This is develop mode, but user-specific issue made me choose this mode.

* Now you can go to any directory and open Python console:
```
import prediction_model
prediction_mode.preprocess.run() # default path settings will apply at the root of the directory.
prediction_mode.models.main(dataframe_returned_from_run, output_path)
```
