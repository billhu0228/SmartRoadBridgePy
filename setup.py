import os
import platform
import re

import setuptools
import subprocess
import sys
import shutil
import sysconfig

from distutils.version import LooseVersion
from setuptools.command.build_ext import build_ext

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CMakeExtension(setuptools.Extension):
    def __init__(self, name, cmake_dir, api):
        setuptools.Extension.__init__(self, name, sources=[], py_limited_api=api)
        self.cmake_dir = os.path.abspath(cmake_dir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the followingextensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r"version\s*([\d.]+)",
                                                   out.decode()).group(1))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # extdir = ext.cmake_dir
        cmake_args = []
        cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
                       "-DPYTHON_EXECUTABLE=" + sys.executable]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)]
            build_args += ["--", "/m"]

        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\"{}\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version())

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        print(" ".join(e for e in ["cmake", ext.cmake_dir] + cmake_args))
        subprocess.check_call(["cmake", ext.cmake_dir] + cmake_args,
                              cwd=self.build_temp, env=env)

        subprocess.check_call(["cmake", "--build", "."] +
                              build_args, cwd=self.build_temp)
        if os.path.exists(self.build_temp):
            shutil.rmtree(self.build_temp)
        print()

# 016
setuptools.setup(name="srbpy",
                 version="0.2.0",
                 description="A Python/C++ Mixed Road Bridge Design Package",
                 url="https://github.com/billhu0228/SmartRoadBridgePy",
                 author="Bill Hu",
                 author_email="billhu0228@icloud.com",
                 license="MIT",
                 zip_safe=False,
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages("src"),
                 package_dir={"": "src"},
                 ext_modules=[
                     CMakeExtension("srbpy/alignment/useless", cmake_dir="src/srbpy/alignment",api=False),
                     CMakeExtension("srbpy/public/useless", cmake_dir="src/srbpy/public", api=False),
                 ],
                 cmdclass=dict(build_ext=CMakeBuild),
                 classifiers=[
                     "Development Status :: 3 - Alpha",
                     "Intended Audience :: Developers",
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 keywords="civil road bridge alignment",
                 project_urls={
                     'Source': 'https://github.com/billhu0228/SmartRoadBridgePy',
                 },
                 py_modules=[],
                 install_requires=[
                     'numpy',
                     'scikit-spatial>=4.0.0',
                     'PyAngle>=2.2.0',
                     'pybind11>=2.6.0',
                     'SQLAlchemy>=1.3',
                     'ezdxf>=0.13',
                 ],
                 python_requires=">=3",
                 # data_files=[],
                 # include_package_data=True,
                 # scripts=[],
                 # test_suite="tests",
                 )
