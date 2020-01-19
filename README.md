Тестовое задание для курса {ITIS} Upgrade. Создание базы даных из логов сервера и генерация отчетов с помощью микрофраймворка Flask. 
Данное тестовое задание написано на языке Python.

Алгоритм работы:
1. Установить необходимые библиотеке из файла requirements.txt.
```python
pip3 install -r requirements.txt
```
2. Запустить файл create_db.py, для создания базы данных.
```python
python3 create_db.py
```
3. Запусть сервер на Flask используя команды:
```python
export FLASK_APP=app.py flask run
```
для развертывания web-сервера и перейти по адресу [loclhost:5000](localhost:5000)
