import unittest
import src
import logging
import module
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class loadTestCase(unittest.TestCase):
    def test_load(self): 
        module.basic_logging_configure()
        logging.info('Load unit test started..')
        # to simulate the transformed_data output       
        # extracted_data = src.extract_data('test')
        # transformed_data = src.transform_data(extracted_data)
        character_power = '[{"character_id":"0","character_name":"Darth Vader","power_id":"0","power_name":"Agility"},{"character_id":"0","character_name":"Darth Vader","power_id":"1","power_name":"Accelerated Healing"},{"character_id":"1","character_name":"Luke Skywalker","power_id":"0","power_name":"Agility"},{"character_id":"1","character_name":"Luke Skywalker","power_id":"1","power_name":"Accelerated Healing"},{"character_id":"2","character_name":"Princess Leia","power_id":null,"power_name":null}]'
        character_stats = '[{"character_stat_id":"0","alignment":"Good","intelligence":100,"strength":100,"speed":90,"durability":100,"power":100,"combat":90,"total":580,"character_id":"1"},{"character_stat_id":"1","alignment":"Good","intelligence":90,"strength":70,"speed":30,"durability":60,"power":30,"combat":95,"total":375,"character_id":"0"},{"character_stat_id":"2","alignment":"Good","intelligence":95,"strength":85,"speed":80,"durability":90,"power":80,"combat":80,"total":510,"character_id":"2"}]'
        character_comic = '[{"comic_id":"001","title":"Spider-Man","issue_number":1.0,"description":"The Amazing Spider-Man #1","character_id":"nan"},{"comic_id":"002","title":"Batman","issue_number":5.0,"description":"Batman #5","character_id":"nan"},{"comic_id":"003","title":"Superman","issue_number":2.0,"description":"Superman #2","character_id":"nan"}]'
        character_wikis = '[{"character_wiki_id":"0","gender":"Male","eyecolor":"Hazel","race":"Human","haircolor":"Brown","publisher":"Marvel","skincolor":"Fair","height":5.7,"weight":142.0,"identity":null,"status":null,"appearances":null,"first_appearance":null,"year":null,"universe":"Marvel","character_id":"1"},{"character_wiki_id":"1","gender":"Male","eyecolor":"Blue","race":"Human","haircolor":"Black","publisher":"Marvel","skincolor":"Fair","height":6.0,"weight":191.0,"identity":null,"status":null,"appearances":null,"first_appearance":null,"year":null,"universe":"DC","character_id":"0"},{"character_wiki_id":"2","gender":"Female","eyecolor":"Green","race":"Human","haircolor":"Red","publisher":"Marvel","skincolor":"Fair","height":5.6,"weight":131.0,"identity":null,"status":null,"appearances":null,"first_appearance":null,"year":null,"universe":"DC","character_id":"2"},{"character_wiki_id":"3","gender":"Male","eyecolor":"Hazel","race":null,"haircolor":"Brown","publisher":null,"skincolor":null,"height":null,"weight":null,"identity":"Secret","status":"Alive","appearances":500,"first_appearance":null,"year":1962,"universe":"Marvel","character_id":"1"},{"character_wiki_id":"4","gender":"Male","eyecolor":"Blue","race":null,"haircolor":"Black","publisher":null,"skincolor":null,"height":null,"weight":null,"identity":"Public","status":"Alive","appearances":1000,"first_appearance":null,"year":1938,"universe":"DC","character_id":"0"},{"character_wiki_id":"5","gender":"Male","eyecolor":"Black","race":null,"haircolor":"Black","publisher":null,"skincolor":null,"height":null,"weight":null,"identity":"Secret","status":"Alive","appearances":800,"first_appearance":null,"year":1939,"universe":"DC","character_id":"2"}]'
        transformed_data = (character_power, character_stats, character_comic, character_wikis)
        loaded = src.load_data(transformed_data)

        # delete the test data in the database
        connection_string = module.generate_conn_str()
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute("TRUNCATE TABLE character_comic_association CASCADE")
        session.execute("TRUNCATE TABLE character_power_association CASCADE")
        session.execute("TRUNCATE TABLE character_stats CASCADE")
        session.execute("TRUNCATE TABLE characters CASCADE")
        session.execute("TRUNCATE TABLE characters_wiki CASCADE")
        session.execute("TRUNCATE TABLE comics CASCADE")
        session.execute("TRUNCATE TABLE powers CASCADE")
        session.commit()
        session.close()

        logging.getLogger().info("Transform unit test completed")
        self.assertTrue(loaded)

if __name__ == '__main__':
    unittest.main()