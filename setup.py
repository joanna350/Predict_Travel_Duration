from setuptools import setup, find_packages

setup(name='prediction_model',
      version='0.7',
      description='FinallyPackaged',
      author='Joanna',
      author_email='joanna@kaist.ac.kr',
      packages=find_packages(), #not sure this works
      scripts = ['prediction_model/models.py', 'prediction_model/preprocess.py'],
      zip_safe=False)