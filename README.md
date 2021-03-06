### Тема курсовой работы: "Разработка утилиты для мониторинга сети"
### Авторы: [Бурзунов Д.](https://github.com/Aranatell), [Готовцев И.](https://github.com/xotohop), [Рустамов Р.](https://github.com/fewva)

#### Утилита: многопоточный сканер TCP-портов

###### Запуск:

    python3 scan_threading.py {args}

    args:
    -H/--hostlist: имя txt-файла со списком хостов, по-умолчанию - host_list
    -P/--portlist: имя txt-файла со списком портов, по-умолчанию - port_list

###### Пример:

    python3 scan_threading.py --hostlist hosts --portlist ports

    Хост: 192.168.0.12

    Список портов которые закрылись после прошлого сканирования:
    [['192.168.0.12', 34036], ['192.168.0.12', 52620]].

    Хост: 192.168.0.8

    Изменений с последнего сканирования не обнаружено.

##### Первичная настройка
###### 1. Автоматизиация скрипта


Для автоматизации выполнения скрипта scan_threading.py рекоммендуется использовать cron

	1. Для начала нужно выдать права на исполнение скрипта в системе:

		chmod +x /путь к файлу/scan_threading.py

	2. После этого запускаем таблицу скриптов cron:

		crontab -e

	3. После выбора редактора для просмотра и внесения изменений в таблицу, попадаем в файл.

	Запись скрипта в crontab обладает несложным синтаксисом, понятно изложнную информацию можно получить [тут](https://crontab.guru/)
	Примерный синтаксис вашего выражения:

		* * * * * python3 /путь к файлу/scan_threading.py
		#выполнение скрипта будет проводиться ежеминутно

		0 9 * * 1-5 python3 /путь к файлу/scan_threading.py
		#выполнение скрипта будет проводиться в девять утра каждый будний день


		#выполнение скрипта будет проводиться один раз в час

	ВАЖНО: после строчки с выражением стоит оставить одну пустую строку (в некоторых версиях без неё работать ничего не будет)


###### 2. Настройка персонального telegram-бота для получения уведомлений об изменениях после сканирования портов

	1. Для начала необходимо получить собственного бота. Делается это [тут](https://t.me/BotFather), у @BotFather - телеграм-бота, который помогает пользователям работать с собственными ботами.

	2. Перейдя в окно к боту, мы создаём собственного бота (команда /newbot), после чего вводим его название и ник

	3. Проделав необходимые манипуляции, мы получаем токен для API нашего бота (token to access HTTP API). Такой код нужен для подключения к серверам телеграмма и успешной обработки сообщений пользователей.

		Образец токена:
		1438173397:AAHA9tBrGDzxFfb5cgNT47Qd7ED1c4ID000

	4. Полученный токен нужно вставить в код файлов tg_01.py и scan_threading.py (строки 10 и 14 соответственно)

		Пример заполнения:
		bot = telebot.TeleBot('1438173397:AAHA9tBrGDzxFfb5cgNT47Qd7ED1c4ID000')


Теперь, при работе скрипта, бот будет отвечать на ваши сообщения, позволит вам просмотривать лист отслеживаемых Вами хостов и добалять новые, а так же присылать уведомления об изменении каждого хоста при срабатывании скрипта scan_threading.py (что будет происходить автоматически за счёт наших манипуляций с cron)

Скрипт scan_threading.py может так же запускаться вами вручную, что никак не повлияет на работу бота - он так же пришлёт вам нужную информацию.

Для вашего же удобства предлагаем так же автоматизировать скрипт tg_0t.py, так же уложив его в cron:

		Код:
		@reboot python3 /путь к файлу/scan_threading.py

Скрипт будет автоматически запускаться каждый раз при загрузке системы, бот начнёт отвечать на ваши сообщения и присылать отчёты в соответствии с Вашими настройками

Приятного пользования :)