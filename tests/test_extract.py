# unit test if file read proper
# import pandas as pd

# assert not characters.empty, "DataFrame is empty"

# o_characters['character_id'].duplicated().any()
# if has_duplicates:
#     print("The 'character_id' column has duplicates.")
# else:
#     print("The 'character_id' column has no duplicates.")


import unittest
import src


class ExtractTestCase(unittest.TestCase):
    def test_extract(self):        
        extracted_data = src.extract_data()
        self.assertIsNotNone(extracted_data)

if __name__ == '__main__':
    unittest.main()