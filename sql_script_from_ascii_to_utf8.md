### Команда для изменения кодировки:

Скрипт нужен для того, чтобы мы могли сортировать запросы like с маленьких букв, ascii работает с латиницей, поэтому utf-8 для кириллицы.

SET client_encoding = 'UTF8';
UPDATE pg_database SET datcollate='ru_RU.UTF-8', datctype='ru_RU' WHERE datname='booking';
UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'booking';

После запуска команд не забудьть открыть новый SQL скрипт/редактор