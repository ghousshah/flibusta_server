DELETE FROM bookauthor WHERE book_id = ANY ($1::int[])