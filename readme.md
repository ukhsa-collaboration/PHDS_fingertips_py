# fingertips_py

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
 
## Installation
 
This packaged should be installed using pip:

    
    pip install fingertips_py 

Or it can be compiled from source (still requires pip):


    pip install git+https://github.com/PublicHealthEngland/PHDS_fingertips_py.git


## Usage

fingertips_py should be imported and used in line with standard python
conventions. It is suggested that if the whole package is to be imported
 then the following convention is used:

    >>> import fingertips_py as ftp

The package returns data in a variety of types dependent on the 
function. 

For more information on any function, you can use:

    >>> help(*fingertips_py function name*)

Or you can view the documents [here](https://fingertips-py.readthedocs.io/en/latest/).

## Example

This is an example of a workflow for retrieving data for the indicator 
on *Healthy Life Expectancy at Birth* from the *Public Health Outcomes 
Framework* profile. 

```python
import fingertips_py as ftp

# Extract the metadata for a particular profile 
phof = ftp.get_profile_by_name('public health outcomes framework')
phof_meta = ftp.get_metadata_for_profile_as_dataframe(phof['Id'])

# Extract metadata for indicators containing the string "Healthy"
indicator_meta = phof_meta[phof_meta['Indicator'].str.contains('Healthy')]

print(indicator_meta)
```
```
Indicator ID     Indicator                                          ...   
90362            0.1i - Healthy life expectancy at birth            ... 
92543            2.05ii - Proportion of children aged 2-2½yrs r     ...
```

We can see that the *Healthy life expectancy at birth* indicator has an 
id of 90362. The data for this indicator at all geographical breakdowns 
can be retrieved using `get_data_for_indicator_at_all_available_geographies()`


    >>> healthy_life_data = ftp.get_data_for_indicator_at_all_available_geographies(90362)


## Licence

This project is released under the [GPL-3](https://opensource.org/licenses/GPL-3.0)
licence.  
