SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
cd $SCRIPT_DIR

uvicorn api:app --host 0.0.0.0 --port 8000 --reload