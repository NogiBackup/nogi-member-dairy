import json
from datetime import date


class Member:

    _id: int
    _roma_name: str
    _kana_name: str
    _kanji_name: str
    _birthday: date
    _term: int
    _graduation: date

    def __init__(self, info: dict) -> None:
        self._id = info['id']
        self._roma_name = info['roma_name']
        self._kana_name = info['kana_name']
        self._kanji_name = info['kanji_name']
        self._birthday = info['birthday']
        self._term = info['term']
        self._graduation = info['graduation']

    @property
    def id(self) -> int: return self._id

    @property
    def roma_name(self) -> str: return self._roma_name

    @property
    def kana_name(self) -> str: return self._kana_name

    @property
    def kanji_name(self) -> str: return self._kanji_name

    @property
    def birthday(self) -> date: return self._birthday

    @property
    def term(self) -> int: return self._term

    @property
    def graduation(self) -> date: return self._graduation

    def to_dict(self) -> dict:
        return dict(
            roma_name=self.roma_name,
            kana_name=self.kana_name,
            kanji_name=self.kanji_name,
            birthday=self.birthday.strftime("%Y-%m-%d"),
            term=self.term,
            graduation=self.graduation.strftime("%Y-%m-%d"),
        )

    def to_str(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=True)
