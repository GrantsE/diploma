# Дипломный проект "Твой каршеринг"
## Задача: необходимо реализовать сервис поминутной аренды автомобилей "Твой каршеринг" на базе фреймворка flask с использование базы данных SQLite.
## Требования:
Онлайн сервис "Твой каршеринг" должен обеспечивать следующий функционал:
### 1. Добавление новых автомобилей в базу данных с указанием картинки и описания;
### 2. Каждый автомобиль должен содержать следующие данные
  * название;
  * описание;
  * цена - может быть дробным числом;
  * вид коробки передач - автоматическая или нет;
  * 4 картинки.
### 3. Просмотр всех автомобилей сервиса;
### 4. Аренда автомобиля:
  * изначально автомобиль находится в состоянии "Свободен";
  * должна быть возможность арендовать автомобиль, которая переводит авто в состояние "Занят";
  * должна быть возможность закончить аренду - перевод авто в состояние "Свободен";
### 5. Изменение и удаление автомобилей;
### 6. Вывод истории аренды для конкретного авто. В таблице для конкретного авто должны выводиться все записи об аренде этого авто со следующими колонками:
  * дата и время начала аренды;
  * дата и время завершения аренды;
  * общая стоимость аренды.
### 7. Вывод журнала аренды - вывод истории аренда по всем авто со следующими колонками:
  * картинка;
  * название авто;
  * количество бронирований;
  * общее время аренды;
  * общая стоимость аренды.

## Требования к содержанию
Ниже приведено описание страниц сервиса.

### 1. Главная страница
На главной странице выводится список всех автомобилей, которые есть в базе данных. Для каждого автомобиля выводится картинка, название и стоимость аренды в минуту. При клике на карточку автомобиля должна открываться детальная страница авто.
### 2. Детальная страница авто
На детальной странице авто выводится следующая информация об автомобиле:
* ID автомобиля;
* Доступность: в этой строке должна выводиться надпись "свободен", если автомобиль еще не арендован и "занят", если автомобиль находится в аренде;
* Стоимость аренды;
* Кнопки:
 * арендовать/освободить: если авто свободен, то название кнопки "Арендовать"; если авто занят, то название кнопки "Освободить". Кнопка переводит авто в состояние "Свободен" или "Занят", в зависимости от текущего состояния.
 * Изменить - изменение всех полей автомобиля;
 * Удалить - удаление автомобиля из базы данных с удалением все истории его аренды.
 * Таблица "История аренды" - выводятся все записи из истории аренды этого авто.
### 3. Добавление нового автомобиля
На странице выводятся все поля из карточки автомобиля и кнопка "Создать", по нажатию на которую автомобиль добавляется в базу данных.
### 4. Журнал аренды
На странице выводится таблица, содержащая все записи по аренде для всех автомобилей. Состав колонок таблицы см. в разделе "Требования к функциональности".
