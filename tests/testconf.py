import unittest
import os

def get_cwd():
    return os.path.dirname(os.path.realpath(__file__))

from etllib.conf import Conf

class TestConf(unittest.TestCase):

    def setUp(self):
        file_path = os.path.join(get_cwd(), '..', 'config.yml.example')
        self.conf = Conf(file_path=file_path)

    def test_db_name(self): 
        data = self.conf.get_data_nodes('db_number_one')
        self.assertEqual(data['db_name'], 'production1')

    def test_db_host(self):
        data = self.conf.get_data_nodes('db_number_one')
        self.assertEqual(data['db_host'], '10.0.0.1')

    def test_db_port(self):
        data = self.conf.get_data_nodes('db_number_one')
        self.assertEqual(data['db_port'], 3306)

    def test_db_user(self):
        data = self.conf.get_data_nodes('db_number_one')
        self.assertEqual(data['db_user'], 'admin')

    def test_db_passwd(self):
        data = self.conf.get_data_nodes('db_number_one')
        self.assertEqual(data['db_passwd'], 'adminpass')

    def test_non_existing(self):
        data = self.conf.get_data_nodes('non-existing-platform')
        self.assertEqual(data, 'NaN')

    def test_list_dbs(self):
        self.assertItemsEqual(self.conf.get_data_nodes(), ['db_number_one', 'db_number_two', 'data_files'])


if __name__ == '__main__':

    unittest.main()