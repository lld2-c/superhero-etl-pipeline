pip install -r requirements.txt
export KAGGLE_CONFIG_DIR=./config
kaggle datasets download dannielr/marvel-superheroes/v/3 -p ./data --force

# once created_db_ifnot exists done
alembic upgrade heads