.. fingertips_py documentation master file, created by
   sphinx-quickstart on Mon Feb 25 08:34:07 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fingertips_py's documentation
=========================================

Introduction
============


This is a python package to interact with Public Health England's
[Fingertips](https://fingertips.phe.org.uk/) data tool. Fingertips is a
major repository of population and public health indicators for England.
The site presents the information in many ways to improve accessibility
for a wide range of audiences ranging from public health professionals
and researchers to the general public. The information presented is a
mixture of data available from other public sources, and those that are
available through user access agreements with other organisations. The
source of each indicator presented is available using the
`get_metadata_for_indicator()` function.


This package can be used to load data from the Fingertips API into
python for further use.

Installation
************

This packaged should be installed using pip:

```
pip install fingertips_py
```

Or it can be compiled from source (still requires pip):

```
pip install git+https://github.com/PublicHealthEngland/PHDS_fingertips_py.git
```

Usage
*****

fingertips_py should be imported and used in line with standard python
conventions. It is suggested that if the whole package is to be imported
 then the following convention is used:

```
import fingertips_py as ftp
```

The package returns data in a variety of types dependent on the
function.

For more information on any function, you can use:

```
help(*fingertips_py function name*)
```

Or you can view the documents [here](https://fingertips-py.readthedocs.io/en/latest/).

Example
*******

This is an example of a workflow for retrieving data for the indicator
on *Healthy Life Expectancy at Birth* from the *Public Health Outcomes
Framework* profile.

```
import fingertips_py as ftp


phof = ftp.get_profile_by_name('public health outcomes framework')
phof_meta = ftp.get_metadata_for_profile_as_dataframe(phof['Id'])
indicator_meta = phof_meta[phof_meta['Indicator'].str.contains('Healthy')]
print(indicator_meta)

    Indicator ID                                          Indicator  ...
0          90362            0.1i - Healthy life expectancy at birth  ...
55         92543  2.05ii - Proportion of children aged 2-2½yrs r...  ...
```

We can see that the *Healthy life expectancy at birth* indicator has an
id of 90362. The data for this indicator at all geographical breakdowns
can be retrieved using `get_data_for_indicator_at_all_available_geographies()`

```
healthy_life_data = ftp.get_data_for_indicator_at_all_available_geographies(90362)
```

Licence
*******

This project is released under the [GPL-3](https://opensource.org/licenses/GPL-3.0)
licence.

.. automodule:: fingertips_py.metadata
   :members:
.. automodule:: fingertips_py.api_calls
   :members:
.. automodule:: fingertips_py.retrieve_data
   :members:
.. automodule:: fingertips_py.area_data
   :members:

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   fingertips_py/readme.md


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
