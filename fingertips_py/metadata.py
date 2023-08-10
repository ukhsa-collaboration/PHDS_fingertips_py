"""
metadata.py
==================================
Calls used to retrieve metadata about areas, ages, sexes, value notes, 
calculation methods, rates, and indicator metadata.
"""

import pandas as pd
from urllib.error import HTTPError, URLError
from .api_calls import get_data_in_tuple, base_url, make_request, get_json, \
    get_json_return_df, get_csv, deal_with_url_error


def get_all_ages(is_test=False, proxy=None):
    """
    Returns a dictionary of all the age categories and their IDs.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Age codes used in Fingertips in a tuple
    """
    ages = get_data_in_tuple(base_url + 'ages', proxy)
    if is_test:
        return ages, base_url + 'ages'
    return ages


def get_all_areas(is_test=False, proxy=None):
    """
    Retrieves all area types.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dictionary of all area types used in Fingertips
    """
    areas = make_request(base_url + 'area_types', 'Id', proxy)
    if is_test:
        return areas, base_url + 'area_types'
    return areas


def get_age_id(age, is_test=False, proxy=None):
    """
    Returns an ID for a given age.

    :param age: Search term of an age or age range as a string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Code used in Fingertips to represent the age or age range as a string
    """
    ages = make_request(base_url + 'ages', 'Name', proxy)
    if is_test:
        return ages[age]['Id'], base_url + 'ages'
    return ages[age]['Id']


def get_age_from_id(age_id, is_test=False, proxy=None):
    """
    Returns an age name from given id.

    :param age_id: Age id used in Fingertips as an integer
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Age or age range as a string
    """
    ages = make_request(base_url + 'ages', 'Id', proxy)
    if is_test:
        return ages[age_id]['Name'], base_url + 'ages'
    return ages[age_id]['Name']


def get_all_sexes(is_test=False, proxy=None):
    """
    Returns a tuple of all sex categories and their IDs.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Sex categories used in Fingertips with associated codes as a tuple
    """
    sexes = get_data_in_tuple(base_url + 'sexes', proxy)
    if is_test:
        return sexes, base_url + 'sexes'
    return sexes


def get_sex_id(sex, is_test=False, proxy=None):
    """
    Returns an ID for a given sex.

    :param sex: Sex category as string (Case sensitive)
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: ID used in Fingertips to represent the sex as integer
    """
    sexes = make_request(base_url + 'sexes', 'Name', proxy)
    if is_test:
        return sexes[sex]['Id'], base_url + 'sexes'
    return sexes[sex]['Id']


def get_sex_from_id(sex_id, is_test=False, proxy=None):
    """
    Returns a sex name given an id.

    :param sex_id: ID used in Fingertips to represent the sex as integer
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Sex category as string
    """
    sexes = make_request(base_url + 'sexes', 'Id', proxy)
    if is_test:
        return sexes[sex_id]['Name'], base_url + 'sexes'
    return sexes[sex_id]['Name']


def get_all_value_notes(is_test=False, proxy=None):
    """
    Returns a dictionary of all value notes and their IDs.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Data value notes and their associated codes that are used in Fingertips as a list of tuples
    """
    value_notes = get_data_in_tuple(base_url + 'value_notes', proxy)
    if is_test:
        return value_notes, base_url + 'value_notes'
    return value_notes


def get_value_note_id(value_note, is_test=False, proxy=None):
    """
    Returns a value note ID for a given value note.

    :param value_note: Value note as string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: ID used in Fingertips to represent the value note as integer
    """
    value_notes = make_request(base_url + 'value_notes', 'Text', proxy)
    if is_test:
        return value_notes[value_note]['Id'], base_url + 'value_notes'
    return value_notes[value_note]['Id']


def get_areas_for_area_type(area_type_id, is_test=False, proxy=None):
    """
    Returns a dictionary of areas that match an area type id given the id as 
    integer or string.

    :param area_type_id: ID of area type (ID of General Practice is 7 etc) used in Fingertips as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dictionary of dictionaries with area codes and the names of those areas
    """
    areas = make_request(
        base_url + 'areas/by_area_type?area_type_id=' + str(area_type_id),
        'Code', proxy)
    if is_test:
        return areas, base_url + 'areas/by_area_type?area_type_id=' + str(area_type_id)
    return areas


def get_metadata_for_indicator(indicator_number, is_test=False, proxy=None):
    """
    Returns the metadata for an indicator given the indicator number as integer or string.

    :param indicator_number: Number used to identify an indicator within Fingertips as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dictionary of metadata for the given indicator
    """
    metadata = get_json(base_url +
                        'indicator_metadata/by_indicator_id?indicator_ids=' +
                        str(indicator_number), proxy)
    if is_test:
        return metadata, base_url + \
             'indicator_metadata/by_indicator_id?indicator_ids=' \
             + str(indicator_number)
    return metadata


def get_metadata_for_all_indicators_from_csv(is_test=False, proxy=None):
    """
    Returns a dataframe from the csv of all metadata for all indicators.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dataframe of all metadata for all indicators
    """
    try:
        metadata = get_csv(base_url + 'indicator_metadata/csv/all', proxy)

    except URLError:
        metadata = deal_with_url_error(
            base_url + 'indicator_metadata/csv/all', proxy)

    if is_test:
        return metadata, base_url + 'indicator_metadata/csv/all'
    return metadata


def get_metadata_for_all_indicators(include_definition=False,
                                    include_system_content=False,
                                    is_test=False, proxy=None):
    """
    Returns the metadata for all indicators in a dataframe.

    :param include_definition: optional to include definitions
    :param include_system_content: optional to include system content
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: dataframe of all indicators
    """
    url_suffix = "indicator_metadata/all?include_definition="

    if include_definition:
        url_suffix += "yes"
    else:
        url_suffix += "no"

    if include_system_content:
        url_suffix += "&include_system_content=yes"
    else:
        url_suffix += "&include_system_content=no"

    df = get_json_return_df(base_url + url_suffix, proxy)

    # Transpose to get the Indicator ID as a column
    df = df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Indicator ID'}, inplace=True)

    # Detect columns that contain any dictionaries
    dict_cols = []

    for col_name in df.columns:
        if any(df[col_name].apply(lambda x: isinstance(x, dict))):
            dict_cols.append(col_name)

    # Expand the dictionary columns of the metadata df
    expanded_dfs = []

    for col_name in dict_cols:

        # Extract the Dict column
        tmp_df = pd.json_normalize(df[col_name])

        # Change the new column names to be unique
        tmp_df = tmp_df.add_prefix(col_name + "_")

        expanded_dfs.append(tmp_df)

    # Remove the dictionary columns
    df.drop(dict_cols, axis=1, inplace=True)

    # Combine all the columns together
    df0 = pd.concat(expanded_dfs, axis=1)
    df = pd.concat([df, df0], axis=1)

    if is_test:
        return df, base_url + url_suffix
    return df


def get_multiplier_and_calculation_for_indicator(indicator_number, proxy=None):
    """
    Returns the multiplier and calculation method for a given indicator.

    :param indicator_number: Number used to identify an indicator within Fingertips as integer or string
    :param proxy: proxy info to access the data
    :return: A tuple of multiplier and calculation method from Fingertips metadata
    """
    metadata = get_metadata_for_indicator(indicator_number, proxy=proxy)
    multiplier = metadata[str(indicator_number)]['Unit']['Value']
    calc_metadata = metadata[str(indicator_number)]['ConfidenceIntervalMethod']['Name']
    if 'wilson' in calc_metadata.lower():
        calc = 'Wilson'
    elif 'byar' in calc_metadata.lower():
        calc = 'Byar'
    else:
        calc = None
    return multiplier, calc


def get_area_types_as_dict(is_test=False, proxy=None):
    """
    Returns all area types and related information such as ID and name.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy info to access the data
    :return: A dictionary of area types
    """
    areas = get_json(base_url + 'area_types', proxy)
    if is_test:
        return areas, base_url + 'area_types'
    return areas


def get_profile_by_id(profile_id, is_test=False, proxy=None):
    """
    Returns a profile as an dictionary which contains information about domains
    and sequencing.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A dictionary of information about the profile
    """

    tmp_url = base_url + 'profile?profile_id=' + str(profile_id)

    if is_test:
        return get_json(tmp_url, proxy), tmp_url

    return get_json(tmp_url, proxy)


def get_all_profiles(is_test=False, proxy=None):
    """
    Returns all profiles.

    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy info to access the data
    :return: A dictionary of all profiles in Fingertips including information on domains and sequencing
    """
    profiles = get_json(base_url + 'profiles', proxy)
    if is_test:
        return profiles, base_url + 'profiles'
    return profiles


def get_domains_in_profile(profile_id, proxy=None):
    """
    Returns the domain IDs for a given profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param proxy: proxy given to the get request used to access the API
    :return: A list of domain IDs
    """
    profile = get_profile_by_id(profile_id, proxy=proxy)
    return profile['GroupIds']


def get_area_types_for_profile(profile_id, is_test=False, proxy=None):
    """
    Retrieves all the area types that have data for a given profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: A list of dictionaries of area types with relevant information
    """

    tmp_url = base_url + 'area_types?profile_ids=' + str(profile_id)

    if is_test:
        return get_json(tmp_url, proxy), tmp_url

    return get_json(tmp_url, proxy)


def get_area_type_ids_for_profile(profile_id, proxy=None):
    """
    Returns a list of area types used within a given profile.

    :param profile_id: ID used in Fingertips to identify a profile as integer or string
    :param proxy: proxy given to the get request used to access the API
    :return: A list of area types used within a given profile
    """
    area_type_obj = get_area_types_for_profile(profile_id, proxy=proxy)
    area_type_list = []
    for area_type in area_type_obj:
        area_type_list.append(area_type['Id'])
    return area_type_list


def get_profile_by_name(profile_name, proxy=None):
    """
    Returns a profile object given a name to search - try to be specific to get
    better results.

    :param profile_name: A string or part of a string that is used as the profile name
    :param proxy: proxy given to the get request used to access the API
    :return: A dictionary of the profile metadata including domain information or an error message
    """
    all_profiles = get_all_profiles(proxy=proxy)
    profile_obj = ''
    for profile in all_profiles:
        if profile_name.lower() in profile['Name'].lower():
            profile_obj = profile
    if not profile_obj:
        return 'Profile could not be found'
    else:
        return profile_obj


def get_profile_by_key(profile_key, proxy=None):
    """
    Returns a profile object given a key (as the stub following 'profile' in the website URL). For example, give, a URL of the form `https://fingertips.phe.org.uk/profile/general-practice/data#page/3/gid/2000...`, the key is 'general-practice'.

    :param profile_key: The exact key for the profile.
    :param proxy: proxy given to the get request used to access the API
    :return: A dictionary of the profile metadata including domain information or an error message
    """
    all_profiles = get_all_profiles(proxy=proxy)
    for profile in all_profiles:
        if profile['Key'] == profile_key:
            return profile
    return 'Profile could not be found'


def get_metadata_for_indicator_as_dataframe(indicator_ids, is_test=False,
                                            proxy=None):
    """
    Returns a dataframe of metadata for a given indicator ID or list of indicator IDs.

    :param indicator_ids: Number or list of numbers used to identify an indicator within Fingertips as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe object with metadate for the indicator ID
    """

    if isinstance(indicator_ids, list):
        indicator_ids = ','.join(list(map(str, indicator_ids)))

    tmp_url = base_url + f"indicator_metadata/csv/by_indicator_id?" \
                         f"indicator_ids={indicator_ids}"
    try:
        df = get_csv(tmp_url, proxy)
    except HTTPError:
        raise NameError(f"Indicator {indicator_ids} does not exist")
    except URLError:
        df = deal_with_url_error(tmp_url, proxy)

    if is_test:
        return df, tmp_url
    return df


def get_metadata_for_domain_as_dataframe(group_ids, is_test=False, proxy=None):
    """
    Returns a dataframe of metadata for a given domain ID or list of domain 
    IDs.

    :param group_ids: Number or list of numbers used to identify a domain within Fingertips as integer or string
    :param is_test: Used for testing. Returns a tuple of expected return and the URL called to retrieve the data
    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe object with metadata for the indicators for a given domain ID
    """
    if not isinstance(group_ids, list):
        group_ids = [group_ids]

    list_of_df = []

    for group_id in group_ids:

        tmp_url = base_url + f"indicator_metadata/csv/by_group_id" \
                             f"?group_id={group_id}"
        try:
            list_of_df.append(get_csv(tmp_url, proxy))
        except HTTPError:
            raise NameError(f"Domain {group_id} does not exist")
        except URLError:
            list_of_df.append(deal_with_url_error(tmp_url, proxy))
    else:
        df = pd.concat(list_of_df)

    if is_test:
        return df, tmp_url
    return df


def get_metadata_for_profile_as_dataframe(profile_ids, proxy=None):
    """
    Returns a dataframe of metadata for a given profile ID or list of profile IDs.

    :param profile_ids: ID or list of IDs used in Fingertips to identify a profile as integer or string
    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe object with metadata for the indicators for a given group ID
    """
    url_suffix = "indicator_metadata/csv/by_profile_id?profile_id={}"

    if not isinstance(profile_ids, list):
        profile_ids = [profile_ids]

    list_of_df = []

    for profile_id in profile_ids:

        tmp_url = base_url + f"indicator_metadata/csv/by_profile_id" \
                             f"?profile_id={profile_id}"
        try:
            list_of_df.append(get_csv(tmp_url, proxy))
        except HTTPError:
            raise NameError(f"Profile {profile_id} does not exist")
        except URLError:
            list_of_df.append(deal_with_url_error((tmp_url, proxy)))

    return pd.concat(list_of_df)


def get_metadata(indicator_ids=None, domain_ids=None, profile_ids=None,
                 proxy=None):
    """
    Returns a dataframe object of metadata for a given indicator, domain, 
    and/or profile given the relevant IDs. At
    least one of these IDs has to be given otherwise an error is raised.

    :param indicator_ids: [OPTIONAL] Number used to identify an indicator within Fingertips as integer or string
    :param domain_ids: [OPTIONAL] Number used to identify a domain within Fingertips as integer or string
    :param profile_ids: [OPTIONAL] ID used in Fingertips to identify a profile as integer or string
    :param proxy: proxy given to the get request used to access the API
    :return: A dataframe object with metadata for the given IDs or an error if nothing is specified
    """

    # Works as long as there is no id that equals zero
    if not any([indicator_ids, domain_ids, profile_ids]):
        raise NameError(
            'Must use a valid indicator IDs, domain IDs or profile IDs')

    list_of_df = []

    if indicator_ids:
        list_of_df.append(get_metadata_for_indicator_as_dataframe(
            indicator_ids, proxy))

    if domain_ids:
        list_of_df.append(get_metadata_for_domain_as_dataframe(
            domain_ids, proxy))

    if profile_ids:
        list_of_df.append(get_metadata_for_profile_as_dataframe(
            profile_ids, proxy))

    return pd.concat(list_of_df)
