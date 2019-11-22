### Environment
```
MacOS Catalina v10.15.1
Python 3.7.3
```

### Dependency
```
numpy==1.17.2
flask==1.1.1
flask-restful
pandas==0.25.1
sklearn==0.21.3
setuptools==41.6.0
```

### Installation
```
python(version adequately) -m pip install --user -Iv '__package_name__==__version__'
```
* didn't use version match, may be necessary as packages evolve and outdated settings allow recreation
* `-Iv` is another argument I rarely use, just to ignore the last version and install anew

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
|   |-- tests.py
|   `-- trips_data.csv
`-- setup.py
```

### How to Test

* For Argparse' end-to-end model generation:
* The first line most likely should be removed depending on the user (I have path and alias settings)

```
./run.sh
```

### Package

* Go to the directory where there is `setup.py`
* Then run:
```
python(version) -m pip install --user .
```
* This is develop mode, but user-specific issue with install mode let me stay on this.

* Now you can go to any directory and open Python console:
```
import prediction_model
```

* Examples of invoking the main functions from each script
```
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

* US short for user-set, parameters {gender, age, station id} can be typed in varying order

* Example:
```
http://0.0.0.0:8000/parameters?gender=Male&age=24&id=4
```

* Returns Jsonified response based on pure numpy calculation


### Unit Test for removal of data and Integration Test for added data

* Run:
```
python tests.py
```
* change test dataframe as you like

* Used built-in module of unittest
