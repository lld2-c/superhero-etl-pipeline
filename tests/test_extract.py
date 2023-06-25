import unittest
import src
import module
import logging 


class extractTestCase(unittest.TestCase):
    def test_extract(self):        
        module.generateTestData()
        module.basic_logging_configure()
        logging.info('Extract unit test started..')
        extracted_data = src.extract_data('test')
        self.assertIsNotNone(extracted_data)
        logging.getLogger().info("Extract unit test completed")

if __name__ == '__main__':
    unittest.main()