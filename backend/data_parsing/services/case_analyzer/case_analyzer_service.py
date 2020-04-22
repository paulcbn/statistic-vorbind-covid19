import datetime
import logging

from api_core.models import Case
from data_parsing.services.case_analyzer.extractors.age_extractor import extract_age
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
    'death_date': extract_death_date
}


def replace_and_log_value(case, field, value, force_overwrite=False):
    old_value = getattr(case, field)

    logger.info(f'Found value "{value}" for field "{field}". Old value: "{old_value}"')
    if old_value is None:
        setattr(case, field, value)
        logger.info(f'Set value "{value}" for field "{field}"')

    elif old_value != value and force_overwrite:
        setattr(case, field, value)
        logger.warning(f'Replaced "{old_value}" for field "{field}" with "{value}"')

    elif old_value != value:
        logger.warning(
            f'Values differ and force_overwrite = False. No replacing is done. This may require manual intervention for case {case}'
        )

    else:
        logger.info("No change in value found.")


def analyze_case(case, force_overwrite=False):
    logger.info(f'Starting to analyze case: {case}')

    changed = False
    for field, extract_func in FIELD_EXTRACTORS.items():
        value = extract_func(case.parsed_text)
        if value is None:
            logger.warning(f'Could not extract "{field}" from case "{case}".')
        else:
            changed = True

        replace_and_log_value(case, field, value, force_overwrite)

    if changed:
        case.save()


def get_queryset(today, source):
    queryset = Case.objects.all()

    if today:
        queryset = queryset.filter(date_created__date=datetime.date.today())

    if source:
        queryset = queryset.filter(source__id=source)

    return queryset


def analyze_all_cases(force_overwrite=False, today=None, source=None):
    logger.info(f'Starting to analyze all cases (force_overwrite={force_overwrite})')
    for case in get_queryset(today, source):
        analyze_case(case, force_overwrite=force_overwrite)
