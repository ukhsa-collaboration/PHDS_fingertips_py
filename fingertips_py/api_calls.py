"""
api_calls.py
==================================
A group of functions to query the Fingertips api and retrieve data in a variety of formats.
"""


import requests
import json
import pandas as pd
from io import StringIO


def make_request(url, attr=None):
    """
    :param url: A url to make a request
    :param attr: The attribute that needs to be returned
    :return: a dict of the attribute and associated data
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    json_response = json.loads(req.content.decode('utf-8'))
    data = {}
    for item in json_response:
        name = item.pop(attr)
        data[name] = item
    return data


def get_json(url):
    """
    :param url: A url to make a request
    :return: A parsed JSON object
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    json_resp = json.loads(req.content.decode('utf-8'))
    return json_resp


def get_json_return_df(url, transpose=True):
    """
    :param url: A url to make a request
    :param transpose: [OPTIONAL] transposes dataframe. Default True.
    :return: Dataframe generated from JSON response.
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    try:
        df = pd.read_json(req.content, encoding='utf-8')
    except TypeError:
        df = pd.DataFrame.from_dict([req.json()])
    if transpose:
        df = df.transpose()
    return df


def get_data_in_tuple(url):
    """
    :param url: A url to make a request
    :return: A list of returned data in tuples
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    json_resp = json.loads(req.content.decode('utf-8'))
    tup_list = []
    for item in json_resp:
        tup_list.append([(k, v) for k, v in item.items()])
    if isinstance(tup_list[0][0], str):
        return [(t[1], t[0]) for t in tup_list]
    else:
        return tup_list
    
    
def get_data_in_dict(url, key = None, value = None):
    """
    :param url: A url to make a request
    :param key: The item in the JSON to be used as the dictionary key
    :param value: The item in the JSON to be used as the dictionary value
    :return: A dictionary of returned data using first item as dictionary key by default
    """
    json_list = get_json(url)
    if key is None:
        key = list(json_list[0].keys())[0]
    json_dict = {}
    if value is None:
        for js in json_list:
            json_dict[js.get(key)] = js
    else:
        for js in json_list:
            json_dict[js.get(key)] = js.get(value)
    return json_dict


def deal_with_url_error(url):
    """
    :param url: A url that returns a URL Error based on SSL errors
    :return: A dataframe from the URL with varify set to false.
    """
    req = requests.get(url, verify=False)
    s = str(req.content, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)
    return df


base_url = 'http://fingertips.phe.org.uk/api/'


