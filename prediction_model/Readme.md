### Project Scope
- Packaged Flask web service
- What it does is return predicted duration of ride
- Prediction model is trained from [Boston hubway database](https://www.kaggle.com/datasets/8758bc11f7ec8eaddad308dc9ec868c0f66403dee81d2bc9062621c57611be8f?resource=download)
- Training algorithm is linear regression
- Prediction result is parametrized by age, gender and station ID(in number)
- Endpoint receives the three parameters in the format below

### Get Prediction Result using REST Endpoint

* Run:
```
python models.py
python server.py
```

* Launch 
```
http://0.0.0.0:8000/parameters?gender={}&age={}&id={}
```

* Replace {} with parameters for gender(string), age(int), station id(int). Order does not matter.

* Example:
![Example](assets/images/post_parameters_correct_format.png)

* Returns Jsonified response based on numpy calculation
![Return_example](assets/images/get_prediction_result.png)

- Example when you type in station ID in string or outside the range
![Example_2](assets/images/post_parameters_wrong_format.png)

![Return_example2](assets/images/get_error.png)

### Environment
```
MacOS Catalina v10.15.1
Python 3.7.3
```

### Dependency
```
numpy
flask
flask-restful
pandas
sklearn
setuptools
```

### Installation
```
python -m pip install --user __package_name__
```

## How to Test

* For Argparse' end-to-end model generation:

- place the missing csv files under data directory
```
./run.sh
```
* for access error, run `chmod u+x`

### Package for develop

* Go to the directory where there is `setup.py` and  run:
```
pip install -e .
```

### Unit Test for removal of data and Integration Test for added data

* Run:
```
python tests.py
```
