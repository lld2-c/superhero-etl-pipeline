import src
import logging 
import module

def main():
    # Extract data
    extracted_data = src.extract_data()

    # Transform data
    transformed_data = src.transform_data(extracted_data)

    # Load data
    src.load_data(transformed_data)

if __name__ == "__main__":
    main()


# [x] load into SQL database hosted on Docker

# [x] generate docker image

# [] deploy docker image to Kubernetes cluster

# [-] Your code should read from config file for dataset location, kubernetes cluster, others

# [x] Logging: Your code should log each step of the process to a file 

# [] error handling

# [-] unit tests

# [-] demo how it can be used for data analysts

# [] Design a data quality check and monitoring system

module.basic_logging_configure()
logging.info("Successfully completed etl")