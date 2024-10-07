"""
area_data.py
==================================
Functions to retrieve data that are specific to areas and relevant to all indicators. For example: Deprivation decile.
"""


import pandas as pd
import warnings
from .retrieve_data import get_data_by_indicator_ids


def defined_qcut(df, value_series, number_of_bins, bins_for_extras, labels=False):
    """
    Allows users to define how values are split into bins when clustering.

    :param df: Dataframe of values
    :param value_series: Name of value column to rank upon
    :param number_of_bins: Integer of number of bins to create
    :param bins_for_extras: Ordered list of bin numbers to assign uneven splits
    :param labels: Optional. Labels for bins if required
    :return: A dataframe with a new column 'bins' which contains the cluster numbers
    """
    if max(bins_for_extras) > number_of_bins or any(x < 0 for x in bins_for_extras):
        raise ValueError('Attempted to allocate to a bin that doesnt exist')
    base_number, number_of_values_to_allocate = divmod(df[value_series].count(), number_of_bins)
    bins_for_extras = bins_for_extras[:number_of_values_to_allocate]
    if number_of_values_to_allocate == 0:
        df['bins'] = pd.qcut(df[value_series], number_of_bins, labels=labels)
        return df
    elif number_of_values_to_allocate > len(bins_for_extras):
        raise ValueError('There are more values to allocate than the list provided, please select more bins')
    bins = {}
    for i in range(number_of_bins):
        number_of_values_in_bin = base_number
        if i in bins_for_extras:
            number_of_values_in_bin += 1
        bins[i] = number_of_values_in_bin
    df['rank'] = df[value_series].rank()
    df = df.sort_values(by=['rank'])
    df['bins'] = 0
    row_to_start_allocate = 0
    row_to_end_allocate = 0
    for bin_number, number_in_bin in bins.items():
        row_to_end_allocate += number_in_bin
        bins.update({bin_number: [number_in_bin, row_to_start_allocate, row_to_end_allocate]})
        row_to_start_allocate = row_to_end_allocate
    conditions = [df['rank'].iloc[v[1]: v[2]] for k, v in bins.items()]
    series_to_add = pd.Series()
    for idx, series in enumerate(conditions):
        series[series > -1] = idx
        series_to_add = series_to_add.append(series)
    df['bins'] = series_to_add
    df['bins'] = df['bins'] + 1
    df = df.reset_index()
    return df


extra_areas = {
    1: [0],
    2: [0, 5],
    3: [0, 3, 7],
    4: [0, 2, 6, 8],
    5: [0, 2, 4, 6, 8],
    6: [0, 1, 3, 5, 6, 8],
    7: [0, 1, 2, 4, 5, 7, 8],
    8: [0, 1, 2, 3, 5, 6, 7, 8],
    9: [0, 1, 2, 3, 4, 5, 6, 7, 8]
}


def deprivation_decile(area_type_id, year='2015', area_code=None):
    """
    Takes in an area type id and returns a pandas series of deprivation deciles for those areas (with the areas as an
    index. If a specific area is requested, it returns just the deprivation decile value.

    :param area_type_id: Area type id as denoted by the Fingertips API
    :param year: Year of deprivation score
    :param area_code: Optional. Area code for area type to return a single value for that area
    :return: A pandas series of deprivation scores with area codes as the index. Or single value if area is specified.
    """
    warnings.warn('Caution, the deprivation deciles are being calculated on the fly and might show some inconsistencies'
                  ' from the live Fingertips site.')
    acceptable_deprivation_years_la = ['2010', '2015']
    acceptable_deprivation_years_gp = ['2015']
    acceptable_area_types = [3, 101, 102, 7, 153]
    order_of_extra_values = []
    if not isinstance(year, str):
        year = str(year)
    if year not in acceptable_deprivation_years_la and area_type_id != 7:
        raise ValueError \
            ('The acceptable years are 2010 and 2015 for local authorities and CCGs, please select one of these')
    elif year not in acceptable_deprivation_years_gp:
        raise ValueError('The acceptable years are 2015, please select this')
    if area_type_id not in acceptable_area_types:
        raise ValueError('Currently, we support deprivation decile for District & UA, County & UA, MSOA and GP area '
                         'types')
    if area_type_id == 3:
        indicator_id = 93275
        area_dep_dec = get_data_by_indicator_ids(indicator_id, area_type_id, parent_area_type_id=101, profile_id=143,
                                                 include_sortable_time_periods=True)
    else:
        indicator_id = 91872
        area_dep_dec = get_data_by_indicator_ids(indicator_id, area_type_id)
    if area_type_id == 102:
        order_of_extra_values = [0, 9, 1, 2, 3, 4, 5, 6, 7, 8]

    area_dep_dec = area_dep_dec[area_dep_dec['Area Code'] != 'E92000001']
    if not order_of_extra_values:
        order_of_extra_values = extra_areas[area_dep_dec['Value'].count() % 10]
    area_dep_dec = defined_qcut(area_dep_dec, 'Value', 10, order_of_extra_values)
    area_dep_dec.set_index('Area Code', inplace=True)
    if area_code:
        try:
            return area_dep_dec.loc[area_code, 'decile']
        except KeyError:
            raise KeyError('This area is not available at in this area type. Please try another area type')
    return area_dep_dec['bins']



