from django.test import SimpleTestCase
import numpy as np
from questions.scripts import simple_linear_regression, ztest
from scipy import stats


class ScriptsTest(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        self.data = np.array(
            [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        )
        pass

    def test_ztest(self):
        ans = ztest(self.data, 0.95, 1)
        t_crit = stats.t.ppf(0.95, 10 - 1)
        print("Scripts : testing z-test")
        self.assertEquals(ans["t_crit"], t_crit)
        self.assertAlmostEquals(round(ans["lower_limit"], 3), 3.745)
        self.assertAlmostEquals(round(ans["upper_limit"], 3), 7.255)
        print("Z-Test Check")

    def test_simple_linear_regression(self):
        ans = simple_linear_regression(self.data, 0.9, 1)
        print("Scripts : testing simple linear regression")
        self.assertEquals(ans["coefficient_of_determination"], 1)
        self.assertAlmostEquals(ans["intercept"], 0)
        print("Simple Linear Regression Check")
