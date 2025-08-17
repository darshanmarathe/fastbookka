call poact

@REM nodemon --exec "py main.py" -e py
nodemon --exec "uvicorn main:app" -e py
