"""
metadata.py
==================================
Calls used to retrieve metadata about areas, ages, sexes, value notes, calculation methods, rates, and indicator
metadata.
"""

import pandas as pd
from urllib.error import HTTPError, URLError
from .api_calls import get_data_in_tuple, base_url, make_request, get_json, get_json_return_df, deal_with_url_error, get_data_in_dict


def get_all_ages(is_test=False):
    """
    Returns a dictionary of all the age categories and their IDs as the dictionary key.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Age codes used in Fingertips in a dictionary
    """
    ages = get_data_in_dict(base_url + 'ages')
    if is_test:
        return ages, base_url + 'ages'
    return ages


def get_all_areas(is_test=False):
    """
    Retreives all area types.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dictionary of all area types used in Fingertips
    """
    areas = make_request(base_url + 'area_types', 'Id')
    if is_test:
        return areas, base_url + 'area_types'
    return areas


def get_age_id(age, is_test=False):
    """
    Returns an ID for a given age.

    :param age: Search term of an age or age range as a string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Code used in Fingertips to represent the age as an integer or age range as a string
    """
    ages = make_request(base_url + 'ages', 'Name')
    if is_test:
        return ages[age]['Id'], base_url + 'ages'
    return ages[age]['Id']


def get_age_from_id(age_id, is_test=False):
    """
    Returns an age name from given id.

    :param age_id: Age id used in Fingertips as an integer
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Age, or age range, as a string
    """
    ages = make_request(base_url + 'ages', 'Id')
    if is_test:
        return ages[age_id]['Name'], base_url + 'ages'
    return ages[age_id]['Name']


def get_all_sexes(is_test=False):
    """
    Returns a dictionary of all sex categories and their IDs as dictionary key.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Sex categories used in Fingertips with associated codes as a dictionary
    """
    sexes = get_data_in_dict(base_url + 'sexes', value = 'Name')
    if is_test:
        return sexes, base_url + 'sexes'
    return sexes


def get_sex_id(sex, is_test=False):
    """
    Returns an ID for a given sex.

    :param sex: Sex category as string (Case sensitive)
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: ID used in Fingertips to represent the sex as an integer
    """
    sexes = make_request(base_url + 'sexes', 'Name')
    if is_test:
        return sexes[sex]['Id'], base_url + 'sexes'
    return sexes[sex]['Id']


def get_sex_from_id(sex_id, is_test=False):
    """
    Returns a sex name given an ID.

    :param sex_id: ID used in Fingertips to represent the sex as integer
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Sex category as string
    """
    sexes = make_request(base_url + 'sexes', 'Id')
    if is_test:
        return sexes[sex_id]['Name'], base_url + 'sexes'
    return sexes[sex_id]['Name']


def get_all_value_notes(is_test=False):
    """
    Returns a dictionary of all value notes and their IDs as dictionary key.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: Data value notes and their associated codes that are used in Fingertips as a dictionary
    """
    value_notes = get_data_in_dict(base_url + 'value_notes', value = 'Text')
    if is_test:
        return value_notes, base_url + 'value_notes'
    return value_notes


def get_value_note_id(value_note, is_test=False):
    """
    Returns a value note ID for a given value note.

    :param value_note: Value note as string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: ID used in Fingertips to represent the value note as an integer
    """
    value_notes = make_request(base_url + 'value_notes', 'Text')
    if is_test:
        return value_notes[value_note]['Id'], base_url + 'value_notes'
    return value_notes[value_note]['Id']


def get_areas_for_area_type(area_type_id, is_test=False):
    """
    Returns a dictionary of areas that match an area type id given the id as integer or string.

    :param area_type_id: ID of area type (ID of General Practice is 7 etc) used in Fingertips as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dictionary of dictionaries with area codes as the key 
    """
    areas = make_request(base_url + 'areas/by_area_type?area_type_id=' + str(area_type_id), 'Code')
    if is_test:
        return areas, base_url + 'areas/by_area_type?area_type_id=' + str(area_type_id)
    return areas


def get_metadata_for_indicator(indicator_number, is_test=False):
    """
    Returns the metadata for an indicator given the indicator number as integer or string.

    :param indicator_number: Number used to identify an indicator within Fingertips as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dictionary of metadata for the given indicator
    """
    metadata = get_json(base_url + 'indicator_metadata/by_indicator_id?indicator_ids=' + str(indicator_number))
    metadata_dict = metadata.get(str(indicator_number))
    if is_test:
        return metadata, base_url + 'indicator_metadata/by_indicator_id?indicator_ids=' + str(indicator_number)
    return metadata_dict


def get_metadata_for_all_indicators_from_csv(is_test=False):
    """
    Returns a dataframe from the csv of all metadata for all indicators.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dataframe of all metadata for all indicators
    """
    try:
        metadata = pd.read_csv(base_url + 'indicator_metadata/csv/all')
    except URLError:
        metadata = deal_with_url_error(base_url + 'indicator_metadata/csv/all')
    if is_test:
        return metadata, base_url + 'indicator_metadata/csv/all'
    return metadata


def get_metadata_for_all_indicators(include_definition='no', include_system_content='no', is_test=False):
    """
    Returns the metadata for all indicators in a dictionary.

    :param include_definition: optional to include definitions
    :param include_system_content: optional to include system content
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: dictionary of all indicators
    """
    url_suffix = f'indicator_metadata/all?include_definition={include_definition}&include_system_content={include_system_content}'
    metadata_dict = get_json(base_url + url_suffix)
    if is_test:
        return metadata_dict, base_url + url_suffix
    return metadata_dict


def get_multiplier_and_calculation_for_indicator(indicator_number):
    """
    Returns the multiplier and calculation method for a given indicator.

    :param indicator_number: Number used to identify an indicator within Fingertips as integer or string
    :return: A tuple of multiplier and calculation method from Fingetips metadata
    """
    metadata = get_metadata_for_indicator(indicator_number)
    multiplier = metadata.get('Unit').get('Value')
    calc_metadata = metadata.get('ConfidenceIntervalMethod').get('Name')
    if 'wilson' in calc_metadata.lower():
        calc = 'Wilson'
    elif 'byar' in calc_metadata.lower():
        calc = 'Byar'
    else:
        calc = None
    return multiplier, calc


def get_area_types_as_dict(is_test=False):
    """
    Returns all area types and related information such as ID and name with dictionary key value as ID.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dictionary of area types
    """
    areas = get_data_in_dict(base_url + 'area_types')
    if is_test:
        return areas, base_url + 'area_types'
    return areas


def get_profile_by_id(profile_id, is_test=False):
    """
    Returns a profile as an dictionary which contains information about domains and sequencing.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dictionary of information about the profile
    """
    if is_test:
        return get_json(base_url + 'profile?profile_id=' + str(profile_id)), base_url + 'profile?profile_id=' + \
               str(profile_id)
    return get_json(base_url + 'profile?profile_id=' + str(profile_id))


def get_all_profiles(is_test=False):
    """
    Returns all profiles.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A dictionary of all profiles in Fingertips including information on domains and sequencing
    """
    profiles = get_data_in_dict(base_url + 'profiles')
    if is_test:
        return profiles, base_url + 'profiles'
    return profiles


def get_domains_in_profile(profile_id):
    """
    Returns the domain IDs for a given profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :return: A list of domain IDs
    """
    profile = get_profile_by_id(profile_id)
    return profile['GroupIds']


def get_area_types_for_profile(profile_id, is_test=False):
    """
    Retrieves all the area types that have data for a given profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :return: A list of dictionaries of area types with relevant information
    """
    if is_test:
        return get_data_in_dict(base_url + 'area_types?profile_ids=' + str(profile_id)), base_url + 'area_types?profile_ids=' + \
               str(profile_id)
    return get_data_in_dict(base_url + 'area_types?profile_ids=' + str(profile_id))


def get_area_type_ids_for_profile(profile_id):
    """
    Returns a list of area types used within a given profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :return: A list of area type IDs used within a given profile
    """
    area_type_obj = get_area_types_for_profile(profile_id)
    area_type_list = [value.get('Id') for value in area_type_obj.values()]
    return area_type_list


def get_profile_by_name(profile_name):
    """
    Returns a profile object given a name to search – try to be specific to get better results.

    :param profile_name: A string or part of a string that is used as the profile name
    :return: A dictionary of the profile metadata including domain information or an error message
    """
    all_profiles = get_all_profiles()
    profile_obj = ''
    for profile in all_profiles.values():
        if profile_name.lower() in profile.get('Name').lower():
            profile_obj = profile
    if not profile_obj:
        return 'Profile could not be found'
    else:
        return profile_obj


def get_profile_by_key(profile_key):
    """
    Returns a profile object given a key (as the stub following 'profile' in the website URL). For example,
    give, a URL of the form `https://fingertips.phe.org.uk/profile/general-practice/data#page/3/gid/2000...`,
    the key is 'general-practice'.

    :param profile_key: The exact key for the profile.
    :return: A dictionary of the profile metadata including domain information or an error message
    """
    all_profiles = get_all_profiles()
    for profile_id, profile_object in all_profiles.items():
        if profile_object.get('Key') == profile_key:
            return profile_object
    return 'Profile could not be found'


def get_metadata_for_indicator_as_dataframe(indicator_ids, is_test=False):
    """
    Returns a dataframe of metadata for a given indicator ID or list of indicator IDs.

    :param indicator_ids: Number or list of numbers used to identify an indicator within Fingertips as integer or string
    :return: Dataframe object with metadate for the indicator ID
    """
    url_suffix = "indicator_metadata/csv/by_indicator_id?indicator_ids={}"
    if isinstance(indicator_ids, list):
        indicator_ids = ','.join(list(map(str, indicator_ids)))
    try:
        df = pd.read_csv(base_url + url_suffix.format(str(indicator_ids)))
    except HTTPError:
        raise NameError(f'Indicator {indicator_ids} does not exist')
    except URLError:
        df = deal_with_url_error(base_url + url_suffix.format(str(indicator_ids)))
    if is_test:
        return df, base_url + url_suffix.format(str(indicator_ids))
    return df


def get_metadata_for_domain_as_dataframe(group_ids, is_test=False):
    """
    Returns a dataframe of metadata for a given domain ID or list of domain IDs.

    :param group_ids: Number or list of numbers used to identify a domain within Fingertips as integer or string
    :return: Dataframe object with metadata for the indicators for a given domain ID
    """
    url_suffix = "indicator_metadata/csv/by_group_id?group_id={}"
    if isinstance(group_ids, list):
        df = pd.DataFrame()
        for group_id in group_ids:
            try:
                df = pd.concat([df, pd.read_csv(base_url + url_suffix.format(str(group_id)))])
            except HTTPError:
                raise NameError(f'Domain {group_id} does not exist')
            except URLError:
                df = deal_with_url_error(base_url + url_suffix.format(str(group_id)))
    else:
        try:
            df = pd.read_csv(base_url + url_suffix.format(str(group_ids)))
        except HTTPError:
            raise NameError(f'Domain {group_ids} does not exist')
        except URLError:
            df = deal_with_url_error(base_url + url_suffix.format(str(group_ids)))
    if is_test:
        return df, base_url + url_suffix.format(str(group_ids))
    return df


def get_metadata_for_profile_as_dataframe(profile_ids):
    """
    Returns a dataframe of metadata for a given profile ID or list of profile IDs.

    :param profile_ids: ID or list of IDs used in Fingertips to identify a profile as integer or string
    :return: Dataframe object with metadata for the indicators for a given group ID
    """
    url_suffix = "indicator_metadata/csv/by_profile_id?profile_id={}"
    if isinstance(profile_ids, list):
        df = pd.DataFrame()
        for profile_id in profile_ids:
            try:
                df = pd.concat([df, pd.read_csv(base_url + url_suffix.format(str(profile_id)))])
            except HTTPError:
                raise NameError(f'Profile {profile_id} does not exist')
            except URLError:
                df = deal_with_url_error(base_url + url_suffix.format(str(profile_id)))
    else:
        try:
            df = pd.read_csv(base_url + url_suffix.format(str(profile_ids)))
        except HTTPError:
            raise NameError(f'Profile {profile_ids} does not exist')
        except URLError:
            df = deal_with_url_error(base_url + url_suffix.format(str(profile_ids)))
    return df


def get_metadata(indicator_ids=None, domain_ids=None, profile_ids=None):
    """
    Returns a dataframe object of metadata for a given indicator, domain, and/or profile given the relevant IDs. At
    least one of these IDs has to be given otherwise an error is raised.

    :param indicator_ids: [OPTIONAL] Number used to identify an indicator within Fingertips as integer or string
    :param domain_ids: [OPTIONAL] Number used to identify a domain within Fingertips as integer or string
    :param profile_ids: [OPTIONAL] ID used in Fingertips to identify a profile as integer or string
    :return: A dataframe object with metadata for the given IDs or an error if nothing is specified
    """
    if indicator_ids and domain_ids and profile_ids:
        df = get_metadata_for_profile_as_dataframe(profile_ids)
        df = pd.concat([df, get_metadata_for_domain_as_dataframe(domain_ids)])
        df = pd.concat([df, get_metadata_for_indicator_as_dataframe(indicator_ids)])
        return df
    if indicator_ids and domain_ids:
        df = get_metadata_for_domain_as_dataframe(domain_ids)
        df = pd.concat([df, get_metadata_for_indicator_as_dataframe(indicator_ids)])
        return df
    if indicator_ids and profile_ids:
        df = get_metadata_for_profile_as_dataframe(profile_ids)
        df = pd.concat([df, get_metadata_for_profile_as_dataframe(indicator_ids)])
        return df
    if domain_ids and profile_ids:
        df = get_metadata_for_profile_as_dataframe(profile_ids)
        df = pd.concat([df, get_metadata_for_domain_as_dataframe(domain_ids)])
        return df
    if profile_ids:
        return get_metadata_for_profile_as_dataframe(profile_ids)
    if domain_ids:
        return get_metadata_for_domain_as_dataframe(domain_ids)
    if indicator_ids:
        return get_metadata_for_indicator_as_dataframe(indicator_ids)
    raise NameError('Must use a valid indicator IDs, domain IDs or profile IDs')
