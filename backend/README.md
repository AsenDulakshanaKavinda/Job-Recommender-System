# Job Recommender System API

This is a FastAPI-based API for the Job Recommender System, which processes PDF resumes to generate summaries, keywords, skill gaps, and roadmaps using AI workflows (powered by Mistral LLM and related tools).

## Features
- Upload a PDF resume via a POST endpoint.
- Processes the resume through a predefined workflow to extract and analyze content.
- Returns JSON results including summary, keywords, skill gaps, and roadmap.
- Handles errors gracefully and cleans up temporary files.

## Prerequisites
- Python 3.8+ installed.
- Git (for cloning the repository).

## Installation

1. **Install UV package manager**:
```
pip install uv

```

2. **Clone the repository**:
```
git clone https://github.com/AsenDulakshanaKavinda/Job-Recommender-System.git
cd Job-Recommender-System/backend
```

3. **Create virtual environment and activate it**:
```
uv venv .venv
source .venv/Scripts/activate or if windows .venv/Scripts/activate 
```

4. **Install dependency**:
```
uv sync

```

5. **Add .env file**:
```
ENV="dev"
LLM_PROVIDER="mistral"
EMBEDDING_PROVIDER="mistral"
MISTRAL_API_KEY=<Your Mistral API key>
APIFY_API_KEY=<Your Apify API key>
```
## Usage
7. **Details**:
* Endpoint: /process_resume
* Method: POST
* Description: Upload a resume PDF and get the processed results.
* Response
```
{
  "status": "success",
  "result": {
    "summery": "Your resume summary...",
    "keywords": ["keyword1", "keyword2"],
    "skill_gap": {...},
    "road_map": {...}
  }
}
```

