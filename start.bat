
@echo off
pushd backend
start /b cmd /c python app.py
popd
pushd frontend
start /b cmd /c npm start
popd
