
__version__ = '0.4.0'

from .api_calls import get_json, get_data_in_tuple, make_request
from .retrieve_data import get_all_data_for_profile, get_all_data_for_indicators, get_data_by_indicator_ids, \
    get_all_areas_for_all_indicators, get_data_for_indicator_at_all_available_geographies
from .metadata import get_metadata_for_profile_as_dataframe, get_metadata, get_metadata_for_indicator_as_dataframe, \
    get_metadata_for_domain_as_dataframe, get_all_value_notes, get_profile_by_name, get_area_types_for_profile,\
    get_domains_in_profile, get_all_profiles, get_area_types_as_dict, get_age_from_id, get_area_type_ids_for_profile, \
    get_profile_by_id, get_age_id, get_all_ages, get_all_sexes, get_areas_for_area_type, get_metadata_for_indicator, \
    get_multiplier_and_calculation_for_indicator, get_sex_from_id, get_sex_id, get_value_note_id, \
    get_metadata_for_all_indicators, get_metadata_for_all_indicators_from_csv, get_all_areas
from .area_data import deprivation_decile
