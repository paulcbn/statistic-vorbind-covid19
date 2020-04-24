import datetime
import logging

from api_core.models import Case
from data_parsing.services.case_analyzer.extractors.age_extractor import extract_age
from data_parsing.services.case_analyzer.extractors.county_extractor import extract_county
from data_parsing.services.case_analyzer.extractors.date_extractors import extract_hospital_admission_date, \
    extract_test_date, extract_positive_result_date, extract_death_date
from data_parsing.services.case_analyzer.extractors.gender_extractor import extract_gender

logger = logging.getLogger(__name__)

FIELD_EXTRACTORS = {
    'age': extract_age,
    'gender': extract_gender,
    'hospital_admission_date': extract_hospital_admission_date,
    'test_date': extract_test_date,
    'positive_result_date': extract_positive_result_date,
    'death_date': extract_death_date,
    'county': extract_county
}


def replace_and_log_value(case, field, value, force_overwrite=False):
    """
    Compare the old value of the field with the new value.  Log de difference. Replace the value accordingly:
        - replace it anyways if the old value is None
        - replace it if it differs from the current value and 'force_overwrite=True'
        - ignore it if the value does not differ from the old one.
    :return True if a change was made on the case, False otherwise.
    """
    old_value = getattr(case, field)

    logger.info(f'Found value "{value}" for field "{field}". Old value: "{old_value}"')
    if old_value is None:
        setattr(case, field, value)
        logger.info(f'Set value "{value}" for field "{field}"')
        return True

    if old_value != value and force_overwrite:
        setattr(case, field, value)
        logger.warning(f'Replaced "{old_value}" for field "{field}" with "{value}"')
        return True

    if old_value != value:
        logger.warning(f"""Values differ and force_overwrite = False. No replacing is done.
        This may require manual intervention for case {case}""")
        return False

    logger.info("No change in value found.")
    return False


def analyze_case_for_one_field(case, field, force_overwrite=False):
    extract_func = FIELD_EXTRACTORS.get(field)
    value = extract_func(case.parsed_text)
    if value is None:
        logger.warning(f'Could not extract "{field}" from case "{case}".')

    if replace_and_log_value(case, field, value, force_overwrite):
        case.validated = False
        case.save()


def analyze_case_for_all_fields(case, force_overwrite=False):
    logger.info(f'Starting to analyze case: {case}')

    changed = False
    for field, extract_func in FIELD_EXTRACTORS.items():
        value = extract_func(case.parsed_text)
        if value is None:
            logger.warning(f'Could not extract "{field}" from case "{case}".')

        changed = changed or replace_and_log_value(case, field, value, force_overwrite)

    if changed:
        case.validated = False
        case.save()


def get_queryset(today, source):
    queryset = Case.objects.all()

    if today:
        queryset = queryset.filter(date_created__date=datetime.date.today())

    if source:
        queryset = queryset.filter(source__id=source)

    return queryset


def analyze_all_cases(force_overwrite=False, today=None, source=None, only_field=None):
    logger.info(f'Starting to analyze all cases (force_overwrite={force_overwrite})')

    for case in get_queryset(today, source):
        if only_field:
            analyze_case_for_one_field(case, field=only_field, force_overwrite=force_overwrite)
        else:
            analyze_case_for_all_fields(case, force_overwrite=force_overwrite)
