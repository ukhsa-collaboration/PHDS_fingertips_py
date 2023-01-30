"""
area_data.py
==================================
Functions to retrieve data that are specific to areas and relevant to all
indicators. For example: Deprivation decile.
"""

import pandas as pd
from .retrieve_data import get_data_by_indicator_ids, \
    get_all_areas_for_all_indicators
from .api_calls import get_json
from .metadata import get_metadata


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

