"""
retrieve_data.py
==================================
A group of functions to retrieve data from Fingertips by indicator, profile, domain (group), or geography.
"""


import pandas as pd
from urllib.error import URLError, HTTPError
from .api_calls import base_url, deal_with_url_error, get_json
from .metadata import get_area_type_ids_for_profile, get_metadata_for_all_indicators, get_all_areas


def get_data_by_indicator_ids(indicator_ids, area_type_id, parent_area_type_id=15, profile_id=None,
                              include_sortable_time_periods=None, is_test=False):
    """
    Returns a dataframe of indicator data given a list of indicators and area types.
    :param indicator_ids: Single indicator ID or list of indicator IDs, as integers or strings
    :param area_type_id: ID of area type (eg. CCG, Upper Tier Local Authority) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param profile_id: ID of profile to select by as either int or string
    :param include_sortable_time_periods: Boolean as to whether to include a sort-friendly data field
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dataframe of data relating to the given indicators
    """

    url_suffix = 'all_data/csv/by_indicator_id?indicator_ids={}&child_area_type_id={}&parent_area_type_id={}'
    if profile_id and not include_sortable_time_periods:
        url_addition = f'&profile_id={profile_id}'
        url_suffix = url_suffix + url_addition
    elif include_sortable_time_periods and not profile_id:
        url_addition = '&include_sortable_time_periods=yes'
        url_suffix = url_suffix + url_addition
    elif profile_id and include_sortable_time_periods:
        url_addition = f'&profile_id={profile_id}&include_sortable_time_periods=yes'
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


def get_all_data_for_profile(profile_id, parent_area_type_id=15, area_type_id = None, filter_by_area_codes=None,
                             is_test=False):
    """
    Returns a dataframe of data for all indicators within a profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param area_type_id: Option to only return data for a given area type. Area type ids are string, int or a list.
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings.
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dataframe of data for all indicators within a profile with any filters applied
    """
    if area_type_id is not None:
        if type(area_type_id) == int:
            area_types = [area_type_id]
        else:
            area_types = area_type_id
    else:
        area_types = get_area_type_ids_for_profile(profile_id)
    df = pd.DataFrame()
    for area in area_types:
        populated_url = f'all_data/csv/by_profile_id?child_area_type_id={area}\
            &parent_area_type_id={parent_area_type_id}&profile_id={profile_id}'
        try:
            df_returned = pd.read_csv(base_url + populated_url)
        except HTTPError:
            raise Exception('There has been a server error with Fingertips for this request. ')
        except URLError:
            df_returned = deal_with_url_error(base_url + populated_url)
        df = pd.concat([df, df_returned])
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

    :param indicators: List or integer or string of indicator IDs
    :param area_type_id: ID of area type (eg. ID of General Practice is 7 etc) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Dataframe of data for given indicators at an area
    """
    if isinstance(indicators, list):
        if any(isinstance(ind, int) for ind in indicators):
            indicators = ','.join(str(ind) for ind in indicators)
        else:
            indicators = ','.join(indicators)
    else:
        indicators = str(indicators)
        
    populated_url = f'all_data/csv/by_indicator_id?indicator_ids={indicators}&\
        child_area_type_id={area_type_id}&parent_area_type_id={parent_area_type_id}'
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
    Returns a dictionary of all indicators and their geographical breakdowns.

    :return: Dictionary of all indicators (ID as key) and their geographical breakdowns
    """
    url_suffix = 'available_data'
    all_area_ids = get_json(base_url + url_suffix)
    all_indicators = list(set([x.get('IndicatorId') for x in all_area_ids]))
    all_indicators.sort()
    area_dict = {}
    for ind in all_indicators:
        area_list = []
        for item in all_area_ids:
            if item.get('IndicatorId') == ind:
                area_list.append(item.get('AreaTypeId'))
        area_dict[ind] = area_list
    return area_dict
                

def get_data_for_indicator_at_all_available_geographies(indicator_id):
    """
    Returns a dataframe of all data for an indicator for all available geographies.

    :param indicator_id: Indicator id
    :return: Dataframe of data for indicator for all available areas for all time periods
    """
    all_area_for_all_indicators = get_all_areas_for_all_indicators()
    areas_to_get = all_area_for_all_indicators.get(indicator_id)
    df = pd.DataFrame()
    for area in areas_to_get:
        df_temp = get_data_by_indicator_ids(indicator_id, area)
        df = pd.concat([df, df_temp])
    df.drop_duplicates(inplace=True)
    return df
