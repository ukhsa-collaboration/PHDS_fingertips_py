import requests
import json
from requests.structures import CaseInsensitiveDict


def make_request(url, attr=None):
    """
    :param url: A url to make a request
    :param attr: The attribute that needs to be returned
    :return: a dict of the attribute and associated data
    """
    req = requests.get(url)
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
    req = requests.get(url)
    json_resp = json.loads(req.content.decode('utf-8'))
    return json_resp


def get_data_in_tuple(url):
    """
    Returns a url response as a tuple
    """
    req = requests.get(url)
    json_resp = json.loads(req.content.decode('utf-8'))
    tup = [tuple(d.values()) for d in json_resp]
    if isinstance(tup[0][0], str):
        return [(t[1], t[0]) for t in tup]
    else:
        return tup


base_url = 'http://fingertips.phe.org.uk/api/'


