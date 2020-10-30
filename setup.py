from setuptools import find_packages, setup

setup(
    name='colon-d',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'mysql-connector-python',
        'beautifulsoup4',
        'requests'
    ],
)