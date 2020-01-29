"""
retrieve_data.py
==================================
A group of functions to retrieve data from Fingertips by indicator, profile, domain (group), or geography.
"""


import pandas as pd
from urllib.error import URLError, HTTPError
from .api_calls import base_url, get_json_return_df, deal_with_url_error
from .metadata import get_area_type_ids_for_profile, get_metadata_for_all_indicators, get_all_areas


def get_data_by_indicator_ids(indicator_ids, area_type_id, parent_area_type_id=15, profile_id=None,
                              include_sortable_time_periods=None, is_test=False):
    """
    Returns a dataframe of indicator data given a list of indicators and area types.

    :param indicator_ids: List of indicator IDs as strings
    :param area_type_id: ID of area type (eg. CCG, Upper Tier Local Authority) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param profile_id: ID of profile to select by as either int or string
    :param include_sortable_time_periods: Boolean as to whether to include a sort-friendly data field
    :return: A dataframe of data relating to the given indicators
    """

    url_suffix = 'all_data/csv/by_indicator_id?indicator_ids={}&child_area_type_id={}&parent_area_type_id={}'
    if profile_id and not include_sortable_time_periods:
        url_addition = '&profile_id={}'.format(str(profile_id))
        url_suffix = url_suffix + url_addition
    elif include_sortable_time_periods and not profile_id:
        url_addition = '&include_sortable_time_periods=yes'
        url_suffix = url_suffix + url_addition
    elif profile_id and include_sortable_time_periods:
        url_addition = '&profile_id={}&include_sortable_time_periods=yes'.format(str(profile_id))
        url_suffix = url_suffix + url_addition
    if isinstance(indicator_ids, list):
        if any(isinstance(ind, int) for ind in indicator_ids):
            indicator_ids = ','.join(str(ind) for ind in indicator_ids)
        else:
            indicator_ids = ','.join(indicator_ids)
    else:
        indicator_ids = str(indicator_ids)
    populated_url = url_suffix.format(indicator_ids, str(area_type_id), parent_area_type_id)
    try:
        df = pd.read_csv(base_url + populated_url)
    except URLError:
        df = deal_with_url_error(base_url + populated_url)
    if is_test:
        return df, base_url + populated_url
    return df


def get_all_data_for_profile(profile_id, parent_area_type_id=15, area_type_id=None, filter_by_area_codes=None,
                             is_test=False):
    """
    Returns a dataframe of data for all indicators within a profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param area_type_id: Option to only return data for a given area type. Area type ids are string, int or a list.
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings.
    :return: A dataframe of data for all indicators within a profile with any filters applied
    """
    if area_type_id:
        area_types = area_type_id
    else:
        area_types = get_area_type_ids_for_profile(profile_id)
    url_suffix = 'all_data/csv/by_profile_id?child_area_type_id={}&parent_area_type_id={}&profile_id={}'
    df = pd.DataFrame()
    for area in area_types:
        populated_url = url_suffix.format(area, parent_area_type_id, profile_id)
        try:
            df_returned = pd.read_csv(base_url + populated_url)
        except HTTPError:
            raise Exception('There has been a server error with Fingertips for this request. ')
        except URLError:
            df_returned = deal_with_url_error(base_url + populated_url)
        df = df.append(df_returned)
    if filter_by_area_codes:
        if isinstance(filter_by_area_codes, list):
            df = df.loc[df['Area Code'].isin(filter_by_area_codes)]
        elif isinstance(filter_by_area_codes, str):
            df = df.loc[df['Area Code'] == filter_by_area_codes]
        df = df.reset_index()
    if is_test:
        return df, base_url + populated_url
    return df


def get_all_data_for_indicators(indicators, area_type_id, parent_area_type_id=15, filter_by_area_codes=None,
                                is_test=False):
    """
    Returns a dataframe of data for given indicators at an area.

    :param indicators: List or integer or string of indicator Ids
    :param area_type_id: ID of area type (eg. ID of General Practice is 7 etc) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings
    :return: Dataframe of data for given indicators at an area
    """
    url_suffix = 'all_data/csv/by_indicator_id?indicator_ids={}&child_area_type_id={}&parent_area_type_id={}'
    if isinstance(indicators, list):
        if any(isinstance(ind, int) for ind in indicators):
            indicators = ','.join(str(ind) for ind in indicators)
        else:
            indicators = ','.join(indicators)
    else:
        indicators = str(indicators)
    populated_url = url_suffix.format(indicators, str(area_type_id), str(parent_area_type_id))
    try:
        df = pd.read_csv(base_url + populated_url)
    except URLError:
        df = deal_with_url_error(base_url + populated_url)
    df.reset_index()
    if filter_by_area_codes:
        if isinstance(filter_by_area_codes, list):
            df = df.loc[df['Area Code'].isin(filter_by_area_codes)]
        elif isinstance(filter_by_area_codes, str):
            df = df.loc[df['Area Code'] == filter_by_area_codes]
        df = df.reset_index()
    if is_test:
        return df, base_url + populated_url
    return df


def get_all_areas_for_all_indicators():
    """
    Returns a dataframe of all indicators and their geographical breakdowns.

    :return: Dataframe of all indicators and their geographical breakdowns
    """
    url_suffix = 'available_data'
    df = get_json_return_df(base_url + url_suffix, transpose=False)
    indicator_metadata = get_metadata_for_all_indicators()
    df = pd.merge(df, indicator_metadata[['Descriptive']], left_on='IndicatorId', right_index=True)
    df['IndicatorName'] = df.apply(lambda x: x['Descriptive']['Name'], axis=1)
    areas = get_all_areas()
    df['GeographicalArea'] = df.apply(lambda x: areas[x['AreaTypeId']]['Name'], axis=1)
    df = df[['IndicatorId', 'IndicatorName', 'GeographicalArea', 'AreaTypeId']]
    return df


def get_data_for_indicator_at_all_available_geographies(indicator_id):
    """
    Returns a dataframe of all data for an indicator for all available geographies.

    :param indicator_id: Indicator id
    :return: Dataframe of data for indicator for all available areas for all time periods
    """
    all_area_for_all_indicators = get_all_areas_for_all_indicators()
    areas_for_indicator = all_area_for_all_indicators[all_area_for_all_indicators['IndicatorId'] == indicator_id]
    areas_to_get = areas_for_indicator['AreaTypeId'].unique()
    df = pd.DataFrame()
    for area in areas_to_get:
        df_temp = get_data_by_indicator_ids(indicator_id, area)
        df = df.append(df_temp)
    df.drop_duplicates(inplace=True)
    return df
