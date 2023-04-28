@echo off
title ui-to-py
color 0a
chcp 65001
set /P in="Введи название входного файла: "
set /P out="Введи название выходного файла: "
python -m PyQt5.uic.pyuic -x %in%.ui -o %out%.py