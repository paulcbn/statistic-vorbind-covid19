from data_parsing.services.case_analyzer.case_analyzer_service import analyze_all_cases
from data_parsing.services.raw_data_analyzer_service import create_deaths_from_data_sources
from data_parsing.services.sources_collector_service import collect_data_sources


def process_data_task():
    collect_data_sources(base_url="https://stirioficiale.ro/informatii", page_count=3)
    create_deaths_from_data_sources(today=True)
    analyze_all_cases(today=True)
