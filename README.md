# Learning project

## 💡 Idea
This project is generaly about non-standart (mb not the best, but still much more enjoyable) practical application of gained knowledge. "Non-standart? What do you meen by that?" - when you learn smth the best way to memorize that is to apply it on practice. This is BASA. And the most common way to do so is to make some small tasks/projects, based on few techs/topics... But thats actually quite boring...

Thats why Im trying to create giant project, with multiple levels of abstracts, which indcludes much more than "few techs and topics", and (hopefully) make it work.

## 🤔 What can you find there (short description)

_short remark: now everything is on python_
1. Custom ASGI-Compatible (not so) web-server on asyncio (+ some kind of multiprocessing)
2. FastAPI web-app

## 📋 Project scheme
_Not accurate scheme, just for personal usage_
https://www.figma.com/design/6DTnJpbMxJkoQ5ZYqhhfiJ/project_scheme?node-id=0-1&t=vvy0Mzm48XP94oce-1


## 📚 Resourses & Covered Topics List

_techs from this list is implemented in project in some way_

1. asyncio (main source - M.Fowler (asyncio & concerrunt bla-bla-bla))
    - basics
    - sockets & asyncio
    - streams
    - protocols
    - asyncio & multiprocessing

2. Web-server (asgi-comp) architecture (main source - uvicorn source code + asgi spec)

_if the truth be told, the way custom server designed is not the way it built in uvicorn, but who cares :3_

3. Protocols
    - HTTP/1.0 (only :C)

4. Frameworks
    1. FastAPI
        - just basics (includes pydantic)

5. Smth bout db
    1. python & sql (with sqlalchemy+alembic)

6. Patterns (no builtins)
    - uwu ^.^ (uow & repo, sql+api)
    - Producer-Consumer (master process --socket-> Queue -> subprocesses)

    _Will transition to Master-Worker in future_

## Ala finale

_#TODO: change the text so it can be assosiated with cur project_

Ну и чисто для поднятия настроения, когда будешь садиться за проект, вспомни слова классика:

"Короче, Программист, я тут задокументировал и в благородство играть не буду: выполнишь для платформы пару заданий — и мы в расчете. Заодно посмотрим, как быстро у тебя башка после этого сочного кода прояснится. А по твоей теме постараюсь разузнать. Хрен его знает, на кой ляд тебе эта платформа сдалась, но я в чужие дела не лезу, хочешь писать на js, значит есть за что...

Здесь у нас хранятся компоненты, которые определяют общую структуру страницы.
Хочешь сделать солидненькое левое меню, с основным контентом справа с менюшкой не в хеардере а в футере (больной ублюдок)? Значит тебе сюда, создавать новый layout. Проходи и присаживайся. 

Типичный признак layout'ов в том, что они включают вызов из props {children}, в котором должен содержаться основной контент, который требуется вписать в слой.
Основное отличие от hoc-ов типа Page заключается в том, что layout как правило достаточно "тупорылые", то есть не содержат логики связанной с запросами на сервер. Но если ты, мой маленький дружок, запихнёшь чуть чуть запросов в layout, то папа Захар тебя не будет сильно бить по твоей розовой попке, а поймёт и простит. 

Только следи, что бы эти твои запросики не влияли на другие компоненты, а только на те, что относятся непосредственно к layout, но не к children."