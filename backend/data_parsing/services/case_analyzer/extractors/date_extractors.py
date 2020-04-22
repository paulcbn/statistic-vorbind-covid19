import logging
import re
from datetime import datetime

from data_parsing.services.case_analyzer.regex_utils import first_match_after_anchor

logger = logging.getLogger(__name__)


def happy_flow_extractor(content, happy_flow_regex):
    match = happy_flow_regex.search(content)
    if match is None:
        return None

    day, month, year = map(int, match.groups())
    return datetime(year=year, month=month, day=day).date()


DATE_REGEX = re.compile(r'([0-9]{1,2})[.]([0-9]{1,2})[.]([0-9]{2,4})', re.I | re.M)


def emergency_flow_extractor(content, emergency_flow_allowed_keyword, emergency_flow_disallowed_keywords):
    match = first_match_after_anchor(
        content,
        anchor=emergency_flow_allowed_keyword,
        regex=DATE_REGEX,
        disallowed_in_between=emergency_flow_disallowed_keywords
    )
    if match is None:
        return None

    day, month, year = map(int, match.groups())
    return datetime(year=year, month=month, day=day).date()


TITLE_REGEX = re.compile(r'^\s*deces(?:\snr[.]?)?\s+[0-9]+', re.I | re.M)


def erase_title(content):
    match = TITLE_REGEX.search(content)
    if match is None:
        return content
    return content[match.end():]


def abstract_date_extractor(content, *,
                            happy_flow_regex,
                            emergency_flow_allowed_keyword,
                            emergency_flow_disallowed_keywords):
    content = erase_title(content)
    result = happy_flow_extractor(content, happy_flow_regex)
    if result is not None:
        return result

    result = emergency_flow_extractor(
        content,
        emergency_flow_allowed_keyword,
        emergency_flow_disallowed_keywords)
    if result is not None:
        return result


ADMITTED_KEYWORD_REGEX = re.compile(r'internat|interne|internare', re.I)
CONFIRMED_KEYWORD_REGEX = re.compile(r'confirm|pozitiv|rezultat', re.I)
TEST_KEYWORD_REGEX = re.compile(r'recolta', re.I)
DECEASED_KEYWORD_REGEX = re.compile(r'deces|deced', re.I)

HAPPY_FLOW_DEATH_DATE_REGEX = re.compile(
    r'data\W+decesului\W+([0-9]{1,2})[.\/\\-]([0-9]{1,2})[.\/\\-]([0-9]{2,4})', re.I)


def extract_death_date(content):
    return abstract_date_extractor(content,
                                   happy_flow_regex=HAPPY_FLOW_DEATH_DATE_REGEX,
                                   emergency_flow_allowed_keyword=DECEASED_KEYWORD_REGEX,
                                   emergency_flow_disallowed_keywords=[
                                       TEST_KEYWORD_REGEX,
                                       ADMITTED_KEYWORD_REGEX,
                                       CONFIRMED_KEYWORD_REGEX
                                   ])


HAPPY_FLOW_HOSPITAL_ADMISSION_REGEX = re.compile(
    r'data\W+(?:intern[aă]rii|internare)\W+([0-9]{1,2})[.\/\\-]([0-9]{1,2})[.\/\\-]([0-9]{2,4})', re.I)


def extract_hospital_admission_date(content):
    return abstract_date_extractor(content,
                                   happy_flow_regex=HAPPY_FLOW_HOSPITAL_ADMISSION_REGEX,
                                   emergency_flow_allowed_keyword=ADMITTED_KEYWORD_REGEX,
                                   emergency_flow_disallowed_keywords=[
                                       TEST_KEYWORD_REGEX,
                                       DECEASED_KEYWORD_REGEX,
                                       CONFIRMED_KEYWORD_REGEX
                                   ])


HAPPY_FLOW_POSITIVE_RESULT_REGEX = re.compile(
    r'data\W+confirm[aă]rii\W+([0-9]{1,2})[.\/\\-]([0-9]{1,2})[.\/\\-]([0-9]{2,4})', re.I)


def extract_positive_result_date(content):
    return abstract_date_extractor(content,
                                   happy_flow_regex=HAPPY_FLOW_POSITIVE_RESULT_REGEX,
                                   emergency_flow_allowed_keyword=CONFIRMED_KEYWORD_REGEX,
                                   emergency_flow_disallowed_keywords=[
                                       TEST_KEYWORD_REGEX,
                                       DECEASED_KEYWORD_REGEX,
                                       ADMITTED_KEYWORD_REGEX
                                   ])


HAPPY_FLOW_TEST_DATE_REGEX = re.compile(
     r'data\W+(?:recolt[aă]rii|testar[aă]rii)\W+([0-9]{1,2})[.\/\\-]([0-9]{1,2})[.\/\\-]([0-9]{2,4})', re.I)


def extract_test_date(content):
    return abstract_date_extractor(content,
                                   happy_flow_regex=HAPPY_FLOW_TEST_DATE_REGEX,
                                   emergency_flow_allowed_keyword=TEST_KEYWORD_REGEX,
                                   emergency_flow_disallowed_keywords=[
                                       CONFIRMED_KEYWORD_REGEX,
                                       DECEASED_KEYWORD_REGEX,
                                       ADMITTED_KEYWORD_REGEX
                                   ])
