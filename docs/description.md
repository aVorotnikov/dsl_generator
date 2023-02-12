# Генератор языков предметной области
Проект позволяет создавать языки предметной области (DSL). Синтаксис языка задаётся описанием грамматики языка через РБНФ. Семантика языка задаётся автоматным объектом на языке программирования общего назначения. Пока для этой цели рассматривается Python.
Проект ориентирован для применения в образовательном процессе в рамках курса «Грамматики и автоматы».
## Ролевая модель
Проект подразумевает ролевую модель использования. В модели есть 3 роли:
* Создатель DSL – задаёт грамматику и семантику согласно предметной области.
* Пользователь DSL – пишет программу на созданном DSL.
* Пользователь программы - использует написанную на DSL программу.
## Технические особенности
Поскольку проект рассчитан на применение в образовательном процессе, то предполагается обеспечить максимальную наглядность:
* Для программ строить дерево разбора
* …

Сканер и анализатор программы должны иметь задел на использование других форматов.