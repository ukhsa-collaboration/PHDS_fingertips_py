"""
area_data.py
==================================
Functions to retrieve data that are specific to areas and relevant to all indicators. For example: Deprivation decile.
"""

import pandas as pd
import warnings
from .retrieve_data import get_data_by_indicator_ids, \
    get_all_areas_for_all_indicators
from .api_calls import get_json
from .metadata import get_metadata


def defined_qcut(df, value_series, number_of_bins, bins_for_extras,
                 labels=False):
    """
    Allows users to define how values are split into bins when clustering.

    :param df: Dataframe of values
    :param value_series: Name of value column to rank upon
    :param number_of_bins: Integer of number of bins to create
    :param bins_for_extras: Ordered list of bin numbers to assign uneven splits
    :param labels: Optional. Labels for bins if required
    :return: A dataframe with a new column 'bins' which contains the cluster numbers
    """
    if max(bins_for_extras) > number_of_bins or any(
            x < 0 for x in bins_for_extras):
        raise ValueError('Attempted to allocate to a bin that doesnt exist')
    base_number, number_of_values_to_allocate = divmod(
        df[value_series].count(), number_of_bins)
    bins_for_extras = bins_for_extras[:number_of_values_to_allocate]
    if number_of_values_to_allocate == 0:
        df['bins'] = pd.qcut(df[value_series], number_of_bins, labels=labels)
        return df
    elif number_of_values_to_allocate > len(bins_for_extras):
        raise ValueError(
            'There are more values to allocate than the list provided, please select more bins')
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
        bins.update({bin_number: [number_in_bin, row_to_start_allocate,
                                  row_to_end_allocate]})
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


def deprivation_decile(area_type_id, year=None, area_code=None, proxy=None):
    """
    Takes in an area type id and returns a pandas series of deprivation deciles
    for those areas (with the areas as an index. If a specific area is
    requested, it returns just the deprivation decile value.

    :param area_type_id: Area type id as denoted by the Fingertips API
    :param year: Year of deprivation score
    :param area_code: Optional. Area code for area type to return a single
    value for that area
    :param proxy: proxy given to the get request used to access the API
    :return: A pandas series of deprivation scores with area codes as the
    index. Or single value if area is specified.
    """

    # find all the indicator IDs that are deprivation indexes
    search_url = "https://fingertips.phe.org.uk/api/indicator_search" \
                 "?search_text=index%20AND%20deprivation%20" \
                 "AND%20score%20AND%20IMD"

    ind_area_dict = get_json(search_url, proxy=proxy)
    valid_ind = list(set([y for x in ind_area_dict.values() for y in x]))

    # Find the valid area types for the indicator IDs
    df = get_all_areas_for_all_indicators(proxy=proxy)
    df = df.loc[df["IndicatorId"].isin(valid_ind)]

    # Add in the year column
    meta_df = get_metadata(indicator_ids=valid_ind, proxy=proxy)
    meta_df["year"] = meta_df["Definition"].str.extract(r"(20[0-9]{2})")
    meta_df = meta_df[["year", "Indicator ID"]]

    df = pd.merge(df, meta_df,
                  how='left',
                  left_on="IndicatorId",
                  right_on="Indicator ID").sort_values("year", ascending=False)

    # Check the users choices
    if int(area_type_id) not in df["AreaTypeId"].values:
        raise ValueError(f"Invalid Area Type: {area_type_id} is not a "
                         f"supported area type. The supported types are"
                         f": {', '.join(set(df['AreaTypeId'].values))}.")

    elif year is not None and str(year) not in df["year"].values:
        raise ValueError(f"Invalid Year: {year} is not a "
                         f"supported year. The supported years are"
                         f": {', '.join(set(df['year'].values))}.")

    # Filter down to the right indicator ID
    if year is not None:
        df0 = df[(df["year"] == str(year))
                 & (df["AreaTypeId"] == int(area_type_id))]
    else:
        df0 = df[df["AreaTypeId"] == int(area_type_id)]

    # Check the year, area type is a valid a combination
    if df0.empty:
        err_str = f"Invalid Combination: {year} and {area_type_id} are not " \
                  f"a valid combination. The following are: \n\n"

        err_str += df.to_string(columns=['GeographicalArea',
                                         'AreaTypeId',
                                         'year'], index=False)
        raise ValueError(err_str)

    # Extract the indicator data from the API
    area_dep_dec = get_data_by_indicator_ids(df0["Indicator ID"].values[0],
                                             area_type_id, proxy=proxy)

    # Remove England from the data
    area_dep_dec = area_dep_dec[area_dep_dec['Area Code'] != 'E92000001']

    # Create the decile column
    area_dep_dec["decile"] = pd.qcut(area_dep_dec["Value"], q=10,
                                     labels=[str(x) for x in range(1, 11)])

    if area_code is None:
        return area_dep_dec

    elif area_code in area_dep_dec["Area Code"].values:
        return area_dep_dec[area_dep_dec["Area Code"] == area_code, \
            'decile'].values[0]

    else:
        raise LookupError(f"Area Code {area_code} not in the data. Possible "
                          f"areas are: "
                          f"{', '.join(area_dep_dec['Area Code'].values)}.")

