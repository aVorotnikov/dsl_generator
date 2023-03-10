# Инструмент создания языков предметной области
Позволяет создавать языки предметной области.
1. Синтаксис задаётся грамматикой
2. Семантика задаётся автоматным объектом

## Настройка рабочего окружения
1. Скачать пакеты при помощи pip:
```
pip install -r requirements.txt
```
2. Установить Graphviz. [Инструкция на официальном сайте](https://graphviz.org/download/)

## Содержание репозитория
### Вспомогательные инструменты
+ [Документация](_docs)
+ [Примеры](_examples)
+ [Утилиты](utils)

Подробнее о каждой части можно узнать в README их директорий.

### Основные инструменты
#### [scanner](scanner.py)
Позволяет получить поток лексем. Вызов скрипта с передачей ему пути к текстовому файлу в качестве аргумента выводит поток лексем.
#### [afterscan](afterscan)
Модуль редактирования потока лексем. Основные задачи:
+ разделение лексем (например при наличии ключей `+=` и `+` и отсутствии ключа `+=+` разумно разделить токен `+=+` на `+=` и `+`)
+ распознавание ключевых слов или конструкций
#### [build_ast](build_ast.py)
Позволяет получить абстрактное синтаксическое дерево программы по программе и описанию синтаксиса.
Задание синтаксиса см. в [описании примеров](_examples/README.md#формат-json-файлов), раздел "Формат JSON-файлов".
