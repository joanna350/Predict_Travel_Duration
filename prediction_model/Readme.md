### Environment
```
MacOS Catalina v10.15.1
Python 3.7
```

### Dependency
```
flask==1.1.1
pandas==0.25.1
sklearn==0.21.3
numpy==1.17.2
flask-restful
```

### Installation
```
python(version adequately) -m pip install --user -Iv '__package_name__==__version__'
```
* I didn't use version match, but it may be necessary in the future

### File Structure
```
|-- prediction_model
|   |-- Readme.md
|   |-- __init__.py
|   |-- data
|   |   |-- Documentation
|   |   |   |-- bike_trips_data_documentation.txt
|   |   |   `-- weather_data_documentation.pdf
|   |   |-- hubway_stations.csv
|   |   `-- hubway_trips.csv
|   |-- lat_dict.p
|   |-- lng_dict.p
|   |-- model.p
|   |-- models.py
|   |-- preprocess.py
|   |-- run.sh
|   |-- server.py
|   |-- tests
|   `-- trips_data.csv
`-- setup.py
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

### Emit Prediction Result using REST Endpoint

* To Run:
```
python(again-adequate-versionname-if-no-alias) server.py
```

* Launch on 
```
http://0.0.0.0:8000/parameters?gender={USER_SET}&age={US}&id={US}
```

* US short for user-set, parameters {gender, age, station id} can vary in order

* Example:
```
http://0.0.0.0:8000/parameters?gender=Male&age=24&id=4
```

* Returns jsonified response based on pure calculation

