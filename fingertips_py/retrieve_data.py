"""
retrieve_data.py
==================================
A group of functions to retrieve data from Fingertips by indicator, profile,
domain (group), or geography.
"""

import pandas as pd
import numpy as np
from urllib.error import URLError, HTTPError
from .api_calls import base_url, get_json_return_df, deal_with_url_error
from .metadata import get_area_type_ids_for_profile, get_csv, \
    get_metadata_for_all_indicators, get_all_areas


def get_data_by_indicator_ids(indicator_ids, area_type_id,
                              parent_area_type_id=15, profile_id=None,
                              include_sortable_time_periods=None,
                              is_test=False,
                              proxy=None):
    """
    Returns a dataframe of indicator data given a list of indicators and area
    types.

    :param indicator_ids: List of indicator IDs as strings
    :param area_type_id: ID of area type (eg. CCG, Upper Tier Local Authority) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param profile_id: ID of profile to select by as either int or string
    :param include_sortable_time_periods: Boolean as to whether to include a sort-friendly data field
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dataframe of data relating to the given indicators
    """
    url_append = ""

    if profile_id:
        url_append += f"&profile_id={profile_id}"

    if include_sortable_time_periods:
        url_append += "&include_sortable_time_periods=yes"

    if isinstance(indicator_ids, list):
        indicator_ids = ','.join(list(map(str, indicator_ids)))

    tmp_url = base_url + f"all_data/csv/by_indicator_id?indicator_ids" \
                         f"={indicator_ids}&child_area_type_id" \
                         f"={area_type_id}&parent_area_type_id" \
                         f"={parent_area_type_id}" + url_append
    try:
        df = get_csv(tmp_url, proxy)
    except URLError:
        df = deal_with_url_error(tmp_url, proxy)
    if is_test:
        return df, tmp_url
    return df


def get_all_data_for_profile(profile_id, parent_area_type_id=15,
                             area_type_id=None, filter_by_area_codes=None,
                             is_test=False,
                             proxy=None):
    """
    Returns a dataframe of data for all indicators within a profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string.
    :param parent_area_type_id: Area type of parent area - defaults to England value.
    :param area_type_id: Option to only return data for a given area type. Area type ids are string, int or a list.
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings.
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dataframe of data for all indicators within a profile with any filters applied.
    """
    if area_type_id:
        area_types = [area_type_id]
    else:
        area_types = get_area_type_ids_for_profile(profile_id, proxy)

    list_of_df = []

    for area in area_types:

        tmp_url = base_url + f"all_data/csv/by_profile_id?child_area_type_id" \
                         f"={area}&parent_area_type_id={parent_area_type_id}" \
                         f"&profile_id={profile_id}"
        try:
            list_of_df.append(get_csv(tmp_url, proxy))

        except URLError:
            list_of_df.append(deal_with_url_error(tmp_url, proxy))
    else:
        df = pd.concat(list_of_df)

    if filter_by_area_codes:
        if isinstance(filter_by_area_codes, list):
            df = df.loc[df['Area Code'].isin(filter_by_area_codes)]
        elif isinstance(filter_by_area_codes, str):
            df = df.loc[df['Area Code'] == filter_by_area_codes]
        df = df.reset_index()

    if is_test:
        return df, tmp_url
    return df


def get_all_data_for_indicators(indicators, area_type_id,
                                parent_area_type_id=15,
                                filter_by_area_codes=None,
                                is_test=False,
                                proxy=None):
    """
    Returns a dataframe of data for given indicators at an area.

    :param indicators: List or integer or string of indicator Ids
    :param area_type_id: ID of area type (eg. ID of General Practice is 7 etc) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe of data for given indicators at an area
    """
    if isinstance(indicators, list):
        indicators = ','.join(list(map(str, indicators)))

    tmp_url = base_url + f"all_data/csv/by_indicator_id?indicator_ids" \
                         f"={indicators}&child_area_type_id={area_type_id}" \
                         f"&parent_area_type_id={parent_area_type_id}"
    try:
        df = get_csv(tmp_url, proxy)
    except URLError:
        df = deal_with_url_error(tmp_url, proxy)

    if filter_by_area_codes:
        if isinstance(filter_by_area_codes, list):
            df = df.loc[df['Area Code'].isin(filter_by_area_codes)]
        elif isinstance(filter_by_area_codes, str):
            df = df.loc[df['Area Code'] == filter_by_area_codes]

    df.reset_index(inplace=True)

    if is_test:
        return df, tmp_url
    return df


def get_all_areas_for_all_indicators(proxy=None):
    """
    Returns a dataframe of all indicators and their geographical breakdowns.

    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe of all indicators and their geographical breakdowns
    """
    url_suffix = 'available_data'

    df_avail = get_json_return_df(base_url + url_suffix, transpose=False,
                                  proxy=proxy)

    df_meta = get_metadata_for_all_indicators(proxy=proxy)

    # Get the descriptive columns
    df_meta = df_meta.loc[:,
              df_meta.columns.str.contains('Descriptive_|Indicator ID')]
    df_meta['Indicator ID'] = df_meta['Indicator ID'].astype(np.int64)

    df = pd.merge(df_avail, df_meta,
                  left_on='IndicatorId',
                  right_on='Indicator ID')

    areas = get_all_areas(proxy=proxy)

    df['GeographicalArea'] = df.apply(lambda x: areas[x['AreaTypeId']]['Name'],
                                      axis=1)

    df.rename(columns={'Descriptive_Name': 'IndicatorName'},
              inplace=True)
    df = df[['IndicatorId', 'IndicatorName', 'GeographicalArea', 'AreaTypeId']]

    return df


def get_data_for_indicator_at_all_available_geographies(indicator_id,
                                                        proxy=None):
    """
    Returns a dataframe of all data for an indicator for all available geographies.

    :param indicator_id: Indicator id
    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe of data for indicator for all available areas for all time periods
    """
    all_area_for_all_indicators = get_all_areas_for_all_indicators(proxy)
    areas_for_indicator = all_area_for_all_indicators[
        all_area_for_all_indicators['IndicatorId'] == indicator_id]
    areas_to_get = areas_for_indicator['AreaTypeId'].unique()

    ls_of_dfs = []
    for area in areas_to_get:
        tmp_df = get_data_by_indicator_ids(indicator_id, area, proxy=proxy)
        ls_of_dfs.append(tmp_df)

    ret_df = pd.concat(ls_of_dfs)

    return ret_df.drop_duplicates()
