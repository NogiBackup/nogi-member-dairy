from typing import List

from sqlalchemy import Column, Constraint, DateTime, MetaData, Table
from sqlalchemy.dialects.postgresql import (ARRAY, BIGINT, INTEGER, TEXT,
                                            VARCHAR)
from sqlalchemy.engine import Engine
from sqlalchemy.sql.expression import and_, desc, func, insert, select

from nogi.objs.blog import Blog


class Blogs:

    def __init__(self, engine: Engine, metadata: MetaData) -> None:
        self.engine = engine
        self.table = Table(
            'blogs',
            metadata,
            Column('id', BIGINT, primary_key=True, autoincrement=True),
            Column('blog_key', VARCHAR(64)),
            Column('member_id', INTEGER),
            Column('title', TEXT),
            Column('blog_created_at', DateTime),
            Column('content', TEXT),
            Column('storage_type', VARCHAR(64)),
            Column('post_paths', ARRAY(TEXT)),
            Column('image_paths', ARRAY(TEXT)),
            Column('created_at', DateTime),
            Column('updated_at', DateTime),
            Constraint('blogs_pkey'),
            Constraint('blog_post_ukey'),
            schema='nogizaka'
        )

    def get_member_blog_keys(self, member_id: int, limit: int = 10) -> List[str]:
        stmt = select([self.table.c.blog_key]) \
            .where(and_(self.table.c.member_id == member_id)) \
            .order_by(desc(self.table.c.blog_created_at)) \
            .limit(limit)
        return [row.blog_key for row in self.engine.execute(stmt).fetchall()]

    def get_members_latest_post_created_ts(self) -> dict:
        stmt = select([
            self.table.c.member_id,
            func.max(self.table.c.blog_created_at).label('latest_post_ts')])\
            .group_by(self.table.c.member_id)

        result = dict()
        for row in self.enigne.execute(stmt).fetchall():
            result[row.member_id] = row.latest_post_ts
        return result

    def insert_post(self, blog: Blog) -> bool:
        stmt = insert(self.table).\
            values(
                blog_key=blog.blog_key,
                member_id=blog.member_id,
                title=blog.title,
                blog_created_at=blog.blog_created_at,
                content=blog.content,
                storage_type=blog.storage_type,
                post_paths=blog.post_paths,
                image_paths=blog.image_paths,
        )
        return bool(self.engine.execute(stmt).rowcount)
