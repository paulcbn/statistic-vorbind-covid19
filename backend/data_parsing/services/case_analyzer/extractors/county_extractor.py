import logging
import re

from api_core.config.counties import Counties
from data_parsing.services.case_analyzer.regex_utils import first_match_after_anchor

logger = logging.getLogger(__name__)

replace_dict = {
    'ă': '[aă]',
    'â': '[aâ]',
    'î': '[iî]',
    'ș': '[sșş]',
    'ț': '[tțţ]',
    '-': '[- ]',
}


def generate_county_regex(county_name: str):
    pattern = county_name
    for letter, alternatives in replace_dict.items():
        pattern = pattern.replace(letter, alternatives)

    pattern = pattern.lower()
    return re.compile(fr'{pattern}\W', re.I | re.M)


def extract_county(content):
    result = None
    pos = len(content)

    for county_code, county_name in Counties.CHOICES:
        regex = generate_county_regex(county_name)
        match = regex.search(content)
        if match and match.start() < pos:
            result = county_code
            pos = match.start()

    return result
