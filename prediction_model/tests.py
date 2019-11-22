import unittest
import pandas as pd
from pandas.util.testing import assert_series_equal, assert_frame_equal
from preprocess import remove_outlier, add_age, fill_loc_statn, fill_loc_trips


class Test(unittest.case.TestCase):

    def test_outlier(self):
        col = 'm'
        one_to_hundred = pd.DataFrame(range(1, 101), columns = [col])
        one_to_ninetyfive = pd.DataFrame(range(1, 96), columns = [col])
        trimmed = remove_outlier(one_to_hundred, col)

        assert_frame_equal(one_to_ninetyfive, trimmed)

    def test_age_column(self):

        millenial = pd.DataFrame([1990, 2000, 2010, 2005, 1999],
                                    columns = ['birth_date'])

        millenial_age = add_age(millenial)

        compare_with =  pd.DataFrame({'birth_date': [1990, 2000, 2010, 2005, 1999],
                                        'age':[29, 19,  9, 14, 20]})

        assert_frame_equal(compare_with, millenial_age)

    def test_map_column(self):
        baseline = pd.DataFrame({'id': [10, 7, 9, 3, 4],
                                        'lat': [2.0, 0.0, 10.0, 100.0, 60.0],
                                            'lng': [-1.0, 1.0, 10.0, 0.0, 40.0]})

        initial = pd.DataFrame({'id': [10, 7, 9, 3, 4]})
        lat_dict, lng_dict = fill_loc_statn(baseline)
        result = fill_loc_trips(initial, lat_dict, lng_dict, base='id')

        assert_frame_equal(baseline, result)


if __name__ == '__main__':
    unittest.main()