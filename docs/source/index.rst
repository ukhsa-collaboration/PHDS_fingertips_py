.. fingertips_py documentation master file, created by
   sphinx-quickstart on Mon Oct 21 13:56:10 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

fingertips_py documentation
***************************

Introduction
============

This is a python package to interact with the Office for Health Improvement & Disparities'
`Fingertips <https://fingertips.phe.org.uk/>`_ data tool. Fingertips is a
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
============

This packaged should be installed using pip:

.. code-block::
  
  pip install fingertips_py


Or it can be compiled from source (still requires pip):

.. code-block::
  
  pip install git+https://github.com/ukhsa-collaboration/PHDS_fingertips_py.git


Usage
=====

fingertips_py should be imported and used in line with standard python conventions.
It is suggested that if the whole package is to be imported then the following convention is used:

.. code-block::
  
  import fingertips_py as ftp


The package returns data in a variety of types dependent on the
function.

For more information on any function, you can use:

.. code-block::
  
  help(*fingertips_py function name*)


Example
=======

This is an example of a workflow for retrieving data for the indicator
on *Healthy Life Expectancy at Birth* from the *Public Health Outcomes
Framework* profile.

.. code-block::
  
  import fingertips_py as ftp

  phof = ftp.get_profile_by_name('public health outcomes framework')
  phof_meta = ftp.get_metadata_for_profile_as_dataframe(phof['Id'])
  indicator_meta = phof_meta[phof_meta['Indicator'].str.contains('Healthy')]
  print(indicator_meta)

      Indicator ID                                          Indicator  ...
  0          90362            0.1i - Healthy life expectancy at birth  ...
  55         92543  2.05ii - Proportion of children aged 2-2½yrs r...  ...



We can see that the *Healthy life expectancy at birth* indicator has an
id of 90362. The data for this indicator at all geographical breakdowns
can be retrieved using `get_data_for_indicator_at_all_available_geographies()`

.. code-block::
  
  healthy_life_data = ftp.get_data_for_indicator_at_all_available_geographies(90362)



Licence
=======

This project is released under the `GPL-3 <https://opensource.org/licenses/GPL-3.0/>`_
licence.


.. toctree::
   :maxdepth: 2
   :hidden:

   modules

