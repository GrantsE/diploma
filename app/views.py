from app import app, db
from app.models import Auto, RentHistory, RentJournal
from flask import render_template, request
from datetime import datetime
from sqlalchemy import func


@app.route('/')
def index():
    
    # Получаем данные из класса Auto
    auto_list = Auto.query.all()
    
    # Полученные данные передаем в контекст
    context = {'auto_list': auto_list,}
    
    return render_template('index.html', **context)


@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():
    
    context = None

    if request.method == 'POST':
        
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить авто')
        # Получаем название авто - это значение поля input с атрибутом name="name"
        auto_title = request.form['name']

        # Получаем стоимость аренды - это значение поля input с атрибутом name="price"
        auto_rent_price = request.form['price']
        
        # Получаем описание авто - это значение поля input с атрибутом name="description"
        auto_description = request.form['description']
        
        # Получаем информацию о коробке передач - это значение поля input с атрибутом name="trasmission"
        auto_transmission = request.form['transmission']
        if auto_transmission == 'option1':
            auto_transmission = True
        else:
            auto_transmission = False
                     
        # Добавляем информацию в базу данных
        db.session.add(Auto(name_auto = auto_title, rent_price = auto_rent_price, 
                            description = auto_description, transmission = auto_transmission,
                            img_url = request.form['img_url'],
                            img_url2 = request.form['img_url2'],
                            img_url3 = request.form['img_url3'],
                            img_url4 = request.form['img_url4'],))
        
        # Добавляем информацию также в базу RentJournal
        db.session.add(RentJournal(name = auto_title, photo = request.form['img_url'],
                                   description = auto_description))

        # сохраняем изменения в базе
        db.session.commit()

        # Заполняем словарь контекста
        context = {
            'method': 'POST',
            'name': auto_title,
            'price': auto_rent_price,
            'description': auto_description,
            'transmission': auto_transmission,
        }
    
    elif request.method == 'GET':

        context = {
            'method': 'GET',
        }
        
        
    return render_template('create_auto.html', **context)


@app.route('/auto_detail/<int:auto_id>', methods=['GET','POST'])
def auto_detail(auto_id):

   # Получаем экземпляр модели Auto по переданному в url параметру
    auto_info = Auto.query.get(auto_id)
    
    rent_context = None
    
    if request.method == 'GET' or request.method == 'POST':
        if request.method == 'POST':
            # Создаём условие. Если отображена кнопка арендовать, то при нажатии кнопка
            # поменяется на Освободить, а статус на Занят, при нажатии на Освободить
            # значение снова поменяется на Арендовать, а поле статуса будет = Свободен
            if auto_info.rent_status != 'Освободить':
                auto_info.car_availability = 'Занят' 
                auto_info.rent_status = 'Освободить' 
                db.session.add(RentHistory(auto_id2 = auto_id, beginning_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                        end_date = None, total_price = None))
            else:
                auto_info.car_availability = 'Свободен'
                auto_info.rent_status = 'Арендовать'
                RentHistory.query.filter_by(end_date = None, auto_id2 = auto_id).update(
                        {'end_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
                            )
                # Получаем объекты, где общая цена не определена, фильтруя по условию
                price_info = RentHistory.query.filter_by(total_price = None, auto_id2 = auto_id)
                # Получаем данные о том, сколько по времени в сек. машина была в аренде
                time_data = (datetime.strptime(price_info[0].end_date, "%d/%m/%Y %H:%M:%S")-
                        datetime.strptime(price_info[0].beginning_date, "%d/%m/%Y %H:%M:%S")).seconds
                # Добавляем общую цену и время аренды в базу
                RentHistory.query.filter_by(total_price = None, auto_id2 = auto_id).update(
                                    {'total_time': time_data,
                                    'total_price': round(time_data / 60 * auto_info.rent_price, 0)
                                    })
            db.session.commit()
        
        
        # Получаем все объекты по переданному url-параметру
        rent_info = RentHistory.query.filter_by(auto_id2 = auto_id).all()
            
        rent_context = {
                        'rent_info': rent_info,
                        }
        
        # Задаём условие. Если автоматическая КПП, то присваемаем Да
        if auto_info.transmission == True:
            auto_info.transmission = 'Да'
        else:
            auto_info.transmission = 'Нет'
                  
        context = {
                    'name_auto': auto_info.name_auto,
                    'yes_or_not': auto_info.transmission,
                    'id_auto': auto_info.auto_id,
                    'price': auto_info.rent_price,
                    'auto_description': auto_info.description,
                    'img_url': auto_info.img_url,
                    'img_url2': auto_info.img_url2,
                    'img_url3': auto_info.img_url3,
                    'img_url4': auto_info.img_url4,
                    'car_availability': auto_info.car_availability,
                    'rent_status': auto_info.rent_status,  
                }
    
    return render_template('auto_detail.html', **context, rent_context=rent_context)


@app.route('/change_auto/<int:auto_id>', methods=['POST', 'GET'])
def change_auto(auto_id):
    
    auto_info = Auto.query.get(auto_id)
    auto_journal = RentJournal.query.get(auto_id)
    
    context = None
    
    if request.method == 'POST':
        
        # Получаем новое название
        new_name = request.form['new_name']

        # Получаем новую стоимость
        new_price = request.form['new_price']
                        
        # Получаем новое описание
        new_description = request.form['new_description']
                        
        # Получаем новую информацию о КПП
        new_transmission = request.form['new_transmission']
        if new_transmission == 'option1':
            auto_info.transmission = True
        else:
            auto_info.transmission = False
                
        # Поучаем новые картинки
        image1 = request.form["new_img_url"]
        image2 = request.form["new_img_url2"]
        image3 = request.form["new_img_url3"]
        image4 = request.form["new_img_url4"]
                
        if new_name:
            auto_info.name_auto = new_name
            auto_journal.name = new_name
                        
        if new_price:
            auto_info.rent_price = new_price
                
        if new_description:
            auto_info.description = new_description
            auto_journal.description = new_description
                      
        if image1:
            auto_info.img_url = image1
            auto_journal.photo = image1
                    
        if image2:
            auto_info.img_url2 = image2
                    
        if image3:
            auto_info.img_url3 = image3
                    
        if image4:
            auto_info.img_url4 = image4
        
        # Возвращаем доступность и статус авто в исходные значения Арендовать и Свободен,
        # так как машина будет изменена    
        Auto.query.filter_by(auto_id = auto_id).update({'rent_status': 'Арендовать',
                                                       'car_availability': 'Свободен'})
       
        # Удаляем информацию об истории аренды прошлого авто, так как машина изменится
        RentHistory.query.filter(RentHistory.auto_id2.like(auto_id)).delete(synchronize_session = 'fetch')
        
        # Фиксируем все изменения            
        db.session.commit()
                                
    # Заполняем словарь контекста
    context = {  
                'id': auto_info.auto_id,
                'new_name': auto_info.name_auto,
                'new_price': auto_info.rent_price,
                'new_description': auto_info.description,
                'new_transmission': auto_info.transmission,
                'new_img_url': auto_info.img_url,
                'new_img_url2': auto_info.img_url2,
                'new_img_url3': auto_info.img_url3,
                'new_img_url4': auto_info.img_url4,    
                }
    

    return render_template('change_auto.html', **context)
    

@app.route('/del_auto/<int:auto_id>', methods=['POST'])
def del_auto(auto_id):
    
    # Удаляем машину с базы
    Auto.query.filter(Auto.auto_id.like(auto_id)).delete(synchronize_session = 'fetch')
    
    # Удаляем информацию об истории аренды авто
    RentHistory.query.filter(RentHistory.auto_id2.like(auto_id)).delete(synchronize_session = 'fetch')
    
    # Удаляем журнал по общим итоговым данным авто
    RentJournal.query.filter(RentJournal.id.like(auto_id)).delete(synchronize_session = 'fetch')
    
    db.session.commit()
    
    return render_template('del_auto.html')


@app.route('/rental_log')
def rental_log():
    
    # Получаем кол-во строк в классе Auto
    auto_numbers = int(Auto.query.count())
    
    # Проходимся циклом по id авто
    for i in range(1, auto_numbers + 1):
        # Фильтруем данные согласно id
        rent_data = RentHistory.query.filter_by(auto_id2 = i)
        # Получаем общую сумму аренды машины за весь период
        amount = db.session.query(func.sum(RentHistory.total_price)).filter_by(auto_id2 = i)
        # Получаем итоговое время аренды в минутах
        time_minute = db.session.query(func.sum(RentHistory.total_time) / 60).filter_by(auto_id2 = i)
        # Получаем итоговое время аренды в секундном формате
        time_second = db.session.query(func.sum(RentHistory.total_time) % 60).filter_by(auto_id2 = i)
        # Обновляем данные в классе
        RentJournal.query.filter_by(id = i).update(
            {'bookings_number': rent_data.count(),
             'total_amount': amount,
             'total_minute': time_minute,
             'total_second': time_second 
             })
        
    db.session.commit()
    
    rent_journal = RentJournal.query.all()
        
    context = {'rent_journal': rent_journal}
        
    return render_template('rental_log.html', **context)
    












    
    

