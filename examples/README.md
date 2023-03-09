# Примеры
+ `.ebnf` - Extended Backus-Naur Form. Описание грамматики в форме расширенной форме Бэкуса-Наура. Описание грамматики см. в [документации](../docs/grammar_description.pdf).
+ `.sgi` - Support Grammar Info. Вспомогательная информация о грамматике. Используется для описания грамматики в форме диаграмм Вирта - описывает лексику, ключевые слова и символы, список нетерминалов. Предствавляет из себя `.ebnf` без блока правил.
+ `.gv` - DOT-диаграммы. Описание грамматики в форме диаграмм Вирта.

## Формат представления диаграмм Вирта
### Формат рёбер
Все рёбра - направленные
### Формат узлов
Виды рёбер:
+ начальное - должно иметь тип `plaintext`.
+ конечное - должно иметь тип `point`.
+ именные - содержат имя нетерминала или терминала, должын иметь тип `box`.
+ ключевые - содержат ключи, должны иметь тип `oval`.

Начальное и конечное ребро должны быть в диаграмме единственными

## Грамматика `.sgi`
### РБНФ
```
SGI ::=
    TERMINALS_BLOCK KEYS_BLOCK NONTERMINALS_BLOCK
    AXIOM_BLOCK [ERROR_BLOCK]
```
### Диаграмма Вирта
Описание терминалов см. в [документации](../docs/grammar_description.pdf).
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