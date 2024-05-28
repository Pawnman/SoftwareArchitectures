workspace {

    !identifiers hierarchical

    model {
        // Сепаратор слов
        properties { 
            structurizr.groupSeparator "/"
        }
        user = person "Пользователь" "Пользователь мессенджера"
        messenger = softwareSystem "Мессенджер" {

            // Описание Пользователя и сервиса
            user_service = container "Messenger app" "Приложение, с которым взаимодействует пользователь"
            identify_user = container "User service" "Сервис управления данными пользователя"
                description "Приложение мессенджера"
            
            // Блоки сервисов чатов (групповой + PtP)
            ptp_service = container "PtP chat service " "Сервис управления данными PtP чатов"
            chat_service = container "Group chat service" "Сервис управления данными групповых чатов"

            // блоки/контейнеры хранящие данные пользователей и чатов
            group "Слой данных"{

                // Описание контейнера с кэшем для хранения данных пользователя
                user_cash = container "User Cache" {
                description "Кэш пользовательских данных для ускоренного поиска по ключевым полям"
                technology "Redis/Memcache"
                tags "cache"
                }

                // Описание контейнера БД для хранения данных пользователя
                user_db = container "User Data" {
                    description "База данных пользователей"
                    technology "PostgreSQL"
                    tags "database"
                }

                // Описание контейнера БД для чатов
                chat_db = container "Chat Data" {
                    description "База данных для хранения сообщений общего и PtP чатов"
                    technology "MongoDB"
                    tags "database"
                }
            }

        }

        // Соединения пользователя  с сервисом    
        user -> messenger "Регистрация/ Написание сообщений/ Создание чатов"
        user -> messenger "Использование: регистрация, создание чатов, добавление в чат, PtP сообщения"

        user -> messenger.user_service "Регистрация/ Написание сообщений/ Создание чатов"
        
        messenger.user_service -> messenger.identify_user "Регистрация нового пользователя"
        messenger.identify_user -> messenger.user_db "Поиск/Добавление пользователя"
        messenger.identify_user -> messenger.user_cash "Получение/ обновление данных пользователя"
        messenger.user_service -> messenger.ptp_service "Написание сообщения"
        messenger.user_service -> messenger.chat_service "Создание чата/ написание сообщения"
        messenger.ptp_service -> messenger.chat_db "Запрос на получение данных чата"
        messenger.chat_service -> messenger.chat_db "Запрос на получение данных чата"
        

        deploymentEnvironment "Deploy" {
            deploymentNode "Пользовательский сервис" {
                containerInstance messenger.user_service
            }
            deploymentNode "Сервис для определения пользователя" {
                containerInstance messenger.identify_user
            }
            deploymentNode "PtP чат сервис" {
                containerInstance messenger.ptp_service
            }
            deploymentNode "Сервис для группового/общего чата" {
                containerInstance messenger.chat_service
            }
            deploymentNode "Кэшированные данные пользователей" {
                containerInstance messenger.user_cash
            }
            deploymentNode "База данных пользователей сервиса" {
                containerInstance messenger.user_db
            }
            
            deploymentNode "База данных для хранения данных чатов" {
                containerInstance messenger.chat_db
            }
        }

    }

    views {
        // Дефолтный стиль
        themes default
        
        // Вывод контекстной диаграммы
        systemContext messenger {
            include *
            autoLayout
        }
        // Вывод диаграммы контейнеров
        container messenger {
            include *
            autoLayout
        }

        deployment messenger "Deploy" "deployment" {
             include *
             autoLayout
        }

        dynamic messenger "UC01" "Создание нового пользователя" {
            autoLayout
            user -> messenger.user_service "Создать нового пользователя (POST /user)"
            messenger.user_service -> messenger.identify_user "Проверка уникальности логина"
            messenger.identify_user -> messenger.user_db "Сохранение данных пользователя"
            messenger.identify_user -> messenger.user_cash "Кэширование данных пользователя"
        }

        dynamic messenger "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> messenger.user_service "Найти пользователя по логину (GET /user)"
            messenger.user_service -> messenger.identify_user "Перенаправление запроса"
            messenger.identify_user -> messenger.user_cash "Получение данных о  пользователе из кэша"
            messenger.identify_user -> messenger.user_db "Получение данных о пользователе"
        }

        dynamic messenger "UC03" "Поиск пользователя по маске имя и фамилии" {
            autoLayout
            user -> messenger.user_service "Найти пользователя по маске (GET /user)"
            messenger.user_service -> messenger.identify_user "Перенаправление запроса"
            messenger.identify_user -> messenger.user_db "Получение данных о  пользователе"
        }

        dynamic messenger "UC11" "Создание группового чата" {
            autoLayout
            user -> messenger.user_service "Запрос на создание чата (POST /users_chat)"
            messenger.user_service -> messenger.chat_service "Перенаправление запроса"
            messenger.chat_service -> messenger.chat_db "Сохранение данных чата"
        }

            dynamic messenger "UC12" "Добавление пользователя в групповой чат" {
            autoLayout
            user -> messenger.user_service "Запрос на добавление пользователя в груповой чат (POST /user/users_chat)"
            messenger.user_service -> messenger.chat_service "Перенаправление запроса"
            messenger.chat_service -> messenger.chat_db "Сохранение и обновление данных чата"
        }

            dynamic messenger "UC13" "Добавление сообщения в групповой чат" {
            autoLayout
            user -> messenger.user_service "Запрос на проверку наличия пользователя в чате, добавление сообщения в чат (POST user/user_chat/message)"
            messenger.user_service -> messenger.chat_service "Перенаправление запроса"
            messenger.chat_service -> messenger.chat_db "Сохранение и обновление данных чата"
        }

            dynamic messenger "UC14" "Загрузка сообщений группового чата" {
            autoLayout
            user -> messenger.user_service "Запрос на поиск сообщений чата (GET user/user_chat/message)"
            messenger.user_service -> messenger.chat_service "Перенаправление запроса"
            messenger.chat_service -> messenger.chat_db "Получение данных о сообщениях пользователя из чата"
        }

            dynamic messenger "UC21" "Отправка PtP Сообщений пользователю" {
            autoLayout
            user -> messenger.user_service "Запрос на отправку сообщения в PtP чате, добавление сообщения в чат (POST user/ptp_chat/message)"
            messenger.user_service -> messenger.chat_service "Перенаправление запроса"
            messenger.chat_service -> messenger.chat_db "Сохранение и обновление данных чата"
        }

            dynamic messenger "UC22" "получение PtP списка сообщения для пользователя" {
            autoLayout
            user -> messenger.user_service "Запрос на поиск сообщений PtP чата (GET user/ptp_chat/message)"
            messenger.user_service -> messenger.chat_service "Перенаправление запроса"
            messenger.chat_service -> messenger.chat_db "Получение данных о сообщениях пользователя из чата"
        }

        styles {
            element "database" {
                shape cylinder
                background #15D600
                color #000000
            }
        }
        styles {
            element "cache" {
            shape cylinder
            background #FEE83D
            color #000000
            }

        }
    }

}
