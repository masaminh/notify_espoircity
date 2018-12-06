"""ユーティリティ関数."""
import mojimoji


def get_racename_line(course, raceno, racename):
    """レース名行の取得."""
    racename = mojimoji.zen_to_han(racename, kana=False)
    return f'{course}{raceno}R {racename}'
