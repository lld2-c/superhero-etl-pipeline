import src
import logging 
import module


def start():    
    # connect to db specified in .env
    connection_string = module.generate_conn_str()
    module.create_db_ifnot_exist(connection_string)

    # ETL
    extracted_data = src.extract_data('prod')
    transformed_data = src.transform_data(extracted_data)
    src.load_data(transformed_data)

def main():
    module.basic_logging_configure()
    try:
        start()
    except Exception as e: 
        logging.error(e)

if __name__ == "__main__":
    main()