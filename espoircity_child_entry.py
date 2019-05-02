"""エスポ産駒の出走予定を取得する."""
from argparse import ArgumentParser
from itertools import groupby
import logging

import line
import settings
import utility
import horseracelib.jbis


def main():
    """メイン関数."""
    parser = ArgumentParser(description='エスポワールシチー産駒の出走予定をLINE Notifyに送る')
    parser.add_argument('-d', '--debug', action='store_true', help='デバッグ用')
    parser.add_argument('--loggingdebug', action='store_true', help='デバッグ用')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.loggingdebug else logging.INFO
    logging.basicConfig(level=log_level)

    jbis = horseracelib.jbis.Access()
    content = f'エスポワールシチー産駒の出走予定\n'

    for date, group in groupby(jbis.iter_sire_entries('0000888832'), lambda x: x.date):
        content += f'\n{date.strftime("%m/%d")}\n'
        for race, group2 in groupby(group, lambda x: (x.course, x.raceno, x.racename)):
            content += '　' + utility.get_racename_line(*race) + '\n'
            for scheduled in group2:
                content += f'　　{scheduled.horsename}\n'

    if args.debug:
        print(content)
    else:
        line.notify(settings.NOTIFY_ACCESS_TOKEN, content)


if __name__ == "__main__":
    main()
