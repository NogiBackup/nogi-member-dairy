from typing import List

from sqlalchemy import (VARCHAR, BigInteger, Column, Constraint, Date, Integer,
                        MetaData, Table)
from sqlalchemy.engine import Engine
from sqlalchemy.sql.expression import and_, select

from nogi.objs.member import Member


class Members:

    def __init__(self, engine: Engine, metadata: MetaData):
        self.engine = engine
        self.table = Table(
            'members',
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('roma_name', VARCHAR(64)),
            Column('kana_name', VARCHAR(64)),
            Column('kanji_name', VARCHAR(64)),
            Column('birthday', Date),
            Column('term', Integer),
            Column('graduation', Date),
            Column('created_at', BigInteger),
            Column('updated_at', BigInteger),
            Constraint('nogi_members_pkey'),
            schema='nogizaka',
        )

    def get_member_profile(self, member_roma: str) -> Member:
        stmt = select([
            self.table.c.id,
            self.table.c.roma_name,
            self.table.c.kana_name,
            self.table.c.kanji_name,
            self.table.c.graduation,
        ]) \
            .where(
            and_(self.table.c.roma_name == member_roma)
        )
        return Member(info=dict(self.execute(stmt).fetchone()))

    def get_current_members(self) -> List[Member]:
        stmt = select([
            self.table.c.id,
            self.table.c.roma_name,
            self.table.c.kana_name,
            self.table.c.kanji_name,
            self.table.c.birthday,
            self.table.c.term,
            self.table.c.graduation
        ]) \
            .where(self.table.c.graduation == None)
        results = []
        for row in self.engine.execute(stmt).fetchall():
            results.append(
                Member(
                    info=dict(
                        id=row.id,
                        roma_name=row.roma_name,
                        kana_name=row.kana_name,
                        kanji_name=row.kanji_name,
                        birthday=row.birthday,
                        term=row.term,
                        graduation=row.graduation,
                    )
                )
            )
        return results
