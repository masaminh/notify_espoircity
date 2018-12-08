"""JBISへのアクセス関数群."""
import re
import datetime
from collections import namedtuple

import requests
from bs4 import BeautifulSoup


def iter_sire_entries(horseid):
    """指定されたIDの種牡馬の産駒の出走予定を返す."""
    r = requests.get(f'https://www.jbis.or.jp/horse/{horseid}/sire/entry/')
    soup = BeautifulSoup(r.content, "html.parser")
    h2s = soup.find_all('h2')
    today = datetime.date.today()

    Entry = namedtuple(
        'Entry', ['date', 'course', 'raceno', 'racename', 'horsename'])

    for h2 in h2s:
        m = re.fullmatch(r"\s?([0-9]{1,2})月\s?([0-9]{1,2})日出走分", h2.string)
        month = int(m.group(1))
        day = int(m.group(2))
        date = datetime.date(
            today.year + (0 if today.month <= month else 1), month, day)

        for tr in h2.find_next('tbody').find_all('tr'):
            tds = tr.find_all('td')
            entry = Entry(date, tr.find('th').string,
                          int(tds[0].string), tds[1].text.strip(), tds[7].string)
            yield entry
