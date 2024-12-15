### dz_3_
Задание №3
------------------------------------------------------------------------------------------------------
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки. Выходной текст на
языке xml попадает в файл, путь к которому задан ключом командной строки.
------------------------------------------------------------------------------------------------------

Однострочные комментарии:

:: Это однострочный комментарий


Многострочные комментарии:
/+

Это многострочный

комментарий

+/


Массивы:

'( значение значение значение ... )


Словари:

@{

 имя = значение;
 
 имя = значение;
 
 имя = значение;
 
 ...
 
}


Имена:

[a-zA-Z][_a-zA-Z0-9]*


Значения:

• Числа.

• Массивы.

• Словари.



Объявление константы на этапе трансляции:

const имя = значение;



Вычисление константного выражения на этапе трансляции (постфиксная
форма), пример:

^[имя 1 +]



Результатом вычисления константного выражения является значение.
Для константных вычислений определены операции и функции:


1. Сложение.

2. Вычитание.

3. Умножение.

4. Деление.

5. concat().

6. mod().

*************************************************************************************************************************
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2
примера описания конфигураций из разных предметных областей.
*************************************************************************************************************************
