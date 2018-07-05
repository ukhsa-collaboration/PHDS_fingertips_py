import pandas as pd
import warnings
from .retrieve_data import get_data_by_indicator_ids


def defined_qcut(df, value_series, number_of_bins, bins_for_extras, labels=False):
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
    warnings.warn('Caution, the deprivation deciles are being calculated on the fly and might show some inconsistencies from the live fingertips site.')
    acceptable_deprivation_years_la = ['2010', '2015']
    acceptable_deprivation_years_gp = ['2010', '2011', '2012', '2015']
    acceptable_area_types = [101, 102, 7, 153]
    order_of_extra_values = []
    if not isinstance(year, str):
        year = str(year)
    if year not in acceptable_deprivation_years_la and area_type_id is not 7:
        raise ValueError \
            ('The acceptable years are 2010 and 2015 for local authorities and CCGs, please select one of these')
    elif year not in acceptable_deprivation_years_gp:
        raise ValueError('The acceptable years are 2010, 2011, 2012 and 2015, please select one of these')
    if area_type_id not in acceptable_area_types:
        raise ValueError('Currently, we support deprivation decile for District & UA, County & UA and GP area types')
    if year is not '2015':
        indicator_id = 338
        if area_type_id == 102:
            order_of_extra_values = [6, 9, 0, 1, 2, 3, 4, 5, 7, 8]
    else:
        indicator_id = 91872
        if area_type_id == 102:
            order_of_extra_values = [0, 9, 1, 2, 3, 4, 5, 6, 7, 8]
    area_dep_dec = get_data_by_indicator_ids(indicator_id, area_type_id)
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



