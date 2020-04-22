import logging
import re

from api_core.models import Case

logger = logging.getLogger(__name__)

MALE_REGEX = re.compile(r'(?:b[aă]rbat)|(?:t[âa]n[ăa]r)', re.I | re.M)
FEMALE_REGEX = re.compile(r'(?:femeie)|(?:t[âa]n[ăa]r[aă])', re.I | re.M)


def extract_gender(content):
    male_match = MALE_REGEX.search(content)
    female_match = FEMALE_REGEX.search(content)

    if male_match is None and female_match is None:
        return None

    if male_match is None:
        return Case.FEMALE

    if female_match is None:
        return Case.MALE

    if female_match.start() < male_match.start():
        return Case.FEMALE

    return Case.MALE
