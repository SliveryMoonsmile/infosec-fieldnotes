import importlib.util
import sqlite3
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


build=module('build',ROOT/'scripts/build.py')
check=module('check',ROOT/'scripts/check.py')
lab=module('lab',ROOT/'labs/sqlite_binding.py')


class PublicationTests(unittest.TestCase):
    def test_quoted_data_is_not_query_syntax(self):
        with sqlite3.connect(':memory:') as con:
            con.execute('CREATE TABLE notes (title TEXT)')
            con.execute('INSERT INTO notes VALUES (?)',("Reader's note",))
            self.assertEqual(lab.lookup(con,"Reader's note"),("Reader's note",))
            self.assertIsNone(lab.lookup(con,"' OR 1=1 --"))
            self.assertEqual(con.execute('SELECT count(*) FROM notes').fetchone(),(1,))

    def test_metadata_is_escaped(self):
        self.assertEqual(build.esc('<script>"&'), '&lt;script&gt;&quot;&amp;')

    def test_secret_patterns_detect_generated_fixtures(self):
        # Generated fixtures only: these do not contain any real credential.
        key='AK'+'IA'+'Z'*16
        self.assertIn('AWS access key',check.secret_findings(key))
        self.assertIn('private key',check.secret_findings('-----BEGIN '+'PRIVATE KEY-----'))
        self.assertFalse(check.secret_findings('A note about AWS identity and temporary roles.'))

    def test_release_links_and_provenance(self):
        self.assertEqual(check.check(),0)


if __name__=='__main__': unittest.main()
