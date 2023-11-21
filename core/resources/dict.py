# fmt: off

answer = {
    'start_reply': '<b>Бот для оформления заказов и поиска исполнителей.</b>\n\n'
                   'Для начала выберите роль:\n',
    'customer_reply': '<b>Вы в режиме работодателя.</b>\n\n'
                      'Удобный сервис для заключения сделок с фрилансерами. '
                      'Полный доступ к размещению заказа бесплатно и без регистрации.\n',
    'freelancer_reply': '<b>Вы в режиме фрилансера.</b>\n\n'
                        'Удобный сервис для заключения сделок с заказчиками.\n'
                        'Все проекты проходят через безопасную сделку.\n',
    'user_balance_reply': 'Следующим сообщением напишите сумму для пополнения баланса в рублях\n\n'
                          'Например: 3000 | 15500 | 22000',
    'incorrect_balance_reply': '<b>Ошибка, некорректное значение (<u>{}</u>)</b>\n'
                               'пожалуйста, введите корректную сумму (число, в рублях),\n'
                               '<i>например: 3000 | 15500 | 22000\n'
                               'разрешено пополнение на сумму от 93 до 924472 рублей.</i>',
    'incorrect_charge_reply': '<b>Ошибка, некорректное значение (<u>{}</u>)</b>\n'
                              'пожалуйста, введите корректную сумму (число, в рублях),\n'
                              '<i>например: 3000 | 15500 | 22000</i>',
    'incorrect_days_reply': '<b>Ошибка, некорректное значение (<u>{}</u>)</b>\n'
                            'пожалуйста, введите корректное число, в днях,\n'
                            '<i>например: 14 | 30 | 25</i>',
    'order_reply': 'Название заказа: <b>{}</b>\n\n'
                   'Бюджет: <b>{}</>\n'
                   'Ссылка на ТЗ: {}\n'
                   'Описание заказа: <b>{}</b>\n\n',
    'post_order': 'Заказ {}: <b>{}</b>\n'
                  'Бюджет: <b>{}₽</b>\n'
                  'Ссылка на ТЗ: {}\n'
                  'Описание заказа: <b>{}</b>\n',
    'read_order': '<b>{}</b>\n\n' '💎 <b>{}₽</b>\n\n' '<b>ОПИСАНИЕ</b>\n' '<i>{}</i>',
    'order_reply_tail': '<i>Обязательны для заполнения все поля, кроме ссылки на ТЗ!</i>',
    'publish_order_reply': 'Ваш заказ был опубликован!\n\n',
    'forward_order_reply': 'Ваш заказ был опубликован в канал <b>{}</b>',
    'publish_order_error_reply': 'Невозможно опубликовать заказ!\n\n'
                                 'Следующие параметры неправильно заполнены или отстуствуют:\n\n'
                                 '<b>{}</b>',
    'change_order_name_reply': 'Введите название заказа.\n\n',
    'change_order_budget_reply': 'Введите бюджет заказа в рублях.\n\n'
                                 'Например: 3000 | 15500 | 22000',
    'delete_draft_reply': 'Вы уверены, что хотите удалить текущий черновик?',
    'delete_order_reply': 'Вы уверены, что хотите удалить этот заказ?',
    'delete_application_reply': 'Вы уверены, что хотите удалить эту заявку?',
    'deleted_order_reply': 'Заказ удалён.',
    'deleted_application_reply': 'Заявка удалена.',
    'change_order_description_reply': 'Введите описание заказа.\n\n',
    'change_order_link_reply': 'Введите ссылку на ТЗ.\n\n'
                                '<i>разрешены только ссылки, которые начинаются с drive.yandex.ru и drive.google.com:</i>',
    'incorrect_url_reply': 'Ошибка. Некорректная ссылка ({})\n\n'
                           'Принимаются только ссылки, которые начинаются с drive.yandex.ru и drive.google.com',
    'check_param_reply': '{}:\n<b>{}</b>\n\nВсё правильно?',
    'check_balance_reply': '{}:\n<b>{}₽</b>\n\nВсё правильно?',
    'my_orders_reply': '💼 <b>Ваши заказы:</b>\n\n',
    'fl_applications_reply': '🔼 <b>Ваши заявки:</b>\n\n',
    'fl_projects_reply': '🗂️ <b>Вы работаете как исполнитель над следующими проектами:</b>\n\n',
    'сustomer_projects_reply': '🗂️ <b>Ваши заказы, находящиеся в работе у исполнителей:</b>\n\n',
    'customer_applications_reply': '💼 <b>На ваши заказы есть следующие заявки:</b>\n\n',
    'fl_find_orders_reply': '🔎 <b>КАТАЛОГ ЗАКАЗОВ:</b>\n\n',
    'fl_take_order_from_customer': '💼 На ваш заказ <b>{}</b> поступил отклик.\n'
                                   'Чтобы его посмотреть, перейдите в меню "Заявки".',
    'fl_send_message_reply': 'Введите сообщение, и оно будет отправлено заказчику.',
    'customer_send_message_reply': 'Введите сообщение, и оно будет отправлено исполнителю.',
    'bot_send_message_reply': '<b>Вам пришло новое сообщение.</b>\n\n'
                              '{} <b>{}</b>. Заявка: <b>{}</b>\n'
                              'Текст сообщения:\n<b>{}</b>',
    'bot_message_sent_reply': 'Ваше сообщение:\n<b>{}</b>\nпо заявке <b>{}</b> было отправлено пользователю <b>{}</b>.\n'
                              'Когда он ответит, вы получите уведомление.',
    'customer_mode': 'Вы в режиме заказчика.\n',
    'freelancer_mode': 'Вы в режиме исполнителя.\n',
    'customer_make_order': 'Новый заказ.\n',
    'deals_as_freelancer': '{} заказов выполнено',
    'deals_as_customer': '{} сделок завершено',
    'rename_account_reply': '👾 <b>{}</b>\n\n'
                            '<i>Следующим сообщением напишите имя, которое будет отображаться на платформе\n\n'
                            'Например: Иван Иванов, Ваня, Jane Doe</i>',
    'rename_account_success': '👾 <b>{}</b>\n\n' 'Ваше имя изменено!',
    'fl_take_order_reply': 'Ваша заявка на выполнение заказа\n<b>{}</b> была отправлена заказчику.\n',
    'insufficient_funds_reply': 'На вашем балансе недостаточно средств, чтобы принять эту заявку.',
    'apply_worker_reply_to_fl': '<b>🗂️ Вас выбрали исполнителем заказа.</b>\n\n'
                                   '💼 Заказчик: <b>{}</b>\n'
                                   '🌐 ID заказа: <b>{}</b>, ID заявки: <b>{}</b>\n'
                                   '✏️ Название заказа: <b>{}</b>\n'
                                   '📝 Описание заказа: <b>{}</b>\n'
                                   '💎 Назначенный вами бюджет в рублях: <b>{}</b>\n'
                                   '🌓 Назначенный вами срок в днях: <b>{}</b>\n',
    'apply_worker_reply_to_customer': '<b>‍💻 Исполнитель заказа успешно назначен!</b>',
    'fl_done_order_reply': '<b>‍🗂️ Вы отметили проект id{}, как выполненный!</b>\n\n'
                           'Заказчику отправлено уведомление.\n'
                           'Он может подтвердить завершение проекта\n'
                           'или внести правки. В любом случае вам придёт сообщение.',
    'customer_done_order_reply': '<b>‍🗂️ Вы отметили проект id{}, как выполненный!</b>\n\n'
                                 'Исполнителю отправлено уведомление '
                                 'и зачислены средства на баланс.',
    'done_order_message_from_freelancer': '<b>💻 Исполнитель {} отметил проект id{}, как выполненный!</b>\n\n'
                                          'Если работа выполнена корректно, подтвердите, нажав кнопку внизу, '
                                          'и исполнителю начислятся деньги за заказ.\n'
                                          'Если у вас остались замечания, отравте исполнителю сообщение.\n'
                                          'Позже вы можете отметить заказ, как выполненный в меню 🗂️ Проекты.',
    'done_order_message_from_customer': '<b>💼 Заказчик {} отметил проект id{}, как выполненный!</b>\n\n'
                                        'На ваш баланс было зачислено <b>{}₽</b>',
    'customer_details': '💼 <b>{}</b>\n\n'
                        '<i>Зарегистрирован {}</i>\n\n'
                        '⭐ {}\n'
                        '🤝 {}',
    'my_account_reply': '👾 <b>{}</b>\n\n'                    
                        '<i>Зарегистрирован {}</i>\n\n'
                        '⭐ {}\n'
                        '🤝 {}\n\n'
                        '💎 Баланс {}₽\n\n',
    'fl_appl_charge_reply': '<b>Следующим сообщением укажите сумму, которую хотите получить за выполнение заказа</b>\n\n'
                            '<i>Тщательно обдумайте ее, если вы новичок, то не стоит завышать цену\n'
                            'Цена указывается в рублях.\nНапример: 3000 | 15500 | 22000</i>',
    'fl_appl_days_reply': '<b>Следующим сообщением укажите сколько <u>дней</u> вам необходимо для выполнения заказа</b>\n\n'
                          '<i>Например: 1 | 23 | 120\n</i>',
    'fl_appl_message_reply': 'Следующим сообщением укажите текст заявки, который увидит заказчик\n\n',
                             # '<i>Бот вас заблокирует, если отправите свои контакты до заключения сделки\n'
                             # '(например, ник в Telegram, ссылка t.me, номер телефона, эл. почта и прочее)</i>',
    'fl_appl_final_reply': 'Заказчик получит следующий отклик:\n\n'
                           'Цена за выполнение работы: {}\n'
                           'Срок выполнения в днях: {}\n'
                           'Текст заявки: {}\n',
    'application_reply': '🔼 Заявка на ваш заказ <b>{}</b>\n'
                         'ℹ️ Номер заявки: <b>{}</b>. От пользователя: <b>{}</b>\n'
                         '🌐 <i>Создана {}</i>\n'
                         '💎 <i>Стоимость работы: </i><b>{}₽</b>\n'
                         '⏳ <i>Срок выполнения в днях: </i><b>{}</b>\n'
                         '📝 <i>Сообщение к заявке:</i>\n<b>{}</b>\n',
    'information': '⁉️ КАК ПОЛЬЗОВАТЬСЯ ПЛАТФОРМОЙ\n\n'
                   '1. Публикация заказов:\nдля публикации нового заказа нажмите на кнопку [⚡️ Создать заказ], '
                   'после чего будет создан новый черновик, к которому вы сможете в любой момент вернуться.\n'
                   'Как только заполните все поля, нажмите на кнопку [💠 Опубликовать], '
                   'проект будет отправлен  в публичный каталог заказов. '
                   'Избегайте политики и мата в названии и описании проекта, это противоречит правилам сообщества.\n'
                   '2. Как принимать заявки от фрилансеров:\n'
                   'Мы оповестим вас о первом отклике. '
                   'Все отклики на заказы можно увидеть, нажав на кнопку [🔼 Заявки].\n'
                   '3. Заключить сделку с фрилансером:\n'
                   'Если вы договорились о цене и сроках, то нажмите на кнопку [✅ Назначить исполнителем].\n'
                   'После этого шага вам необходимо зарезервировать средства. Не беспокойтесь, '
                   'в случае возникновения проблем мы вернем их в полной мере. '
                   'После оплаты фрилансер приступит к выполнению поставленных задач.',
    'added_funds_reply': 'Вы успешно пополнили баланс на <b>{}₽</b>\n'
                         'Ваш баланс: <b>{}₽</b>\n',
}
# fmt: on
