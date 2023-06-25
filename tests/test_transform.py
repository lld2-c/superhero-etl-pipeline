import unittest
import src
import pandas as pd
import logging
import module


class transformTestCase(unittest.TestCase):
    def test_transform(self):  
        module.basic_logging_configure()
        logging.info('Transform unit test started..')
        # below is to simulate extracted_data = src.extract_data('test') output
        data = {
            'characterID': [1, 2, 3],
            'name': ['Luke Skywalker', 'Darth Vader', 'Princess Leia']
            }
        characters = pd.DataFrame(data)
        data = {
            'comicID': [1, 2, 3],
            'characterID': [1, 2, 1]
            }
        charactersToComics = pd.DataFrame(data)
        data = {
            'Name': ['Luke Skywalker', 'Darth Vader', 'Princess Leia'],
            'Alignment': ['Good', 'Good', 'Good'],
            'Intelligence': [100, 90, 95],
            'Strength': [100, 70, 85],
            'Speed': [90, 30, 80],
            'Durability': [100, 60, 90],
            'Power': [100, 30, 80],
            'Combat': [90, 95, 80],
            'Total': [580, 375, 510]
        }
        characters_stats = pd.DataFrame(data)
        data = {
            'comicID': ['001', '002', '003'],
            'title': ['Spider-Man', 'Batman', 'Superman'],
            'issueNumber': [1.0, 5.0, 2.0],
            'description': ['The Amazing Spider-Man #1', 'Batman #5', 'Superman #2']
        }
        comics = pd.DataFrame(data)
        data = {
            'ID': [1, 2, 3],
            'Name': ['Luke Skywalker', 'Darth Vader', 'Princess Leia'],
            'Alignment': ['Good', 'Good', 'Neutral'],
            'Gender': ['Male', 'Male', 'Female'],
            'EyeColor': ['Hazel', 'Blue', 'Green'],
            'Race': ['Human', 'Human', 'Human'],
            'HairColor': ['Brown', 'Black', 'Red'],
            'Publisher': ['Marvel', 'Marvel', 'Marvel'],
            'SkinColor': ['Fair', 'Fair', 'Fair'],
            'Height': [5.7, 6.0, 5.6],
            'Weight': [142, 191, 131]
        }
        marvel_characters_info = pd.DataFrame(data)
        data = {
            'Name': ['Luke Skywalker', 'Darth Vader', 'Princess Leia'],
            'Agility': [True, True, False],
            'Accelerated Healing': [True, True, False],
            'Lantern Power Ring': [False, False, False],
            'Dimensional Awareness': [False, False, False],
            'Phoenix Force': [False, False, False],
            'Molecular Dissipation': [False, False, False],
            'Vision - Cryo': [False, False, False],
            'Omnipresent': [False, False, False],
            'Omniscient': [False, False, False]
        }
        superheroes_power_matrix = pd.DataFrame(data)
        data = {
            'ID': [1, 2, 3],
            'Name': ['Luke Skywalker', 'Darth Vader', 'Princess Leia'],
            'Identity': ['Secret', 'Public', 'Secret'],
            'Alignment': ['Good', 'Good', 'Good'],
            'EyeColor': ['Hazel', 'Blue', 'Black'],
            'HairColor': ['Brown', 'Black', 'Black'],
            'Gender': ['Male', 'Male', 'Male'],
            'Status': ['Alive', 'Alive', 'Alive'],
            'Appearances': [500, 1000, 800],
            'FirstAppearance': ['Amazing Fantasy #15', 'Action Comics #1', 'Detective Comics #27'],
            'Year': [1962, 1938, 1939],
            'Universe': ['Marvel', 'DC', 'DC']
        }
        marvel_dc_characters_ms = pd.DataFrame(data)
        extracted_data = (characters, charactersToComics, characters_stats, comics, marvel_characters_info, superheroes_power_matrix, marvel_dc_characters_ms)

        transformed_data = src.transform_data(extracted_data)
        logging.getLogger().info("Transform unit test completed")
        self.assertIsNotNone(transformed_data)

if __name__ == '__main__':
    unittest.main()