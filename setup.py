from setuptools import setup


setup(
    name='fingertips_py',
    version='0.3.0',
    packages=['fingertips_py'],
    url='https://github.com/ukhsa-collaboration/PHDS_fingertips_py.git',
    license='GPL-3.0',
    author='Russell Plunkett, OHID, Annabel Westermann, Hadley Nanayakkara',
    author_email='DataScience@dhsc.gov.uk, annabel.westermann@dhsc.gov.uk, hadley.nanayakkara@dhsc.gov.uk',
    description='This is a python package to interact with OHID\'s Fingertips data tool.'
                'This can be used to load data from the Fingertips API into Python for further manipulation.',
    install_requires=['pandas>=1.5', 'requests']
)
