from setuptools import setup


setup(
    name='fingertips_py',
    version='0.2',
    packages=['fingertips_py'],
    url='https://gitlab.phe.gov.uk/Russell.Plunkett/fingertips_py.git',
    license='',
    author='Public Health England',
    author_email='russell.plunkett@phe.gov.uk, phds@phe.gov.uk',
    description='This is a python package to interact with Public Health England\'s Fingertips data tool.'
                'This can be used to load data from the Fingertips API into python for further manipulation.',
    install_requires=['pandas>=0.18.1', 'requests']
)
