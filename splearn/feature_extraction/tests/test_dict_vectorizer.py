import scipy.sparse as sp
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from splearn.feature_extraction import SparkDictVectorizer
from splearn.rdd import ArrayRDD
from splearn.utils.testing import (SplearnTestCase, assert_array_equal,
                                   assert_equal, assert_true)
from splearn.utils.validation import check_rdd_dtype


class TestDictVectorizer(SplearnTestCase):

    def make_dict_dataset(self, blocks=None):
        X = [{"foo": 1, "bar": 3},
             {"bar": 4, "baz": 2},
             {"bar": 6, "baz": 1},
             {"bar": 4, "ewo": "ok"},
             {"bar": 4, "baz": 2},
             {"bar": 9, "ewo": "fail"},
             {"bar": 4, "baz": 2},
             {"bar": 1, "quux": 1, "quuux": 2}]
        X_rdd = ArrayRDD(self.sc.parallelize(X, 4), blocks)
        return X, X_rdd

    def test_same_output(self):
        X, X_rdd = self.make_dict_dataset()
        local = DictVectorizer()
        dist = SparkDictVectorizer()

        result_local = local.fit_transform(X)
        result_dist = dist.fit_transform(X_rdd)
        result_collected = sp.vstack(result_dist.collect())

        assert_true(check_rdd_dtype(result_dist, (np.ndarray,)))
        assert_equal(local.vocabulary_, dist.vocabulary_)
        assert_array_equal(result_local.toarray(), result_collected.toarray())
