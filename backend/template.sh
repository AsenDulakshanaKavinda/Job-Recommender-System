
mkdir -p sample_data

# config
mkdir -p config
touch config/config.yaml
touch config/config.dev.yaml
touch config/config.prod.yaml


# src
mkdir -p job_recommender
touch job_recommender/__init__.py

mkdir -p job_recommender/src
touch job_recommender/src/__init__.py


# - core -
# core dir
mkdir -p job_recommender/src/core
# core files
touch job_recommender/src/core/__init__.py
touch job_recommender/src/core/settings.py
touch job_recommender/src/core/load_config.py
touch job_recommender/src/core/exceptions_config.py
touch job_recommender/src/core/logger_config.py
touch job_recommender/src/core/api_key_config.py
touch job_recommender/src/core/model_config.py

# loaders
mkdir -p job_recommender/src/loaders
touch job_recommender/src/loaders/pdf_loader.py

# loaders
mkdir -p job_recommender/src/preprocessing
touch job_recommender/src/preprocessing/preprocessor.py
touch job_recommender/src/preprocessing/embedder.py
touch job_recommender/src/preprocessing/scorer.py

# llm
mkdir -p job_recommender/src/llm
touch job_recommender/src/llm/client.py
touch job_recommender/src/llm/prompts.py

# llm
mkdir -p job_recommender/src/vector_db
touch job_recommender/src/vector_db/db_manager.py

# app
mkdir -p app
touch app/app.py

mkdir -p test





echo "Directory and files are created!"