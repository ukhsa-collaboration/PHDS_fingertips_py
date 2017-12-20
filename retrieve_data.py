import pandas as pd
from api_calls import base_url
from metadata import get_area_type_ids_for_profile


def get_data_by_indicator_ids(indicator_ids, area_type_id, parent_area_type_id=15):
    """
    Returns a dataframe of indicator data given a list of indicators and area types
    :param indicator_ids: List of indicator IDs as strings
    :param area_type_id: ID of area type (eg. CCG, Upper Tier Local Authority) used in Fingertips as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :return: A dataframe of data relating to the given indicators
    """
    url_suffix = 'all_data/csv/by_indicator_id?indicator_ids={}&child_area_type_id={}&parent_area_type_id={}'
    populated_url = url_suffix.format(indicator_ids, str(area_type_id), parent_area_type_id)
    df = pd.read_csv(base_url + populated_url)
    return df


def get_all_data_for_profile(profile_id, parent_area_type_id=15, filter_by_area_codes=None):
    """
    Returns a dataframe of data for all indicators within a profile
    :param profile_id: ID used in fingertips to identify a profile as integer or string
    :param parent_area_type_id: Area type of parent area - defaults to England value
    :param filter_by_area_codes: Option to limit returned data to areas. Areas as either string or list of strings.
    :return: A dataframe of data for all indicators within a profile with any filters applied
    """
    area_types = get_area_type_ids_for_profile(profile_id)
    url_suffix = 'all_data/csv/by_profile_id?child_area_type_id={}&parent_area_type_id={}&profile_id={}'
    df = pd.DataFrame()
    for area in area_types:
        populated_url = url_suffix.format(area, parent_area_type_id, profile_id)
        df_returned = pd.read_csv(base_url + populated_url)
        df = df.append(df_returned)
    if filter_by_area_codes:
        if isinstance(filter_by_area_codes, list):
            df = df.loc[df['Area Code'].isin(filter_by_area_codes)]
        elif isinstance(filter_by_area_codes, str):
            df = df.loc[df['Area Code'] == filter_by_area_codes]
        df = df.reset_index()
    return df
