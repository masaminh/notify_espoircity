"""エスポ産駒の出走予定を取得する."""
from argparse import ArgumentParser
from itertools import groupby

import jbis
import line
import settings
import utility


def main():
    """メイン関数."""
    p = ArgumentParser(description='エスポワールシチー産駒の出走予定をLINE Notifyに送る')
    p.add_argument('-d', '--debug', action='store_true', help='デバッグ用')
    args = p.parse_args()

    content = f'エスポワールシチー産駒の出走予定\n'

    for date, g in groupby(jbis.iter_sire_entries('0000888832'), lambda e: e.date):
        content += f'\n{date.strftime("%m/%d")}\n'
        for r, g2 in groupby(g, lambda x: (x.course, x.raceno, x.racename)):
            content += '　' + utility.get_racename_line(*r) + '\n'
            for e in g2:
                content += f'　　{e.horsename}\n'

    if args.debug:
        print(content)
    else:
        line.notify(settings.NOTIFY_ACCESS_TOKEN, content)


if __name__ == "__main__":
    main()
