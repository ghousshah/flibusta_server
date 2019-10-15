from typing import List, Optional

import pathlib
import asyncpg
from aiohttp import web
from asyncpg import Record

from config import Config as config


async def create_pool(app: web.Application):
    app["pool"] = await asyncpg.create_pool(user=config.DB_USER, password=config.DB_PASSWORD,
                                            database=config.DB_NAME, host=config.DB_HOST)

    await create_tables(app["pool"])


SQL_FOLDER = pathlib.Path("./sql")


class Requests:
    create_book_table = open(SQL_FOLDER / "create_book_table.sql").read().format(config.DB_USER)
    create_author_table = open(SQL_FOLDER / "create_author_table.sql").read().format(config.DB_USER)
    create_book_author_table = open(SQL_FOLDER / "create_book_author_table.sql").read().format(config.DB_USER)
    create_sequence_name_table = open(SQL_FOLDER / "create_sequence_name_table.sql").read().format(config.DB_USER)
    create_sequence_table = open(SQL_FOLDER / "create_sequence_table.sql").read().format(config.DB_USER)
    create_book_annotation_table = open(SQL_FOLDER / "create_book_annotation_table.sql").read().format(config.DB_USER)
    create_author_annotation_table = open(SQL_FOLDER / "create_author_annotation_table.sql").read().format(config.DB_USER) # ToDO

    update_indexes = open(SQL_FOLDER / "update_indexes.sql").read()

    book_all_ids = open(SQL_FOLDER / "book_all_ids.sql").read()
    book_by_id = open(SQL_FOLDER / "book_by_id.sql").read()
    book_search_count = open(SQL_FOLDER / "book_search_count.sql").read()
    book_search = open(SQL_FOLDER / "book_search.sql").read()
    book_update = open(SQL_FOLDER / "book_update.sql").read()
    book_create = open(SQL_FOLDER / "book_create.sql").read()
    book_delete = open(SQL_FOLDER / "book_delete.sql").read()
    book_random = open(SQL_FOLDER / "book_random.sql").read()

    author_all_ids = open(SQL_FOLDER / "author_all_ids.sql").read()
    author_by_id = open(SQL_FOLDER / "author_by_id.sql").read()
    author_info_by_id = open(SQL_FOLDER / "author_info_by_id.sql").read()
    author_by_id_count = open(SQL_FOLDER / "author_by_id_count.sql").read()
    author_search_count = open(SQL_FOLDER / "author_search_count.sql").read()
    author_search = open(SQL_FOLDER / "author_search.sql").read()
    author_update = open(SQL_FOLDER / "author_update.sql").read()
    author_create = open(SQL_FOLDER / "author_create.sql").read()
    author_delete = open(SQL_FOLDER / "author_delete.sql").read()
    author_random_id = open(SQL_FOLDER / "author_random_id.sql").read()

    bookauthor_create = open(SQL_FOLDER / "bookauthor_create.sql").read()
    bookauthor_delete = open(SQL_FOLDER / "bookauthor_delete.sql").read()
    bookauthor_delete_by_author = open(SQL_FOLDER / "bookauthor_delete_by_author.sql").read()
    bookauthor_delete_by_book = open(SQL_FOLDER / "bookauthor_delete_by_book.sql").read()

    sequencename_all_ids = open(SQL_FOLDER / "sequencename_all_ids.sql").read()
    sequencename_by_id_count = open(SQL_FOLDER / "sequencename_by_id_count.sql").read()
    sequencename_by_id = open(SQL_FOLDER / "sequencename_by_id.sql").read()
    sequencename_search_count = open(SQL_FOLDER / "sequencename_search_count.sql").read()
    sequencename_search = open(SQL_FOLDER / "sequencename_search.sql").read()
    sequencename_record_by_id = open(SQL_FOLDER / "sequencename_record_by_id.sql").read()
    sequencename_create = open(SQL_FOLDER / "sequencename_create.sql").read()
    sequencename_update = open(SQL_FOLDER / "sequencename_update.sql").read()
    sequencename_delete_by_id = open(SQL_FOLDER / "sequencename_delete_by_id.sql").read()
    sequencename_random = open(SQL_FOLDER / "sequencename_random.sql").read()

    sequence_by_book_id = open(SQL_FOLDER / "sequence_by_book_id.sql").read()
    sequence_create = open(SQL_FOLDER / "sequence_create.sql").read()
    sequence_delete = open(SQL_FOLDER / "sequence_delete.sql").read()
    sequence_delete_by_sequence = open(SQL_FOLDER / "sequence_delete_by_sequence.sql").read()
    sequence_delete_by_book = open(SQL_FOLDER / "sequence_delete_by_book.sql").read()

    book_annotations_by_id = open(SQL_FOLDER / "book_annotation_by_id.sql").read()

    author_annotations_by_id = open(SQL_FOLDER / "author_annotation_by_id.sql").read()


async def create_book_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_book_table)


async def create_author_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_author_table)


async def create_book_author_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_book_author_table)


async def create_sequence_name_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_sequence_name_table)


async def create_sequence_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_sequence_table)


async def create_book_annotation_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_book_annotation_table)


async def create_author_annotation_table(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.create_author_annotation_table)


async def create_tables(pool: asyncpg.pool.Pool):
    await create_book_table(pool)
    await create_author_table(pool)
    await create_book_author_table(pool)
    await create_sequence_name_table(pool)
    await create_sequence_table(pool)
    await create_book_annotation_table(pool)
    await create_author_annotation_table(pool)

async def update_indexes(pool: asyncpg.pool.Pool):
    async with pool.acquire() as conn:  # type: asyncpg.Connection
        await conn.execute(Requests.update_indexes)


async def get_short_name(author) -> str:
    temp = ''
    if author['last_name']:
        temp += author['last_name']
    if author['first_name']:
        if temp:
            temp += " "
        temp += author['first_name'][0]
    if author['middle_name']:
        if temp:
            temp += " "
        temp += author['middle_name'][0]
    return temp


class BooksDB:
    @staticmethod
    async def all_ids(pool: asyncpg.pool.Pool):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = await conn.fetch(Requests.book_all_ids)
            return [] if result[0]["array_agg"] is None else result[0]["array_agg"]

    @staticmethod
    async def by_id(pool: asyncpg.pool.Pool, book_id: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = await conn.fetch(Requests.book_by_id, book_id)
            return result[0]["json_build_object"] if result else None

    @staticmethod
    async def search(pool: asyncpg.pool.Pool, query: str, allowed_langs: List[str],
                     limit: int, page: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            count = (await conn.fetch(Requests.book_search_count, allowed_langs, query))[0]["count"]
            if count == 0:
                return None
            result = (await conn.fetch(Requests.book_search,
                                       allowed_langs, query, limit, limit * (page - 1)))[0]["array_to_json"]
            return "{" + f'"result": {result}, "count": {count}' + "}"

    @staticmethod
    async def update(pool: asyncpg.pool.Pool, id_, title, lang, file_type):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.book_update, title, lang, file_type, id_)

    @staticmethod
    async def create(pool: asyncpg.pool.Pool, id_: int, title: str, lang: str, file_type: str):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.book_create, id_, title, lang, file_type)

    @staticmethod
    async def delete(pool: asyncpg.pool.Pool, ids: List[int]):
        if not ids:
            return
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await BookAuthor.delete_by_book(pool, ids)
            await Sequence.delete_by_book(pool, ids)
            await conn.execute(Requests.book_delete, ids)

    @staticmethod
    async def random(pool: asyncpg.pool.Pool, allowed_langs: List[str]):
        async with pool.acquire() as conn:
            result = await conn.fetch(Requests.book_random, allowed_langs)
            return result[0]["json_build_object"] if result else None


class AuthorsBD:
    @staticmethod
    async def all_ids(pool: asyncpg.pool.Pool):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = (await conn.fetch(Requests.author_all_ids))
            return result[0]["array_agg"] if result[0] else []

    @staticmethod
    async def by_id(pool: asyncpg.pool.Pool, author_id: int, allowed_langs: List[str], limit: int, page: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            count = (await conn.fetch(Requests.author_by_id_count, author_id, allowed_langs))[0]["count"]
            if count == 0:
                return None
            result = (await conn.fetch(Requests.author_by_id, allowed_langs, author_id,
                                       limit, limit * (page - 1)))[0]["json_build_object"]
            return "{" + f'"result": {result}, "count": {count}' + "}"

    @staticmethod
    async def search(pool: asyncpg.pool.Pool, query: str, allowed_langs: List[str],
                     limit: int, page: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            count = (await conn.fetch(Requests.author_search_count, query, allowed_langs))[0]["count"]
            if count == 0:
                return None
            result = (await conn.fetch(Requests.author_search, query, allowed_langs,
                                       limit, limit * (page - 1)))[0]["array_to_json"]
            return "{" + f'"result": {result}, "count": {count}' + "}"

    @staticmethod
    async def update(pool: asyncpg.pool.Pool, id_, first_name, middle_name, last_name):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.author_update,
                               first_name, middle_name, last_name, id_,
                               " ".join([first_name, middle_name, last_name], ))

    @staticmethod
    async def create(pool: asyncpg.pool.Pool, id_: int, first_name: str, middle_name: str, last_name: str):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.author_create, id_, first_name, middle_name, last_name,
                               " ".join([first_name, middle_name, last_name]))

    @staticmethod
    async def delete(pool: asyncpg.pool.Pool, ids: List[int]):
        if not ids:
            return
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await BookAuthor.delete_by_author(pool, ids)
            await conn.execute(Requests.author_delete, ids)

    @staticmethod
    async def random(pool: asyncpg.pool.Pool, allowed_langs: List[str]):
        async with pool.acquire() as conn:
            author_id = (await conn.fetch(Requests.author_random_id, allowed_langs))[0]["id"]
            return (await conn.fetch(Requests.author_info_by_id, author_id))[0]["json_build_object"]


class BookAuthor:
    @staticmethod
    async def create(pool: asyncpg.pool.Pool, book_id: int, author_id):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.bookauthor_create, book_id, author_id)

    @staticmethod
    async def delete(pool: asyncpg.pool.Pool, book_id: int, author_id: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.bookauthor_delete, book_id, author_id)

    @staticmethod
    async def delete_by_author(pool: asyncpg.pool.Pool, author_ids: List[int]):
        if not author_ids:
            return
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.bookauthor_delete_by_author, author_ids)

    @staticmethod
    async def delete_by_book(pool: asyncpg.pool.Pool, book_ids: List[int]):
        if not book_ids:
            return
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.bookauthor_delete_by_book, book_ids)


class SequenceName:
    @staticmethod
    async def all_ids(pool: asyncpg.pool.Pool):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            return (await conn.fetch(Requests.sequencename_all_ids))[0]["array_agg"]

    @staticmethod
    async def by_id(pool: asyncpg.pool.Pool, allowed_langs, seq_id: int, limit: int, page: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            count = (await conn.fetch(Requests.sequencename_by_id_count, seq_id, allowed_langs))[0]["count"]
            if count == 0:
                return None
            result = (await conn.fetch(Requests.sequencename_by_id, allowed_langs, seq_id,
                                       limit, limit * (page - 1)))[0]["json_build_object"]
            return "{" + f'"result": {result}, "count": {count}' + "}"

    @staticmethod
    async def search(pool: asyncpg.pool.Pool, allowed_langs, query: str, limit: int, page: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            count = (await conn.fetch(Requests.sequencename_search_count, query, allowed_langs))[0]["count"]
            if count == 0:
                return None
            result = (await conn.fetch(Requests.sequencename_search, query, allowed_langs,
                                       limit, limit * (page - 1)))[0]["array_to_json"]
            return "{" + f'"result": {result}, "count": {count}' + "}"

    @staticmethod
    async def record_by_id(pool: asyncpg.pool.Pool, seq_id: int) -> Optional[Record]:
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = await conn.fetch(Requests.sequencename_record_by_id, seq_id)
            return result[0] if result else None

    @staticmethod
    async def create(pool: asyncpg.pool.Pool, seq_id: int, name: str):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.sequencename_create, seq_id, name)

    @staticmethod
    async def update(pool: asyncpg.pool.Pool, seq_id: int, name: str):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.sequencename_update, seq_id, name)

    @staticmethod
    async def delete_by_id(pool: asyncpg.pool.Pool, seq_ids: List[int]):
        if not seq_ids:
            return
        async with pool.acquire() as conn:
            await Sequence.delete_by_sequence(pool, seq_ids)
            await conn.execute(Requests.sequencename_delete_by_id, seq_ids)

    @staticmethod
    async def random(pool: asyncpg.pool.Pool, allowed_langs: List[str]):
        async with pool.acquire() as conn:
            return (await conn.fetch(Requests.sequencename_random, allowed_langs))[0]["json_build_object"]


class Sequence:
    @staticmethod
    async def by_book_id(pool: asyncpg.pool.Pool, book_id: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = (await conn.fetch(Requests.sequence_by_book_id, book_id))[0]
            return result["array_agg"] if result["array_agg"] else []

    @staticmethod
    async def create(pool: asyncpg.pool.Pool, book_id: int, seq_id: int, num: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.sequence_create, book_id, seq_id, num)

    @staticmethod
    async def delete(pool: asyncpg.pool.Pool, book_id: int, seq_id: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.sequence_delete, book_id, seq_id)

    @staticmethod
    async def delete_by_sequence(pool: asyncpg.pool.Pool, seq_ids: List[int]):
        if not seq_ids:
            return
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.sequence_delete_by_sequence, seq_ids)

    @staticmethod
    async def delete_by_book(pool: asyncpg.pool.Pool, book_ids: List[int]):
        if not book_ids:
            return
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            await conn.execute(Requests.sequence_delete_by_book, book_ids)


class BookAnnotations:
    @staticmethod
    async def by_id(pool: asyncpg.pool.Pool, book_id: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = (await conn.fetch(Requests.book_annotations_by_id, book_id))
            return result[0]["json_build_object"] if result else None


class AuthorAnnotations:
    @staticmethod
    async def by_id(pool: asyncpg.pool.Pool, author_id: int):
        async with pool.acquire() as conn:  # type: asyncpg.Connection
            result = (await conn.fetch(Requests.author_annotations_by_id, author_id))
            return result[0]["json_build_object"] if result else None
