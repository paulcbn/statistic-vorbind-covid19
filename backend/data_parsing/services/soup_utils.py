from typing import Iterable, Iterator

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError


def get_soup_from_url(url: str) -> BeautifulSoup:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features='html.parser')

    except HTTPError as http_err:
        raise Exception(f'HTTP error occurred: {http_err}')
    except Exception as err:
        raise Exception(f'Other error occurred: {err}')

    return soup


def skip_first(sequence: Iterable) -> Iterator:
    iterator = iter(sequence)
    next(iterator)
    return iterator
