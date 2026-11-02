#!/usr/bin/env python3
"""A local, in-memory demonstration of parameter binding. No network access."""
import sqlite3


def lookup(connection, requested_title):
    return connection.execute(
        "SELECT title FROM notes WHERE title = ?", (requested_title,)
    ).fetchone()


def main():
    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE TABLE notes (title TEXT NOT NULL)")
        title = "Reader's fieldnote"
        connection.execute("INSERT INTO notes (title) VALUES (?)", (title,))
        assert lookup(connection, title) == (title,)
        assert lookup(connection, "' OR 1=1 --") is None
        assert connection.execute("SELECT count(*) FROM notes").fetchone() == (1,)
    print("PASS: values stayed data; table intact.")


if __name__ == "__main__":
    main()
