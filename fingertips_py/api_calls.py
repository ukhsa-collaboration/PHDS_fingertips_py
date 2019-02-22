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
    Returns a JSON object from url response
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    json_resp = json.loads(req.content.decode('utf-8'))
    return json_resp


def get_json_return_df(url, transpose=True):
    """
    Returns a transposed dataframe of a JSON response
    :param url: Url
    :return: dataframe
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    try:
        df = pd.read_json(req.content, encoding='utf-8')
    except ValueError:
        df = pd.DataFrame.from_dict([req.json()])
    if transpose:
        df = df.transpose()
    return df


def get_data_in_tuple(url):
    """
    Returns a url response as a tuple
    """
    try:
        req = requests.get(url)
    except requests.exceptions.SSLError:
        req = requests.get(url, verify=False)
    json_resp = json.loads(req.content.decode('utf-8'))
    tup = [tuple(d.values()) for d in json_resp]
    if isinstance(tup[0][0], str):
        return [(t[1], t[0]) for t in tup]
    else:
        return tup


def deal_with_url_error(url):
    req = requests.get(url, verify=False)
    s = str(req.content, 'utf-8')
    data = StringIO(s)
    df = pd.read_csv(data)
    return df


base_url = 'http://fingertips.phe.org.uk/api/'


