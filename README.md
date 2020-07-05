# template_sanic

in system
  *     python3.7 -m venv .venv
  *     source .venv/bin/activate
  *     pip install poetry
  *     poetry update
  *     export REDIS_CONNECTION=
  *     start server: python -m sanic autoapp.app --host=0.0.0.0 --port=8000
  *     start tests: pytest tests/test.py 

in docker
  *     docker-compose build
  *     docker-compose up
    
