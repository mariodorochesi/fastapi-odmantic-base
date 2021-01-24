#! /bin/bash
uvicorn main:app --app-dir=app --host=0.0.0.0 --port=5000 --reload