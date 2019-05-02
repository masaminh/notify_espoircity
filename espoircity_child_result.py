"""エスポワールシチー産駒の成績を通知する."""
import datetime
import logging
from argparse import ArgumentParser
from itertools import groupby

import emoji

import horseracelib.jbis
import horseracelib.nar
import horseracelib.netkeiba
import line
import settings
import utility


def main():
    """メイン関数."""
    parser = ArgumentParser(description='エスポワールシチー産駒の出走予定をLINE Notifyに送る')
    parser.add_argument('-d', '--debug', action='store_true', help='デバッグ用')
    parser.add_argument('--loggingdebug', action='store_true', help='デバッグ用')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.loggingdebug else logging.INFO
    logging.basicConfig(level=log_level)

    nar = horseracelib.nar.Access()
    jbis = horseracelib.jbis.Access()
    netkeiba = horseracelib.netkeiba.Access()

    content = "エスポワールシチー産駒の成績\n\n"
    today = datetime.date.today()
    todayhorse = [x for x in jbis.iter_sire_entries(
        '0000888832') if x.date == today]

    if todayhorse:
        for race, group in groupby(todayhorse, lambda x: (x.course, x.raceno, x.racename)):
            content += utility.get_racename_line(*race) + '\n'
            raceresult = nar.get_race_result(today, race[0], race[1])
            if raceresult is None:
                raceresult = netkeiba.get_race_result(today, race[0], race[1])

            if raceresult is not None:
                result = {x.name: x for x in raceresult}
            else:
                result = dict()

            for scheduled in group:
                if scheduled.horsename in result:
                    horse = result[scheduled.horsename]
                    poplar = horse.poplar
                    order = horse.order
                else:
                    poplar = '*'
                    order = '*'

                content += f'　{scheduled.horsename} '

                if order.isdecimal():
                    content += f'{poplar}番人気 {order}着'
                elif order == '取消':
                    content += '出走取消'
                else:
                    content += order

                if order == '1':
                    content += emoji.emojize(':confetti_ball:')

                content += '\n'
    else:
        content += '出走なし\n'

    if args.debug:
        print(content)
    else:
        line.notify(settings.NOTIFY_ACCESS_TOKEN, content)


if __name__ == "__main__":
    main()
