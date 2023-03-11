# Примеры
+ `.ebnf` - Extended Backus-Naur Form. Описание грамматики в форме расширенной форме Бэкуса-Наура. Описание грамматики см. в [документации](../_docs/grammar_description.pdf).
+ `.sgi` - Support Grammar Info. Вспомогательная информация о грамматике. Используется для описания грамматики в форме диаграмм Вирта - описывает лексику, ключевые слова и символы, список нетерминалов. Предствавляет из себя `.ebnf` без блока правил.
+ `.gv` - DOT-диаграммы. Описание грамматики в форме диаграмм Вирта.

## Формат представления диаграмм Вирта
### Формат рёбер
Все рёбра направленные
### Формат узлов
Виды вершин:
+ начальная - должно иметь тип `plaintext`.
+ конечная - должно иметь тип `point`.
+ именная - содержат имя нетерминала или терминала, должын иметь тип `box`.
+ ключевая - содержат ключи, должны иметь тип `oval`.

Условия:
+ Начальные и конечные вершины должны быть в диаграмме единственными.
+ В начальную вершину не могут входить дуги.
+ Из конечной вершины не могут исходить дуги.
+ Конечная вершина должна быть достижима из начальной.

## Грамматика `.sgi`
### РБНФ
```
SGI ::=
    TERMINALS_BLOCK KEYS_BLOCK NONTERMINALS_BLOCK
    AXIOM_BLOCK [ERROR_BLOCK]
```
### Диаграмма Вирта
Описание нетерминалов `TERMINALS_BLOCK`, `KEYS_BLOCK`, `NONTERMINALS_BLOCK`, `AXIOM_BLOCK`, `ERROR_BLOCK` см. в [документации](../_docs/grammar_description.pdf).

![Диагарамма Вирта .sgi](sgi_virt_diagram.png)
```
digraph SGI {
	start [label=SGI shape=plaintext]
	A [label=TERMINALS_BLOCK shape=box]
	B [label=KEYS_BLOCK shape=box]
	C [label=NONTERMINALS_BLOCK shape=box]
	D [label=AXIOM_BLOCK shape=box]
	F [label=ERROR_BLOCK shape=box]
	end [label="" shape=point]
	start -> A
	A -> B
	B -> C
	C -> D
	D -> F
	D -> end
	F -> end
}
```