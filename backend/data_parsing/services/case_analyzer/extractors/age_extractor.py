import logging
import re

logger = logging.getLogger(__name__)

AGE_REGEX = re.compile(r'([0-9]+)\s+(?:de\s)?\s*ani', re.I)


def extract_age(content):
    age_match = AGE_REGEX.search(content)

    if age_match is None:
        return None

    try:
        age = int(age_match.group(1))
    except ValueError as exc:
        return None

    return age
