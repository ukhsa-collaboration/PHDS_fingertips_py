"""
api_calls.py
==================================
A group of functions to query the Fingertips api and retrieve data in a variety of formats.
"""

import requests
import json
import pandas as pd
from io import StringIO
import urllib


def make_request(url, attr=None, proxy=None):
    """
    :param url: A url to make a request
    :param attr: The attribute that needs to be returned
    :param proxy: proxy given to the get request used to access the API
    :return: a dict of the attribute and associated data
    """
    try:
        req = requests.get(url, proxies=proxy)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False, proxies=proxy)
    json_response = json.loads(req.content.decode('utf-8'))
    data = {}
    for item in json_response:
        name = item.pop(attr)
        data[name] = item
    return data


def get_json(url, proxy=None):
    """
    :param url: A url to make a request
    :param proxy: proxy given to the get request used to access the API
    :return: A parsed JSON object
    """
    try:
        req = requests.get(url, proxies=proxy)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False, proxies=proxy)
    json_resp = json.loads(req.content.decode('utf-8'))
    return json_resp


def get_json_return_df(url, transpose=True, proxy=None):
    """
    :param url: A url to make a request
    :param transpose: transposes dataframe.
    :param proxy: proxy given to the get request used to access the API
    :return: Dataframe generated from JSON response.
    """
    try:
        req = requests.get(url, proxies=proxy)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False, proxies=proxy)
    try:
        df = pd.DataFrame.from_dict(req.json())
    except ValueError:
        df = pd.DataFrame.from_dict([req.json()])
    if transpose:
        df = df.transpose()
    return df


def get_data_in_tuple(url, proxy=None):
    """
    :param url: A url to make a request
    :param proxy: proxy given to the get request used to access the API
    :return: A tuple of returned data
    """
    try:
        req = requests.get(url, proxies=proxy)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False, proxies=proxy)
    json_resp = json.loads(req.content.decode('utf-8'))
    tup = [tuple(d.values()) for d in json_resp]
    if isinstance(tup[0][0], str):
        return [(t[1], t[0]) for t in tup]
    else:
        return tup


def get_csv(url, proxy=None):
    """
    :param url: A url to make a request
    :param proxy: proxy given to the get request used to access the API
    :return: A pandas df of the csv file
    """
    try:
        req = requests.get(url, proxies=proxy).text

    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False, proxies=proxy).text

    except urllib.error.HTTPError:
        raise Exception(
            'There has been a server error with Fingertips for this request.')

    return pd.read_csv(StringIO(req), low_memory=False)


def deal_with_url_error(url, proxy=None):
    """
    :param url: A url that returns a URL Error based on SSL errors
    :param proxy: proxy given to the get request used to access the API
    :return: A dataframe from the URL with verify set to false.
    """
    req = requests.get(url, verify=False, proxies=proxy)
    s = str(req.content, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)
    return df


base_url = 'http://fingertips.phe.org.uk/api/'
