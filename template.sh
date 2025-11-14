mkdir -p data
mkdir -p output
mkdir -p outputs
mkdir -p sample_data

# config
mkdir -p config
touch config/config.yaml
touch config/config.dev.yaml
touch config/config.prod.yaml


# src
mkdir -p src
touch src/__init__.py

mkdir -p src/job_recommender
touch src/job_recommender/__init__.py

mkdir -p src/job_recommender/ai
mkdir -p src/job_recommender/cli

# - core -
# core dir
mkdir -p src/job_recommender/core
# core files
touch src/job_recommender/core/__init__.py
touch src/job_recommender/core/settings.py
touch src/job_recommender/core/load_config.py
touch src/job_recommender/core/exceptions_config.py
touch src/job_recommender/core/logger_config.py
touch src/job_recommender/core/api_key_config.py
touch src/job_recommender/core/model_config.py



mkdir -p src/job_recommender/dashboard
mkdir -p src/job_recommender/task



mkdir -p test





echo "Directory and files are created!"