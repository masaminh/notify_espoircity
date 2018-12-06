"""エスポワールシチー産駒の成績を通知する."""
import datetime
from argparse import ArgumentParser
from itertools import groupby

import emoji

import jbis
import line
import nar
import settings
import utility


def main():
    """メイン関数."""
    p = ArgumentParser(description='エスポワールシチー産駒の出走予定をLINE Notifyに送る')
    p.add_argument('-d', '--debug', action='store_true', help='デバッグ用')
    args = p.parse_args()

    content = "エスポワールシチー産駒の成績\n\n"
    today = datetime.date.today()
    todayhorse = (x for x in jbis.iter_sire_entries(
        '0000888832') if x.date == today)
    for r, g in groupby(todayhorse, lambda x: (x.course, x.raceno, x.racename)):
        content += utility.get_racename_line(*r) + '\n'
        raceresult = nar.get_race_result(today, r[0], r[1])
        if raceresult is not None:
            result = {x.name: x for x in nar.get_race_result(
                today, r[0], r[1])}
        else:
            result = dict()

        for h in g:
            if h.horsename in result:
                horse = result[h.horsename]
                poplar = horse.poplar
                order = horse.order
            else:
                poplar = '*'
                order = '*'

            content += f'　{h.horsename} {poplar}番人気 {order}着'

            if order == '1':
                content += emoji.emojize(':confetti_ball:')

            content += '\n'

    if args.debug:
        print(content)
    else:
        line.notify(settings.NOTIFY_ACCESS_TOKEN, content)


if __name__ == "__main__":
    main()
