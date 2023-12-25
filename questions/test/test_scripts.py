from django.test import SimpleTestCase
import numpy as np
from questions.scripts import (
    bionomial_exact_method_test,
    bionomial_normal_theory_test,
    fishers_exact_test,
    mcnemar_test,
    one_sample_chi_sq_test_for_variances,
    paired_t_test,
    signed_rank_test,
    simple_linear_regression,
    two_sample_F_test,
    two_sample_t_eq_var,
    two_sample_t_uneq_var,
    wilcoxon_rank_test,
    ztest,
)
from scipy import stats


class ScriptsTest(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        self.data = np.array(
            [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        )
        pass

    def test_ztest(self):
        ans = ztest(self.data, 0.95, 1, 0)
        t_crit = stats.t.ppf(0.95, 10 - 1)
        print("Scripts : testing z-test")
        self.assertEquals(ans["t_crit"], t_crit)
        self.assertAlmostEquals(round(ans["lower_limit"], 3), 3.745)
        self.assertAlmostEquals(round(ans["upper_limit"], 3), 7.255)
        print("Z-Test Check")

    def test_simple_linear_regression(self):
        ans = simple_linear_regression(self.data, 0.9, 1, 0)
        print("Scripts : testing simple linear regression")
        self.assertEquals(ans["coefficient_of_determination"], 1)
        self.assertAlmostEquals(ans["intercept"], 0)
        print("Simple Linear Regression Check")

    def test_one_sample_chi_sq_test_for_variances(self):
        ans = one_sample_chi_sq_test_for_variances(self.data, 0.9, 1, 0)
        print("Scripts : testing one sample chi sq test for variances")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("Simple Linear Regression Check")

    def test_bionomial_normal_theory_test(self):
        ans = bionomial_normal_theory_test(self.data, 0.9, 1, 0)
        print("Scripts : testing bionomial_normal_theory_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("Simple Linear Regression Check")

    def test_Exact_Methods(self):
        ans = bionomial_exact_method_test(self.data, 0.9, 1, 0)
        print("Scripts : testing Exact_Methods")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("Exact_Methods Check")

    def test_signed_rank_test(self):
        ans = signed_rank_test(self.data, 0.9, 1, 0)
        print("Scripts : testing signed_rank_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("signed_rank_test Check")

    def test_two_sample_F_test(self):
        ans = two_sample_F_test(self.data, 0.9, 1, 0)
        print("Scripts : testing two_sample_F_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("two_sample_F_test Check")

    def test_paired_t_test(self):
        ans = paired_t_test(self.data, 0.9, 1, 0)
        print("Scripts : testing paired_t_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("paired_t_test Check")

    def test_two_sample_t_eq_var(self):
        ans = two_sample_t_eq_var(self.data, 0.9, 1, 0)
        print("Scripts : testing two_sample_t_eq_var")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("two_sample_t_eq_var Check")

    def test_two_sample_t_uneq_var(self):
        ans = two_sample_t_uneq_var(self.data, 0.9, 1, 0)
        print("Scripts : testing two_sample_t_uneq_var")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("two_sample_t_uneq_var Check")

    def test_mcnemar_test(self):
        ans = mcnemar_test(self.data, 0.9, 1, 0)
        print("Scripts : testing mcnemar_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("mcnemar_test Check")

    def test_fishers_exact_test(self):
        ans = fishers_exact_test(self.data, 0.9, 1, 0)
        print("Scripts : testing fishers_exact_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("fishers_exact_test Check")

    def test_wilcoxon_rank_test(self):
        ans = wilcoxon_rank_test(self.data, 0.9, 1, 0)
        print("Scripts : testing wilcoxon_rank_test")
        # self.assertEquals(ans["coefficient_of_determination"], 1)
        # self.assertAlmostEquals(ans["intercept"], 0)
        print("wilcoxon_rank_test Check")
