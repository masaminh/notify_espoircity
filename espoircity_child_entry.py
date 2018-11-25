"""エスポ産駒の出走予定を取得する."""
from itertools import groupby

import jbis
import line
import mojimoji
import settings


def main():
    """メイン関数."""
    content = f'エスポワールシチー産駒の出走予定\n'

    for date, g in groupby(jbis.iter_sire_entries('0000888832'), lambda e: e.date):
        content += f'\n{date.strftime("%m/%d")}\n'
        for e in g:
            racename = mojimoji.zen_to_han(e.racename, kana=False)
            content += f'{e.course}{e.raceno}R {racename} {e.horsename}\n'

    line.notify(settings.NOTIFY_ACCESS_TOKEN, content)


if __name__ == "__main__":
    main()
