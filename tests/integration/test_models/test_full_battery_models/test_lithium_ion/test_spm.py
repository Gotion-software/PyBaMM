#
# Tests for the lithium-ion SPM model
#
import pybamm
import tests
import numpy as np
import unittest
from platform import system


class TestSPM(unittest.TestCase):
    def test_basic_processing(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_basic_processing_1plus1D(self):
        options = {"current collector": "potential pair", "dimensionality": 1}

        model = pybamm.lithium_ion.SPM(options)
        var = pybamm.standard_spatial_vars
        var_pts = {
            var.x_n: 5,
            var.x_s: 5,
            var.x_p: 5,
            var.r_n: 5,
            var.r_p: 5,
            var.y: 5,
            var.z: 5,
        }
        modeltest = tests.StandardModelTest(model, var_pts=var_pts)
        modeltest.test_all(skip_output_tests=True)

    def test_basic_processing_2plus1D(self):
        options = {"current collector": "potential pair", "dimensionality": 2}
        model = pybamm.lithium_ion.SPM(options)
        var = pybamm.standard_spatial_vars
        var_pts = {
            var.x_n: 5,
            var.x_s: 5,
            var.x_p: 5,
            var.r_n: 5,
            var.r_p: 5,
            var.y: 5,
            var.z: 5,
        }
        modeltest = tests.StandardModelTest(model, var_pts=var_pts)
        modeltest.test_all(skip_output_tests=True)

    def test_optimisations(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lithium_ion.SPM(options)
        optimtest = tests.OptimisationsTest(model)

        original = optimtest.evaluate_model()
        simplified = optimtest.evaluate_model(simplify=True)
        using_known_evals = optimtest.evaluate_model(use_known_evals=True)
        simp_and_known = optimtest.evaluate_model(simplify=True, use_known_evals=True)
        simp_and_python = optimtest.evaluate_model(simplify=True, to_python=True)
        np.testing.assert_array_almost_equal(original, simplified)
        np.testing.assert_array_almost_equal(original, using_known_evals)
        np.testing.assert_array_almost_equal(original, simp_and_known)
        np.testing.assert_array_almost_equal(original, simp_and_python)

        if system() != "Windows":
            simp_and_jax = optimtest.evaluate_model(simplify=True, to_jax=True)
            np.testing.assert_array_almost_equal(original, simp_and_jax)

    def test_set_up(self):
        model = pybamm.lithium_ion.SPM()
        optimtest = tests.OptimisationsTest(model)
        optimtest.set_up_model(simplify=False, to_python=True)
        optimtest.set_up_model(simplify=True, to_python=True)
        optimtest.set_up_model(simplify=False, to_python=False)
        optimtest.set_up_model(simplify=True, to_python=False)

    def test_charge(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lithium_ion.SPM(options)
        parameter_values = model.default_parameter_values
        parameter_values.update({"Current function [A]": -1})
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_zero_current(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lithium_ion.SPM(options)
        parameter_values = model.default_parameter_values
        parameter_values.update({"Current function [A]": 0})
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_thermal(self):
        options = {"thermal": "lumped"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

        options = {"thermal": "x-full"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_particle_uniform(self):
        options = {"particle": "uniform profile"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_particle_quadratic(self):
        options = {"particle": "quadratic profile"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_particle_quartic(self):
        options = {"particle": "quartic profile"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_loss_active_material(self):
        options = {
            "loss of active material": "none",
        }
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_loss_active_material_negative(self):
        options = {
            "particle cracking": "no cracking",
            "loss of active material": "negative",
        }
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_loss_active_material_positive(self):
        options = {
            "particle cracking": "no cracking",
            "loss of active material": "positive",
        }
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_loss_active_material_both(self):
        options = {
            "particle cracking": "no cracking",
            "loss of active material": "both",
        }
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_surface_form_differential(self):
        options = {"surface form": "differential"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_surface_form_algebraic(self):
        options = {"surface form": "algebraic"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()


class TestSPMWithSEI(unittest.TestCase):
    def test_well_posed_reaction_limited(self):
        options = {"sei": "reaction limited"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_well_posed_solvent_diffusion_limited(self):
        options = {"sei": "solvent-diffusion limited"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_well_posed_electron_migration_limited(self):
        options = {"sei": "electron-migration limited"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_well_posed_interstitial_diffusion_limited(self):
        options = {"sei": "interstitial-diffusion limited"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_well_posed_ec_reaction_limited(self):
        options = {"sei": "ec reaction limited", "sei porosity change": "true"}
        model = pybamm.lithium_ion.SPM(options)
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()


class TestSPMWithCrack(unittest.TestCase):
    def test_well_posed_none_crack(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "none"}
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_well_posed_no_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "no cracking"}
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_well_posed_negative_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "negative"}
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_well_posed_positive_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "positive"}
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()

    def test_well_posed_both_cracking(self):
        options = {"particle": "Fickian diffusion", "particle cracking": "both"}
        model = pybamm.lithium_ion.SPM(options)
        chemistry = pybamm.parameter_sets.Ai2020
        parameter_values = pybamm.ParameterValues(chemistry=chemistry)
        modeltest = tests.StandardModelTest(model, parameter_values=parameter_values)
        modeltest.test_all()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    sys.setrecursionlimit(10000)

    if "-v" in sys.argv:
        debug = True
    unittest.main()
