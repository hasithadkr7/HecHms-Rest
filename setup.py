from setuptools import setup, find_packages

setup(
    name='hec_hms',
    version='0.0.1',
    packages=find_packages(exclude=['']),
    url='http://www.curwsl.org',
    license='MIT',
    author='hasitha',
    author_email='hasithadkr7@gamil.com',
    description='Data integration system for CUrW project managed under Mega Polis Ministry, Sri Lanka',
    include_package_data=True,
    install_requires=[],
    dependency_links=['https://github.com/nirandaperera/models/tarball/v2.0.0-snapshot-dev#egg=curw-2.0.0-snapshot'],
    zip_safe=False
)
