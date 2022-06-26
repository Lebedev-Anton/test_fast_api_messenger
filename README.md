Преамбула:
Представьте себе, что вы с вашим ноутбуком оказались в начале 90х.
Каким-то чудом, на нем через VPN работает связь с современным интернетом, однако кругом интернет еще преджний -- научный.
К вам, внезапно, пристает толпа ученых, которые вас, якобы, хорошо знают и слезно просят сделать чудо -- гипертекстовый FIDO! 
И работать он должен уже не peer-to-peer, а через общий сервер, способный обслуживать тысячи запросов.
Они говорят, что консольный клиент для него уже на половину написан, но весь сетевой обмен с радостью переведут в API, построенном на суперсовременном, на тот момент, протоколе HTTP.
FIDO должен уметь создавать комнаты для общения двух и более участников.
Сами участники почти не имеют авторизации -- для входа нужно просто написать свой валидный email-адрес.
Ученые еще очень хотели организовать обмен документами, но их вовремя остановили, и показали язык HTML.
Однако, ссылки на документы тоже можно пересылать и даже как-то оформлять их (повторюсь, консольный клиент они сами напишут).

Задача:
Написать сервис, API которого бы позволил делать следующие вещи:
- регистрироваться и авторизовываться, указав валидный email-адрес
- видеть список пользователей в системе (без статуса онлайн)
- писать одному пользователю
- читать сообщения этого пользователя по отношению к вам
- создавать групповые чаты
- показывать список групповых чатов 
- писать в них сообщения и читать сообщения других
- да, конечно же предполагается некий режим long polling-а, никаких WebSockets

Особенности:
* сборку сервиса необходимо произвести на фреймворке FastAPI
* предположим все-таки наличие БД хотя бы в виде SQLite 
* работу с БД желательно выстроить с помощью SQLAlchemy
* для сервиса нужно сделать внятную схему данных 
* а для эндпоинтов API описать модели и типы 
* бизнес-логику можно сделать "большими мазками", потому что главное увидеть как вы мыслите
* но, все равно, будет здорово если она будет работать :)
--