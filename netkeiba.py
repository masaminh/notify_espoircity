"""netkeiba.comへのアクセス関数群."""
import datetime
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from horseraceutility import HorseResult

_lastaccess = datetime.datetime(2000, 1, 1)


def get_race_result(date, course, raceno):
    """レース結果を取得する (本日分のみ)."""
    url = _get_raceurl('https://race.netkeiba.com/', date, course, raceno)
    r = _requests_get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    trs = soup.find('table', summary='レース結果').find_all('tr')

    def get_horseresult(tr):
        tds = tr.find_all('td')
        return HorseResult(tds[0].string, tds[3].a.string, tds[9].string)

    return [get_horseresult(tr) for (i, tr) in enumerate(trs) if i > 0]


def _get_raceurl(urlbase, date, course, raceno):
    courses = {'札幌': 1, '函館': 2, '福島': 3, '新潟': 4, '東京': 5,
               '中山': 6, '中京': 7, '京都': 8, '阪神': 9, '小倉': 10}

    if course not in courses:
        return None

    params = {'pid': 'race_list_sub', 'id': f'c{date.strftime("%m%d")}'}

    r = _requests_get(urlbase, params=params)

    soup = BeautifulSoup(r.content, 'html.parser')

    url = None
    hrefs = (x.find('a').get('href')
             for x in soup.find_all('div', class_='racename'))
    reg = re.compile(f'id=.{date.year:04}{courses[course]:02}....{raceno:02}')
    for href in hrefs:
        if reg.search(href):
            url = urljoin(urlbase, href)
            break

    if url is None:
        return None

    return url


def _requests_get(url, params=None):
    global _lastaccess
    delta = datetime.datetime.now() - _lastaccess

    if delta.seconds < 1:
        time.sleep(1 - delta.seconds)

    r = requests.get(url, params=params)
    _lastaccess = datetime.datetime.now()
    return r


def main():
    """メイン関数."""
    result = get_race_result(datetime.date(2018, 12, 2), '中京', 11)

    print(result)


if __name__ == "__main__":
    main()
