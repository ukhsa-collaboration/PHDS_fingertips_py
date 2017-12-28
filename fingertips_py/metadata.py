import pandas as pd
from api_calls import get_data_in_tuple, base_url, make_request, get_json
from urllib.error import HTTPError


def get_all_ages():
    """
    Returns a dictionary of all the age categories and their IDs
    :return: Age codes used in fingertips in a tuple
    """
    ages = get_data_in_tuple(base_url + 'ages')
    return ages


def get_age_id(age):
    """
    Returns an ID for a given age
    :param age: Search term of an age or age range as a string
    :return: Code used in fingertips to represent the age or age range as a string
    """
    ages = make_request(base_url + 'ages', 'Name')
    return ages[age]['Id']


def get_age_from_id(age_id):
    """
    Returns a age name from given id
    :param age_id: Age id used in fingertips as an integer
    :return: Age or age range as a string
    """
    ages = make_request(base_url + 'ages', 'Id')
    return ages[age_id]['Name']


def get_all_sexes():
    """
    Returns a tuple of all sex categories and their IDs
    :return: Sex categories used in fingertips with associated codes as a tuple
    """
    sexes = get_data_in_tuple(base_url + 'sexes')
    return sexes


def get_sex_id(sex):
    """
    Returns an ID for a given sex
    :param sex: Sex category as string (Case sensitive)
    :return: ID used in fingertips to represent the sex as integer
    """
    sexes = make_request(base_url + 'sexes', 'Name')
    return sexes[sex]['Id']


def get_sex_from_id(sex_id):
    """
    Returns a sex name given an id
    :param sex_id: ID used in fingertips to represent the sex as integer
    :return: Sex category as string
    """
    sexes = make_request(base_url + 'sexes', 'Id')
    return sexes[sex_id]['Name']


def get_all_value_notes():
    """
    Returns a dictionary of all value notes and their IDs
    :return: Data value notes and their associated codes that are used in Fingertips as a list of tuples
    """
    value_notes = get_data_in_tuple(base_url + 'value_notes')
    return value_notes


def get_value_note_id(value_note):
    """
    Returns a value note ID for a given value note
    :param value_note: Value note as string
    :return: ID used in fingertips to represent the value note as integer
    """
    value_notes = make_request(base_url + 'value_notes', 'Text')
    return value_notes[value_note]['Id']


def get_areas_for_area_type(area_type_id):
    """
    Returns a dictionary of areas that match an area type id given the id as integer or string
    :param area_type_id: ID of area type (eg. CCG, Upper Tier Local Authority) used in Fingertips as integer or string
    :return: A dictionary of dictionaries with area codes and the names of those areas
    """
    areas = make_request(base_url + 'areas/by_area_type?area_type_id=' + str(area_type_id), 'Code')
    return areas


def get_metatdata_for_indicator(indicator_number):
    """
    Returns the metadata for an indicator given the indicator number as integer or string
    :param indicator_number: Number used to identify an indicator within Fingertips as integer or string
    :return: A dictionary of metadata for the given indicator
    """
    metadata = get_json(base_url + 'indicator_metadata/by_indicator_id?indicator_ids=' + str(indicator_number))
    return metadata


def get_rate_and_calculation_for_indicator(indicator_number):
    """
    Returns the rata and calculation method for a given indicator
    :param indicator_number: Number used to identify an indicator within Fingertips as integer or string
    :return: A tuple of rate and calculation method from Fingetips metadata
    """
    metadata = get_metatdata_for_indicator(indicator_number)
    rate = metadata[str(indicator_number)]['Unit']['Value']
    calc_metadata = metadata[str(indicator_number)]['ConfidenceIntervalMethod']['Name']
    if 'wilson' in calc_metadata.lower():
        calc = 'Wilson'
    elif 'byar' in calc_metadata.lower():
        calc = 'Byar'
    else:
        calc = None
    return rate, calc


def get_area_types_as_dict():
    """
    Returns all area types and related information such as Id and name
    :return: A dictionary of area types
    """
    areas = get_json(base_url + 'area_types')
    return areas


def get_profile_by_id(profile_id):
    """
    Returns a profile as an dictionary which contains information about domains and sequencing
    :param profile_id: ID used in fingertips to identify a profile as integer or string
    :return: A dictionary of information about the profile
    """
    return get_json(base_url + 'profile?profile_id=' + str(profile_id))


def get_all_profiles():
    """
    Returns all profiles
    :return: A dictionary of all profiles in fingertips including information on domains and sequencing
    """
    profiles = get_json(base_url + 'profiles')
    return profiles


def get_domains_in_profile(profile_id):
    """
    Returns the domain IDs for a given profile
    :param profile_id: ID used in fingertips to identify a profile as integer or string
    :return: A list of domain IDs
    """
    profile = get_profile_by_id(profile_id)
    return profile['GroupIds']


def get_area_types_for_profile(profile_id):
    """
    Retrieves all the area types that have data for a given profile
    :param profile_id: ID used in fingertips to identify a profile as integer or string
    :return: A list of dictionaries of area types with relevant information
    """
    return get_json(base_url + 'area_types?profile_ids=' + str(profile_id))


def get_area_type_ids_for_profile(profile_id):
    """
    Returns a list of area types used within a given profile
    :param profile_id: ID used in fingertips to identify a profile as integer or string
    :return: A list of area types used within a given profile
    """
    area_type_obj = get_area_types_for_profile(profile_id)
    area_type_list = []
    for area_type in area_type_obj:
        area_type_list.append(area_type['Id'])
    return area_type_list


def get_profile_by_name(profile_name):
    """
    Returns a profile object given a name to search - try to be specific to get better results
    :param profile_name: A string or part of a string that is used as the profile name
    :return: A dictionary of the profile metadata including domain information or an error message
    """
    all_profiles = get_all_profiles()
    profile_obj = ''
    for profile in all_profiles:
        if profile_name.lower() in profile['Name'].lower():
            profile_obj = profile
    if not profile_obj:
        return 'Profile could not be found'
    else:
        return profile_obj


def get_metadata_for_indicator(indicator_ids):
    """
    Returns a dataframe of metadata for a given indicator ID or list of indicator IDs
    :param indicator_ids: Number or list of numbers used to identify an indicator within Fingertips as integer or string
    :return: Dataframe object with metadate for the indicator ID
    """
    url_suffix = "indicator_metadata/csv/by_indicator_id?indicator_ids={}"
    if isinstance(indicator_ids, list):
        indicator_ids = ','.join(list(map(str, indicator_ids)))
    try:
        df = pd.read_csv(base_url + url_suffix.format(str(indicator_ids)))
    except HTTPError:
        raise NameError('Indicator {} does not exist'.format(indicator_ids))
    return df


def get_metadata_for_domain(group_ids):
    """
    Returns a dataframe of metadata for a given domain ID or list of domain IDs
    :param group_ids: Number or list of numbers used to identify a domain within Fingertips as integer or string
    :return: Dataframe object with metadate for the indicators for a given domain ID
    """
    url_suffix = "indicator_metadata/csv/by_group_id?group_id={}"
    if isinstance(group_ids, list):
        df = pd.DataFrame()
        for group_id in group_ids:
            try:
                df = df.append(pd.read_csv(base_url + url_suffix.format(str(group_id))))
            except HTTPError:
                raise NameError('Domain {} does not exist'.format(group_id))
    else:
        try:
            df = pd.read_csv(base_url + url_suffix.format(str(group_ids)))
        except HTTPError:
            raise NameError('Domain {} does not exist'.format(group_ids))
    return df


def get_metadata_for_profile(profile_ids):
    """
    Returns a dataframe of metadata for a given profile ID or list of profile IDs
    :param profile_ids: ID or list of IDs used in fingertips to identify a profile as integer or string
    :return: Dataframe object with metadata for the indicators for a given group ID
    """
    url_suffix = "indicator_metadata/csv/by_profile_id?profile_id={}"
    if isinstance(profile_ids, list):
        df = pd.DataFrame()
        for profile_id in profile_ids:
            try:
                df = df.append(pd.read_csv(base_url + url_suffix.format(str(profile_id))))
            except HTTPError:
                raise NameError('Profile {} does not exist'.format(profile_id))
    else:
        try:
            df = pd.read_csv(base_url + url_suffix.format(str(profile_ids)))
        except HTTPError:
            raise NameError('Profile {} does not exist'.format(profile_ids))
    return df


def get_metadata(indicator_ids=None, domain_ids=None, profile_ids=None):
    """
    Returns a dataframe object of metadata for a given indicator, domain, and/or profile given the relevant IDs. At
    least one of these IDs has to be given otherwise an error is raised
    :param indicator_ids: [OPTIONAL] Number used to identify an indicator within Fingertips as integer or string
    :param domain_ids: [OPTIONAL] Number used to identify a domain within Fingertips as integer or string
    :param profile_ids: [OPTIONAL] ID used in fingertips to identify a profile as integer or string
    :return: A dataframe object with metadata for the given IDs or an error
    """
    if indicator_ids and domain_ids and profile_ids:
        df = get_metadata_for_profile(profile_ids)
        df = df.append(get_metadata_for_domain(domain_ids))
        df = df.append(get_metadata_for_indicator(indicator_ids))
        return df
    if indicator_ids and domain_ids:
        df = get_metadata_for_domain(domain_ids)
        df = df.append(get_metadata_for_indicator(indicator_ids))
        return df
    if indicator_ids and profile_ids:
        df = get_metadata_for_profile(profile_ids)
        df = df.append(get_metadata_for_indicator(indicator_ids))
        return df
    if domain_ids and profile_ids:
        df = get_metadata_for_profile(profile_ids)
        df = df.append(get_metadata_for_domain(domain_ids))
        return df
    if profile_ids:
        return get_metadata_for_profile(profile_ids)
    if domain_ids:
        return get_metadata_for_domain(domain_ids)
    if indicator_ids:
        return get_metadata_for_indicator(indicator_ids)
    raise NameError('Must use a valid indicator IDs, domain IDs or profile IDs')
