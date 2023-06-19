from src import extract, transform, load
import logging 
import module
from config.configurations import connection_string

def main():
    # Create database
    module.create_db_ifnot_exist(connection_string)

    # Extract data
    extracted_data = extract.extract_data()

    # Transform data
    transformed_data = transform.transform_data(extracted_data)

    # Load data
    load.load_data(transformed_data)

if __name__ == '__main__':
    main()


# [x] load into SQL database hosted on Docker

# [] generate docker image

# [] deploy docker image to Kubernetes cluster

# [-] Your code should read from config file for dataset location, kubernetes cluster, others

# [x] Logging: Your code should log each step of the process to a file 

# [] error handling

# [-] unit tests

# [-] demo how it can be used for data analysts

# [] Design a data quality check and monitoring system

module.basic_logging_configure()
logging.info("Successfully completed etl")