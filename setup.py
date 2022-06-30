import setuptools

setuptools.setup(
    name="minimal_example",
    packages=setuptools.find_packages(exclude=["minimal_example_tests"]),
    install_requires=[
        "dagster==0.15.2",
        "dagit==0.15.2",
        "pytest",
    ],
)
