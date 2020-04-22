import logging
import re

from api_core.models import DataSource, Case

logger = logging.getLogger(__name__)

SEPARATOR_REGEX_DEFAULT = re.compile(r'((?<!dat[ăa] )deces\W*(?:nr)?\W*[0-9]+)', re.I)
SEPARATOR_REGEX_CASE_91_92 = re.compile(r'((?<!dat[ăa] )deces\W*(?:nr)?\W*[0-9]+)\s', re.I)
NUMBER_REGEX = re.compile(r'[0-9]+')

HARDCODED_REGEXES = {
    'https://stirioficiale.ro/informatii/informare-de-presa-1-aprilie-2020-ora-9-10pm': SEPARATOR_REGEX_CASE_91_92
}


def create_deaths_for_source(source):
    sep_regex = HARDCODED_REGEXES.get(source.url, SEPARATOR_REGEX_DEFAULT)

    split_content = re.split(sep_regex, source.parsed_content)

    partial_result = []
    string_count = len(split_content)

    for index in range(string_count):
        if SEPARATOR_REGEX_DEFAULT.match(split_content[index]):
            title = split_content[index]
            if index + 1 < string_count and not sep_regex.search(split_content[index + 1]):
                content = split_content[index + 1]
            else:
                content = ""

            death_parsed_text = title + "\n" + content
            patient_count = int(NUMBER_REGEX.search(title).group())

            partial_result.append((patient_count, death_parsed_text, source))

    if len(partial_result) == 0:
        numbers_in_title = NUMBER_REGEX.findall(source.title)
        if len(numbers_in_title) == 1:
            patient_count = int(numbers_in_title[0])
            death_parsed_text = source.title + '\n' + source.parsed_content

            partial_result.append((patient_count, death_parsed_text, source))

    for id, text, _ in partial_result:
        logger.info(f"ID:{id}")
        logger.info(f"TEXT:{text}")

    return partial_result


def create_deaths_from_data_sources():
    parsed_number_content_tuples = []
    for source in DataSource.objects.all():
        logger.info(f"-------------- Source: {source.pk} -------------- \n")
        parsed_number_content_tuples += create_deaths_for_source(source)

    case_dict = {}
    for case_number, case_description, case_source in parsed_number_content_tuples:
        if case_number not in case_dict.keys():
            case_dict[case_number] = [
                Case(
                    case_number=case_number,
                    collision_index=1,
                    parsed_text=case_description,
                    source=case_source
                )
            ]
        else:
            last_collision_index = case_dict[case_number][-1].collision_index
            case_dict[case_number].append(
                Case(
                    case_number=case_number,
                    collision_index=last_collision_index + 1,
                    parsed_text=case_description,
                    source=case_source
                )
            )

    for case_number, deaths_list in case_dict.items():
        for death in deaths_list:
            try:
                death.save()
            except Exception as exc:
                logger.error(f'Could not save death {death}: {exc}')
