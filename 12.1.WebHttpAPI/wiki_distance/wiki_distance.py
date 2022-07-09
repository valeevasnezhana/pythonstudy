import typing as tp
import requests

from pathlib import WindowsPath

from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup

# Directory to save your .json files to
# NB: create this directory if it doesn't exist
SAVED_JSON_DIR = WindowsPath(__file__).parent / 'visited_paths'



def retriable_request(url: str, tries: int = 3, timeout: int = 5) -> requests.Response:
    for i in range(tries):
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.RequestException:
            continue
    raise LookupError(f'Failed to fetch {url}')


def distance(source_url: str, target_url: str) -> tp.Optional[int]:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
    url = source_url
    visited = set()
    visited_path = []

    while True:
        visited.add(url)
        resp = retriable_request(url)
        html = resp.text

        soup = BeautifulSoup(html, 'lxml')

        title = soup.head.title.text
        title = title.rsplit(' — ')[0]
        visited_path.append({"title": title})
        print(title, len(visited) - 1)

        if target_url in visited:
            break

        article = soup.find(id="mw-content-text").find("div", class_="mw-parser-output")
        first_paragraph = article.find('p', recursive=False)
        if not first_paragraph:
            print('Failed to reach target page')
            return None

        for link in first_paragraph.find_all('a', href=True):
            url = link['href'].split('?', maxsplit=1)[0]

            splitted_url = urlsplit(url)
            if splitted_url.netloc and splitted_url.netloc != 'ru.wikipedia.org':
                continue
            if not splitted_url.path.startswith('/wiki/'):
                continue
            if ':' in splitted_url.path:
                continue

            url = urljoin('https://ru.wikipedia.org/', url)
            if url in visited:
                continue
            break
        else:
            print('Failed to reach target page')
            return None

    return len(visited) - 1






