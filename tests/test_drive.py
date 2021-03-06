from unittest import TestCase
from mock import patch
import mock
from nose import with_setup


__author__ = 'krtek'

KEY = """INSERT KEY HERE"""
EMAIL = 'xxx@developer.gserviceaccount.com'
IMPERSONATE = 'admin@d22.myapps.cz'


def get_gae_mock_memcache():
    memcache = mock.MagicMock()
    memcache.get, memcache.set = mock.MagicMock(), mock.MagicMock()
    memcache.get.return_value = None
    return memcache

class TestDrive(TestCase):

    def setUp(self):
        from gapi import Api
        self.api = Api(['drive'],EMAIL , KEY, IMPERSONATE)

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_drive_list(self):
        files = self.api.drive.files.list()['items']
        self.assertGreater(len(files), 0)

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_drive_touch(self):
        file = self.api.drive.files.list()['items'][0]
        self.api.drive.files.touch(file['id'])

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_trash(self):
        file = self.api.drive.files.list()['items'][0]
        self.api.drive.files.trash(file['id'])
        self.api.drive.files.untrash(file['id'])

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_revisions(self):
        file = self.api.drive.files.list()['items'][0]
        revs_api = self.api.drive.revisions
        revs_api.file_id = file['id']
        self.assertGreater(len(revs_api.list()), 0)

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_revisions_empty_file_id(self):
        self.assertRaises(ValueError, self.api.drive.revisions.list)

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_changes(self):
        self.assertEquals(self.api.drive.changes.list(), 'x')
        changes = self.api.drive.changes.list()['items']
        self.assertGreater(0, changes)
        self.api.drive.changes.get(changes[0]['id'])

    @patch('google.appengine.api.memcache', get_gae_mock_memcache())
    def test_about(self):
        self.assertGreater(self.api.drive.about.get(), 0)





