import pandas as pd
import pytest
from ..api_calls import get_json, get_data_in_tuple, make_request, get_json_return_df, base_url
from ..retrieve_data import get_all_data_for_profile, get_all_data_for_indicators, get_data_by_indicator_ids, \
    get_all_areas_for_all_indicators, get_data_for_indicator_at_all_available_geographies
from ..metadata import get_metadata_for_profile_as_dataframe, get_metadata, get_metadata_for_indicator_as_dataframe, \
    get_metadata_for_domain_as_dataframe, get_all_value_notes, get_profile_by_name, get_area_types_for_profile, \
    get_domains_in_profile, get_all_profiles, get_area_types_as_dict, get_age_from_id, get_area_type_ids_for_profile, \
    get_profile_by_id, get_age_id, get_all_ages, get_all_sexes, get_areas_for_area_type, get_metadata_for_indicator, \
    get_multiplier_and_calculation_for_indicator, get_sex_from_id, get_sex_id, get_value_note_id, \
    get_metadata_for_all_indicators, get_metadata_for_all_indicators_from_csv, get_all_areas, get_profile_by_key
from ..area_data import deprivation_decile


def test_get_json():
    data = get_json('https://jsonplaceholder.typicode.com/todos/1')
    assert data['userId'] == 1
    assert isinstance(data, dict)


def test_get_data_in_tuple():
    data = get_data_in_tuple(base_url + 'ages')
    assert type(data[1]) == tuple


def test_make_request():
    data = make_request(base_url + 'area_types', 'Id')
    assert type(data) == dict
    assert data[15]['Name'] == 'England'


def test_get_json_return_df():
    data = get_json_return_df('https://jsonplaceholder.typicode.com/todos/1')
    assert isinstance(data, pd.DataFrame) is True


# need to think about this one
def test_get_all_data_for_profile():
    data = get_all_data_for_profile(84, is_test=True)
    assert isinstance(data[0], pd.DataFrame) is True
    assert data[1] == base_url + 'all_data/csv/by_profile_id?child_area_type_id=154&parent_area_type_id=15&profile_id=84'
    assert data[0].shape[1] == 26


def test_get_all_areas():
    test_dict, url = get_all_areas(is_test=True)
    first_dict = test_dict.get(next(iter(test_dict)))
    assert isinstance(test_dict, dict) is True
    assert isinstance(first_dict, dict) is True
    assert isinstance(first_dict.get('Name'), str) is True
    assert url == 'http://fingertips.phe.org.uk/api/area_types'


def test_get_all_data_for_indicators():
    data, url = get_all_data_for_indicators([92949, 92998], area_type_id=102, is_test=True)
    assert isinstance(data, pd.DataFrame) is True
    assert data.shape[1] == 27
    assert url == 'http://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=92949,92998&child_area_type_id=102&parent_area_type_id=15'


def test_get_data_by_indicator_ids():
    data, url = get_data_by_indicator_ids([92949, 92998], 102, is_test=True)
    assert isinstance(data, pd.DataFrame) is True
    assert data.shape[1] == 27
    assert url == 'http://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=92949,92998&child_area_type_id=102&parent_area_type_id=15'


def test_get_all_areas_for_all_indicators():
    test_dict = get_all_areas_for_all_indicators()
    first_list = test_dict.get(next(iter(test_dict)))
    assert isinstance(data, dict) is True
    assert 15 in first_list


def test_get_data_for_indicator_at_all_available_geographies():
    data = get_data_for_indicator_at_all_available_geographies(92998)
    assert isinstance(data, pd.DataFrame) is True
    assert data.shape[1] == 27


def test_get_metadata_for_profile_as_dataframe():
    data = get_metadata_for_profile_as_dataframe(84)
    assert isinstance(data, pd.DataFrame) is True
    assert data.shape[1] == 30


def test_get_metadata():
    data_indicators = get_metadata(indicator_ids=[92949, 90581])
    data_domain = get_metadata(domain_ids=[1938133052, 1938132811])
    data_profile = get_metadata(profile_ids=84)
    data_indicators_and_domain = get_metadata(indicator_ids=[92949, 90581], domain_ids=[1938133052, 1938132811])
    data_domain_and_profile = get_metadata(domain_ids=[1938133052, 1938132811], profile_ids=84)
    #data_profile_and_indicators = get_metadata(indicator_ids=[92949, 90581], profile_ids=84) ####!
    data_all = get_metadata(indicator_ids=[92949, 90581], domain_ids=[1938133052, 1938132811], profile_ids=84)
    assert isinstance(data_indicators, pd.DataFrame) is True
    assert data_indicators.shape[1] == 32
    assert isinstance(data_domain, pd.DataFrame) is True
    assert data_domain.shape[1] == 32
    assert isinstance(data_profile, pd.DataFrame) is True
    assert data_profile.shape[1] == 32
    assert isinstance(data_indicators_and_domain, pd.DataFrame) is True
    assert data_indicators_and_domain.shape[1] == 32
    assert isinstance(data_domain_and_profile, pd.DataFrame) is True
    assert data_domain_and_profile.shape[1] == 32
    assert isinstance(data_profile_and_indicators, pd.DataFrame) is True
    assert data_profile_and_indicators.shape[1] == 32
    assert isinstance(data_all, pd.DataFrame) is True
    assert data_all.shape[1] == 32


def test_get_metadata_for_indicator_as_dataframe():
    data = get_metadata_for_indicator_as_dataframe(247, is_test=True)
    assert isinstance(data[0], pd.DataFrame) is True
    assert data[0].shape[1] == 30
    assert data[1] == 'http://fingertips.phe.org.uk/api/indicator_metadata/csv/by_indicator_id?indicator_ids=247'


def test_get_metadata_for_domain_as_dataframe():
    data = get_metadata_for_domain_as_dataframe(1938132811, is_test=True)
    assert isinstance(data[0], pd.DataFrame) is True
    assert data[0].shape[1] == 30
    assert data[1] == 'http://fingertips.phe.org.uk/api/indicator_metadata/csv/by_group_id?group_id=1938132811'


def test_get_all_value_notes():
    test_dict = get_all_value_notes()
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(data, dict) is True
    assert isinstance(first_item, str) is True


def test_get_profile_by_name():
    data = get_profile_by_name('dementia')
    assert isinstance(data, dict) is True
    assert data['Id'] == 84


def test_get_profile_by_key():
    data = get_profile_by_key("general-practice")
    assert isinstance(data, dict) is True
    assert data['Id'] == 20


def test_get_area_types_for_profile():
    test_dict = get_area_types_for_profile(84)
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(data, dict) is True
    assert isinstance(first_item, dict) is True


def test_get_domains_in_profile():
    test_dict = get_domains_in_profile(84)
    assert isinstance(data, dict) is True


def test_get_all_profiles():
    test_dict = get_all_profiles()
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(data, dict) is True
    assert isinstance(first_item, dict) is True


def test_get_area_types_as_dict():
    test_dict = get_area_types_as_dict()
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(data, dict) is True
    assert isinstance(first_item, dict) is True


def test_get_age_from_id():
    data = get_age_from_id(1)
    assert data == 'All ages'


def test_get_area_type_ids_for_profile():
    data = get_area_type_ids_for_profile(84)
    assert isinstance(data, list) is True
    assert isinstance(data[1], int) is True


def test_get_profile_by_id():
    data = get_profile_by_id(84)
    assert isinstance(data, dict) is True


def test_get_age_id():
    data = get_age_id('All ages')
    assert data == 1


def test_get_all_ages():
    test_dict = get_all_ages()
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(data, dict) is True
    assert isinstance(first_item, dict) is True


def test_get_all_sexes():
    test_dict = get_all_sexes()
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(test_dict, dict) is True
    assert isinstance(first_item, str) is True


def test_get_areas_for_area_type():
    data = get_areas_for_area_type(102)
    assert isinstance(data, dict) is True
    assert isinstance(list(data.values())[0], dict) is True


def test_get_metadata_for_indicator():
    data = get_metadata_for_indicator(247)
    assert isinstance(data, dict) is True


def test_get_multiplier_and_calculation_for_indicator():
    data = get_multiplier_and_calculation_for_indicator(247)
    assert isinstance(data, tuple) is True
    assert data[0] == 100


def test_get_sex_from_id():
    data = get_sex_from_id(1)
    assert data == 'Male'


def test_get_sex_id():
    data = get_sex_id('Male')
    assert data == 1


def test_get_value_note_id():
    data = get_value_note_id('Value suppressed for disclosure control due to small count')
    assert data == 101


def test_get_metadata_for_all_indicators():
    test_dict = get_metadata_for_all_indicators()
    first_item = test_dict.get(next(iter(test_dict)))
    assert isinstance(test_dict, dict) is True
    assert len(first_item.keys()) == 15


def test_get_metadata_for_all_indicators_from_csv():
    data = get_metadata_for_all_indicators_from_csv()
    assert isinstance(data, pd.DataFrame) is True
    assert data.shape[1] == 30


def test_deprivation_decile():
    data = deprivation_decile(7)
    assert len(data.unique()) == 10
