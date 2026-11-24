zapis: Django, custom User and Docker

Created by Concept Loom on 2026-10-23T14:37:36.700Z

> [!note] Custom User: timing checkpoint
> 
> Checkpoint пройден: первая миграция создаёт auth_user и внешние ключи на неё; смена AUTH_USER_MODEL позже не переименует таблицу и не перестроит связи. Поэтому своя модель задаётся до первого migrate.

> [!note] PROTECT: направление защиты
> 
> Checkpoint: приom on 2026-10-23Tсapis: Django, custom  если на роль ссылаются пользователи, Django выбрасывает ProtectedError; роль и пользователи остаются. PROTECT защищает роль от удаления, а не пользователя. CASCADE удалил бы пользователей, SET_NULL обнулил бы ссылку.

> [!note] Пауза: PostgreSQL и Docker впереди
> 
> Сохранено 23 октября. Готово: кастомный User с username-логином, Role FK с PROTECT, AUTH_USER_MODEL, миграция 0001_initial.py. Осталось: DATABASES на PostgreSQL через POSTGRES_* из .env, Dockerfile/.dockerignore/compose.yml, первый migrate в контейнере, начальные роли, createsuperuser и проверка админки. При возобновлении сначала прочитать settings.py и проверить наличие .env, не выводя значения.

> [!note] Роадмапа ред. 23.10: рамки zapis
> 
> Источник: сайт роадмапы, вкладка «Код» (прочитано 2026-10-27).
> 
> - Приоритеты: Voluma → фриланс → zapis. zapis получает ~4.5 ч/нед; минимум 25 мин/день (одна из пяти галочек дня).
> - К 27 декабря в zapis: модели + админка + seed; каталог и расчёт свободных окон; запись с ExclusionConstraint и ответом 409; JWT и роли; 3–5 ключевых тестов на pytest; VPS, Nginx, HTTPS, бэкап, Swagger; README по-английски и кейс.
> - Уехало в январь: Celery и напоминания, CI на GitHub Actions, страница на Next.js, N+1 с цифрами, полная матрица прав, factory_boy/freezegun, notify на FastAPI.
> - Учебный цикл: зачем (что сломается без фичи) → читать 15–20 мин → первая версия в проект → сломать → объяснить вслух. Нейросеть — ментор, не решатель.
> - Режим: ноутбук закрыт в 22:00, телефон вне спальни в 23:00, сон в 23:30.
> - Отставание от старого плана ~2.5 недели; план пересобран под реальный темп, а не догоняется.

> [!note] Пауза внутри WorkingHours (карточка 2)
> 
> Точка остановки 2026-10-27: дописан class WorkingHours,zapis: Dне написан.
> 
> Готово в файле:ocker

Creatzapis: Djanzapis: Django, c(поля), внутреннийtom User and Docker

Created0..6.
> Осталось:stom User and Docker
zapis: Djanzapis: Djan(+pis: Django, custom User and Docker

> 
> Замечания на возобновление:
> 
> - Опечатка в имени члена enum:6-10-23T14:3→apis: Djang
> -s: Djangzapis: Django, custom User and Docker

Created by Concept Loom on +apis: Django, custom User and Docker

Crea
> - Порядок:, custom User and Docker

Created by Concept 

> [!note] Карточка 2: модели и ограничения проверены на живой базе
> 
> Миграция:36.700Zприменена. Ограничения проверены вставками, а не чтением каталога:
> 
> - валидные часы (пн 10:00–12:00) создались — id=1;
> - часы с концом раньше начала отвергнуты:ed by Concept Loom on 2026-10-23T14:37:36.700Z

> [!note] Cust
> - повтор слота пн 10:00 отвергнут:

Created by Concept Loom on 2026-10-23T14:37:36.700Z

> [!note] Custom User: 
> 
> Вывод:o, custom User and D— это реальный DDL в Postgres, а не проверка в Python. Обойти нельзя ни через14:37:36. ни черезango, custom Us
> 
> Осталось по карточке 2: админка (`UserAdmin` +ncept Lo inlines услуг и часов), командаocker

C проверкаango, custom User aиapis: Django, custпри удалении услуги с записью.

> [!note] 2026-11-04 — Admin verified, Card 2 closed
> 
> Session restored (zapis-core, rev 53). Admin file checked against code.
> 
> Learner evidence:
> 
> - C1 (fieldsets is the whole form, not a patch list) — accurate.
> - C2 (add page uses add_fieldsets, separate description) — accurate.
> 
> Code notes on users/admin.py (minor, not blocking):
> 
> - ExecutorAdmin.list_display includes bio (TextField) — long text in a column; drop it or use a short method.
> - User.**str** returns email while admin columns show username — cosmetic inconsistency, keep in mind later for logs.
> 
> Next: seed management command (idempotent), then break tests for Booking.
clean() and ProtectedError.

> [!note] Seed: что это и зачем (2026-11-04)
> 
> seed — не аббревиатура, от англ. to seed «сеять». «Засеять базу» = наполнить пустую БД начальными данными.
> 
> Два вида данных в сиде:
> 
> - reference data: роли tutor/student — нужны на каждом стенде, включая прод;
> - demo data: исполнитель, услуги, часы работы — для разработки, тестов и показа.
> 
> Не миграция (та меняет схему), не fixture/loaddata (статичный JSON-дамп), не pytest-фабрика.
> Требование: идемпотентность через get_or_create — повторный запуск не падает и не плодит дубли.
> 
> Порядок вставки задан FK: Role -> User -> Executor -> Service / WorkingHours.

> [!note] PAUSE 2026-11-04 — resume point: seed command
> 
> ## Где остановились
> 
> Стек поднят после переустановки Windows. В базе: roles=0, users=1 (superuser), executors=1.
> Понятия сида и идемпотентности закрыты чекпоинтами (оба accurate). Код ещё не написан.
> 
> ## Что сделать при возврате
> 
> Создать три файла:
> 
> - users/management/**init**.py
> - users/management/commands/**init**.py
> - users/management/commands/seed_demo.py
> 
> В handle():
> 
> 1. Role tutor/student через get_or_create по name.
> 1. Демо-пользователь demo_tutor с role=tutor (пароль — через set_password или create_user, не в defaults).
> 1. Executor.objects.get_or_create(user=demo_user, defaults={“specialization”: …}).
> 1. Две Service: разные duration_minutes и format (offline/online), цена Decimal. Ключ (executor, title).
> 1. 1-2 WorkingHours, start_time < end_time, weekday через WorkingHours.Weekdays.Monday. Ключ (executor, weekday, start_time).
> 1. self.stdout.write со сводкой.
> 
> ## Проверка
> 
> docker compose exec web python manage.py help seed_demo
> docker compose exec web python manage.py seed_demo   (дважды — идемпотентность)
> 
> ## После этого
> 
> Break-тесты: Booking.clean() с чужим исполнителем -> ValidationError; удаление Service с бронью -> ProtectedError.
> Затем карточка 3: DRF-каталог.

> [!note] 2026-11-17 — seed: services done, WorkingHours pending verification
> 
> ## Что закрыто
> 
> Services block — доказано живыми прогонами:
> 
> |Прогон|Услуга 1|Услуга 2|
> |------|--------|--------|
> |1-й   |создана |создана |
> |2-й   |найдена |найдена |
> 
> БД: «Математика 90 минут» 90 / 1000.00 / offline, «Геометрия 60 минут» 60 / 8000.00 / online. Мусорная строка с пустым title удалена.
> 
> ## Три правила, выведенные из своих же ошибок
> 
> 1. lookup опознаёт, defaults рождает. Поля из lookup определяют, та ли это строка; defaults записываются только при создании и никогда не синхронизируются повторно (get_or_create).
> 1. Поля из UniqueConstraint модели = lookup. Для WorkingHours это (executor, weekday, start_time) — механически, без гадания. Для Service уникального ограничения нет, ключ (executor, title) выбран осознанно.
> 1. Код, работающий на текущих данных, ещё не доказан. Признак неполного ключа — второй легитимный набор значений для поля, оставшегося в defaults: он молча проглатывается с created=False.
> 
> ## Типы choices
> 
> - TextChoices: член является str-подклассом, Service.Format.ONLINE == “online”. В колонку идёт значение, метка только для отображения. Строка “ONLINE” не пройдёт валидацию choices.
> - IntegerChoices: член является int-подклассом, Weekdays.Monday == 0. Нумерация в модели с нуля, не ISO.
> - get_FOO_display() генерируется метаклассом по имени поля для каждого поля с choices: weekday -> get_weekday_display(), status -> get_status_display(). Имя класса STATUS/Weekdays роли не играет. Если значения нет в choices, возвращается само значение. Источник: Django 5.2 Model instance reference, Extra instance methods (проверено на 5.2.18).
> 
> ## Осталось на следующий раз
> 
> - Добавить третий слот понедельник 18:00–20:00: это тест на опровержение, без него полный ключ не доказан.
> - Исправить латинские c/o (0x63/0x6f) в словах «coздан…» — 4 сообщения.
> - Удалить артефактную строку расписания исполнителя dihh.online@mail.ru.
> - Итоговые счётчики в конце handle().
> - Break-тесты: Booking.
clean() с чужим исполнителем, ProtectedError при удалении услуги с бронью.

> [!note] 2026-11-19: constraint scope vs lookup scope (misconception found)
> 
> Checkpoint on adding Mon 18:00-20:00 alongside Mon 10:00-18:00 answered ‘IntegrityError from unique constraint’. Misconception: one row per executor per weekday.
> 
> Ground truth from migration 0002 / models.py:
> 
> - Constraint unique_working_hours_slot = (executor, weekday, start_time).ker

Createdis NOT part of it.
> - So two Monday rows coexist if start_time differs; only the same (executor, weekday, start_time) triple is rejected.
> - Same tuple governs the get_or_create lookup, which is why the third call creates a row rather than matching Mon 10:00.

> [!note] 2026-11-19: constraint equality rule secured + guide correction (DB INSERT vs get_or_create)
> 
> Learner derived the rule correctly on the third try: UniqueConstraint(fields=[executor, weekday, start_time]) fires only when ALL THREE match; a differing weekday makes a new row even with identical times.
> 
> GUIDE CORRECTION: my earlier phrasing ‘Mon 10:00-16:00 падает с IntegrityError’ was wrong at the command level. working_hours() uses get_or_create with lookup (executor, weekday, start_time), so Mon 10:00-16:00 MATCHES the existing Mon 10:00-18:00 row and returns created=False - no INSERT, no error, end_time unchanged. The IntegrityError would only appear on a raw WorkingHours.objects.create(…) with the same triple.
> 
> Two layers, do not merge them:
> 
> - DB constraint: rejects an INSERT whose triple duplicates an existing row.
> - get_or_create helper: never reaches the INSERT because the lookup already matched; extra fields in defaults are silently dropped.

> [!note] 2026-11-19: learner rule for this coach
> 
> Learner explicitly forbade doing the work for them: ‘do not do anything for me, only direct and hint, and above all do not give me the complete solution until I ask or arrive at it myself’.
> 
> Consequences for all future turns in this session:
> 
> - No full code patches, no ready commands, no complete answers to implementation tasks.
> - Hints in layers: (1) which layer/field is involved, (2) what to compare or predict, (3) only on explicit request - the concrete solution.
> - Checkpoints and questions stay the default mechanism; the learner runs the code and reports output.
> - The guide’s own error on 2026-11-19 (claiming Mon 10:00-16:00 raises IntegrityError) is a reminder to verify the helper layer, not just the model layer.

> [!note] 2026-11-19: отказ тратить время на орфографию в выводе seed
> 
> Learner challenged the priority of the Latin c/o fix in seed messages: ‘why should I bust my ass on orthography right now’. Verdict accepted: the string fix is a cosmetic defect ticket, not a learning connection and not a blocker for the 27 Dec goal. Demoted to BACKLOG, keep it out of the route. Only stated reason to do it at all: a mixed-alphabet string is invisible to a text search for ‘создан’, so any later grep/verification of seed output silently misses those lines.

> [!success] 2026-11-19: run 1 вывода seed после добавления третьего вызова
> 
> Learner ran the command themselves. Output: roles/users/executor/services all found; Рабочие часы Понедельник 10:00-18:00 найдены; Вторник 12:00-20:00 найдены; Понедельник 18:00-20:00 созданы.
> 
> This confirms the constraint rule at DB level: a second Monday row with a different start_time is legal and get_or_create created it. Half the disproof is done. Remaining: run 2 must print найдены for that row, and the row count must be checked by an independent path (ORM/admin/SQL), not by the command’s own messages.

> [!success] 2026-11-19: проверка через админку вместо БД
> 
> Learner reported: the new row is visible in admin; the stray artifact row is not visible in admin.
> 
> Teaching point: admin is a query/view layer. WorkingHours is registered as an inline under Executor, so a row appears only on the page of its parent Executor. ‘Absent in admin’ therefore does not prove ‘absent in DB’ - it may mean the parent page was never opened.
Same lesson as the run-1 print: a report is not the data.

> [!note] 2026-11-19: disproof-тест пройден (2 прогона + независимый счёт)
> 
> Run 1: Mon 18:00-20:00 созданы. Run 2: все строки найдены. Итог: 3 строки WorkingHours, все принадлежат tutor (Mon 10-18, Mon 18-20, Tue 12-20).
> 
> What this proves: the get_or_create lookup triple (executor, weekday, start_time) is complete for these demo rows - a second Monday row is created once and then found, so created=True appears exactly once. The constraint permits it because start_time differs.
> 
> Also settled: WorkingHours appears in admin only as an inline of Executor, so an empty screen means ‘wrong parent page’, not ‘no row’. The artifact executor and its hours were removed by the learner via the CASCADE chain user -> executor -> working_hours.

> [!note] 2026-11-19: дизайн счётчиков — возвращать created, а не считать по БД
> 
> Learner answered the three design questions:
> 
> 1. Helpers currently return the object (user, executor) or nothing; created is not propagated.
> 1. Chose to return created from each helper rather than counting rows in the DB, because a DB count cannot distinguish rows created by this run from pre-existing ones. Correct reasoning.
> 1. Predicted 10 created rows on an empty DB. Correct: 2 roles + 2 users + 1 executor + 2 services + 3 working hours.
> 
> Open detail to raise next: returning a pair changes every call site that reuses the object (tutor_user feeds executor), and the accumulation must cover calls made in sequence, not just the first one.

> [!success] 2026-11-19: счётчик врёт на единицу — разбор
> 
> Observed: populated DB run announces найдено everywhere, yet prints ‘Записей создано: 1. Записей найдено: 9’.
> 
> Diagnosis (guide): the counter contradicts its own messages, so exactly one branch incremented on the found path. Line 17 does if self.user(email="student@student.com", role="student"): while user() now returns (user, created). A non-empty tuple is always truthy, so that call adds 1 regardless of created. The other two tuple-returning call sites were unpacked properly (lines 20-28), which is why only one extra appears.
> 
> Second defect in the same block: found = 10 is hardcoded; found is computed as 10 - created, so it is a second source of truth that breaks as soon as the number of calls changes.

> [!note] 2026-11-19: итог дня и статус блока seed
> 
> Closed today: constraint equality rule + layering (constraint vs get_or_create) restored and secure; disproof test passed on two runs (Mon 18:00-20:00 created once, then found); counter design agreed and implemented.
> 
> Code state at pause: users/management/commands/seed_demo.py modified (line 17 fixed to self.user(…)[1]), working tree otherwise clean, last commit e420ea2. Counters not yet re-run, so the fix is unverified. found = 10 remains hardcoded.
> 
> Verdict: seed is functionally complete but not closed - one verification run and the found derivation are outstanding.

> [!note] 2026-11-19: seed закрыт двумя прогонами (пустая и заполненная БД)
> 
> Empty DB: 10 created / 0 found, every block ‘создана/создан/созданы’.
> Second run on the same DB: 0 created / 10 found, every block ‘найдена/найден/найдены’.
> 
> Conclusion: counters match reality on both paths, the truthiness bug is gone, idempotency holds across all blocks including Mon 18:00-20:00. Seed work for Card 2 is complete.
> 
> Known debt left in the file: found = 10 is still a hardcoded total, so the ‘found’ figure is only true while the number of calls stays at 10. Not a blocker for committing.

> [!note] 2026-11-19: перенос счётчиков в helper’ы и ошибка области видимости
> 
> Learner implemented option C (accounting inside helpers) but left the counters as locals declared in handle(). Two defects:
> 
> 1. func_count += 1 inside a method binds the name as a local of that method, so the first read raises UnboundLocalError.
> 1. Even if it did not raise, each helper would own a private counter; handle() would still print 0 / 0.
> 
> Fix: counters must live on the instance (self.rows_created, self.
func_count), initialised at the top of handle() and printed at the end. This is the same principle as the seed itself: one owner per piece of state.

> [!note] 2026-11-19: блок seed закрыт, счётчики работают
> 
> Final shape: self.func_count incremented on entry to each helper, self.rows_created incremented where created is True, both initialised in handle(), summary prints rows_created and func_count - rows_created. No per-call-site duplication, no hardcoded total.
> 
> Lesson of the day, worth keeping: the same bug appeared three times in different clothes - a tuple believed to be a bool, a hardcoded total believed to be a count, a local variable believed to be shared state. Each time the command’s own output looked confident.

> [!note] 2026-11-24: стиль объяснений по просьбе ученика
>
> Learner asked: explanations shorter and plainer from now on. Keep one idea per message, plain words, no long build-ups. Applies to all later turns.

> [!note] 2026-11-24: окружение — Docker недоступен, локальный Postgres через db-start
>
> Docker daemon на рабочем месте не запускается и недоступен. БД поднимается командой `db-start` (локальный Postgres, 127.0.0.1:5433 по .env). Проверено: порт 5433 отвечает, `showmigrations users` показывает 0001 и 0002 применёнными. Тесты запускать через `uv run python manage.py test` — Django создаст отдельную test_zapis_db. Все прежние инструкции с `docker compose exec` считать устаревшими для этой машины.

> [!note] 2026-11-24: ответ a верный — full_clean проверяет и constraints
>
> Checkpoint: end раньше start + full_clean() -> ValidationError будет, но из validate_constraints, а не из clean(). Тест оказался бы ложнозелёным. Ученик ответил a (верно).

> [!note] 2026-11-24: тест Booking.clean прошёл break-проверку
>
> Первая автоматическая Django-проверка написана учеником в users/tests.py. Она создаёт Booking с executor первого исполнителя и service второго; ORM create проходит, full_clean() ожидает ValidationError, есть assert по pk. Запуск: Ran 1 test, OK. Break-тест: ученик временно отключил проверку в Booking.clean() — тест упал (FAILED, 1 failure); проверку восстановил — тест снова прошёл. Вывод: тест действительно обнаруживает удаление правила. Следующий шаг: написать тест PROTECT для удаления Service с существующей Booking, затем break-тест с on_delete=CASCADE. Ученик попросил продолжить позже.
