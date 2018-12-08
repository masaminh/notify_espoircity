"""keiba.go.jpへのアクセス関数群."""
import datetime
import time

import requests
from bs4 import BeautifulSoup

from horseraceutility import HorseResult

_lastaccess = datetime.datetime(2000, 1, 1)


def get_race_result(date, course, raceno):
    """レース結果を取得する."""
    global _lastaccess

    courses = {'門別': 36, '盛岡': 10, '水沢': 11, '浦和': 18, '船橋': 19, '大井': 20, '川崎': 21,
               '金沢': 22, '笠松': 23, '名古屋': 24, '園田': 27, '高知': 31, '佐賀': 32}

    if course not in courses:
        return None

    params = {'k_raceDate': date.strftime('%Y/%m/%d'),
              'k_raceNo': raceno, 'k_babaCode': courses[course]}

    delta = datetime.datetime.now() - _lastaccess

    if delta.seconds < 1:
        time.sleep(1 - delta.seconds)

    r = requests.get(
        'http://www2.keiba.go.jp/KeibaWeb/TodayRaceInfo/RaceMarkTable', params=params)
    _lastaccess = datetime.datetime.now()

    soup = BeautifulSoup(r.content, "html.parser")

    def get_horseresult(tr):
        tds = tr.find_all('td')
        return HorseResult(tds[0].string, tds[3].text.strip(), tds[14].string)

    return [get_horseresult(tr) for tr in soup.find('tr', class_='dbitem').findNextSiblings('tr')]
