import logging
import re
import time

from django.db import IntegrityError

from api_core.models import DataSource
from data_parsing.services.soup_utils import get_soup_from_url

ARTICLE_REGEX = re.compile(r'deces[e]?(?:[\W]*[\d]+)+', re.IGNORECASE)

logger = logging.getLogger(__name__)


def _parse_articles(articles):
    result = []
    article_index = 1
    for article in articles:

        p = article.find('p')
        if p is None:
            logger.warning(f'Parsing failed at article {article_index}')
            continue

        match = ARTICLE_REGEX.search(p.text)
        if match is not None:
            a = article.find('a')
            result.append((p.text, a['href']))

        article_index += 1
    return result


def _get_deceased_articles_links(base_url, page_count):
    article_links = []
    for page_index in range(1, page_count + 1):
        url = f'{base_url}?page={page_index}'
        logger.info(f'Parsing page {page_index}: {url}')

        soup = get_soup_from_url(url)
        articles = soup.find_all('article')
        article_links += _parse_articles(articles)

        time.sleep(0.5)

    return article_links


def _get_string_content(element):
    result = ""
    for string in element.strings:
        result += string
    return result


def _get_deceased_articles_contents(urls):
    result = []
    for title, url in urls:
        logger.info(f'Parsing article {url}')
        soup = get_soup_from_url(url)
        content_element = soup.find(class_='my-8 break-words rich-text')
        content = _get_string_content(content_element)
        result.append((url, title, content))
    return result


def collect_data_sources(base_url, page_count):
    urls = _get_deceased_articles_links(base_url, page_count)
    logger.info(f"Found {len(urls)} valid urls.")

    sources = _get_deceased_articles_contents(urls)
    logger.info(f"Found {len(urls)} valid sources from the urls.")

    added_count = 0
    for url, title, content in sources:
        try:
            DataSource.objects.create(url=url, parsed_content=content, title=title)
            added_count += 1
        except IntegrityError as exc:
            logger.info(f'Data source with url "{url}" already exists in the database. It is ignored.')
        except Exception as exc:
            logger.error(f"Could not create data source from {url}: {exc}")

    logger.info(f"Added {added_count} sources to the database.")
