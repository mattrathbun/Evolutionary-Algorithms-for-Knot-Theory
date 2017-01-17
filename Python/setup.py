# Compile with: python setup.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("ADT", ["ADT.pyx"])]
        )

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("ADTOp", ["ADTOp.pyx"])]
        )

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("ADTOpPopulation", ["ADTOpPopulation.pyx"])]
        )

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("ADTOpPopulationSets", ["ADTOpPopulationSets.pyx"])]
        )

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("Fit", ["Fit.pyx"])]
        )

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("AllDiagrams", ["AllDiagrams.pyx"])]
        )
