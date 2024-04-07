import unittest
import sqlite3


class TestDatabase(unittest.TestCase):
    def test_sentences_table_existence(self):
        conn = sqlite3.connect("sentences.db")
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sentences'"
        )
        table_exists = c.fetchone() is not None
        conn.close()
        self.assertTrue(
            table_exists, "The 'sentences' table does not exist in the database."
        )


if __name__ == "__main__":
    unittest.main()
