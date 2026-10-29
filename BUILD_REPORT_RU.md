# CONTROL1.3.1 — готовая пересобранная игра

22.10.2026. Основной результат — **готовый автономный HTML**, а не ещё один исходный патч. Пользователю Node/npm/пересборка не нужны.

## Установленное расхождение поставки
В папке `1wiXeGDRDh3eydm6U2nwaMPIN9UkAypoZ` готовый `payload/foundation/IRON_DUNGEON_FOUNDATION.html` имеет размер51 204 381байт и MD5 `e43106b82667e7535b00422fa5dcf3e1`. Это точное совпадение с standalone из1.1. Его embedded game JS также совпал с проверенным архивом. При этом все34 записи исходного manifest1.3 совпали с реконструированными исходниками1.3.

Следовательно, в папке были новые исходники, но **старый готовый HTML**. В нём осталась старая policy: после240 samples при плохих frame timings автоматически переключать WebGL→Canvas. Взят именно этот архивный HTML с совпадающим MD5 и браузером подтверждён переход при синтетическом воспроизведении условий старого watchdog. Это подтверждённый механизм изменения вида карты, но не независимая телеметрия GPU исходного компьютера из видео.

Транспортное скачивание HTML через connector добавляло Cloudflare script attributes; такая изменённая транспортная копия НЕ использовалась для запуска. Использована проверенная байт-в-байт архивная копия, чей MD5 совпадает с метаданными Drive. Embedded JS обеих копий одинаков.

## Что сделано
- Проверенные07→08→10→11→12→13 исходники действительно собраны командой `npm run build:single`.
- Игра получила уникальные имя, title/meta и `IronDungeon.build = CONTROL1.3.1-20261022-REBUILT`.
- В build-single добавлена защита от выдачи старого bundle: обязательны pinned policy/build ID и отсутствие старой performance-fallback ветки.
- Старое поведение при падении FPS отсутствует в новом bundle. Медленные кадры дают warning без смены backend. Явный ручной режим и genuine context-loss/render-error fallback сохранены.
- Новых механик/графического редизайна не добавлено: сохранены игрок A, таблицы врагов/оружия и уже существующие изменения пещеры1.3.
- Все11 embedded resources декодированы и побайтно сопоставлены с `public/`; внешняя загрузка ассетов не требуется.

## Идентичность готового файла
`IRON_DUNGEON_CONTROL_13_1_PLAY.html`:
- bytes: **51 214 624**;
- MD5: **525580833b56c8d164748b2cb5c27795**;
- полный SHA256 — в SHA256SUMS.txt/artifact-check.json;
- API version foundation-0.1 намеренно не переименована; номер поставки — свойство build/title.

## Свежие проверки именно автономного файла
- Старый HTML с совпадающим MD5: старый synthetic slow-frame trigger действительно сменил WebGL на Canvas.
- Новый HTML: offline WebGL startup, title/build ID, тот же trigger без смены backend.
- **90 секунд** после trigger: прежний renderer/scene/green-player definition, один RAF; игрок оставался alive. Это wall-time stability session, не90s gameplay simulation на hardware GPU. В медленном SwiftShader наблюдались очень большие frame intervals; этот тест не доказывает60FPS.
- В WebGL: настоящие WASD/F8, E вход в пещеру,9 enemy models + player, прозрачный HUD; настоящий projectile вызвал live rock damage overlay; genuine context loss сохранил safety fallback. **Полная high-quality WebGL последовательность не завершена:** первая попытка завершилась kernelOOM при параллельной тяжёлой работе в2GB VM, вторая дошла до10 успешных проверок и остановилась на timeout screenshot после context-loss. Это не скрыто и не помечено полным pass.
- Отдельная последовательная offline Canvas-проверка **10/10**: startup, реальное движение/огонь, E вход, разрушение90HP глыбы мышью, удаление collider, проезд через открытый проход, E выход, отсутствие page/native-loop errors, disposal, default production entry без debug globals. AI не выключался, invulnerability не добавлялась; позиции/camera использовались как fixtures рядом с проверяемыми местами.
- Build/check pass:69 ESM/11 modules/32 provenance ports. Полный unit suite **76/78**, прежние два красных: whole-file SHA pin и old assertion, требующий именно запрещённого автоматического watchdog fallback. Assertions не менялись.

## Что не заявлено
Физический GPU/мобильные устройства,60FPS, hours-long soak и исправление всех аппаратных ошибок не квалифицированы. Ранее измеренная steady-state Canvas performance-регрессия1.3 не объявлена устранённой в этом rebuild. Genuine GPU context loss всё ещё может потребовать другого backend — это отдельный путь, не падение FPS.

## Запуск и откат
Распаковать готовый ZIP, открыть START.html → WebGL для объёмной графики либо автоматический безопасный выбор. Не запускать старый HTML/ярлык. Все ресурсы уже внутри игры. Вкладка должна содержать `CONTROL1.3.1 — REBUILT`.

Новые готовые файлы добавляются отдельно; исходные пользовательские файлы/сохранения не перезаписываются и не удаляются. Откат — открыть прежнюю сохранённую версию. Для разработчика отдельный source delta приложен только как обновление build identity/guard/памяти поверх1.3; это не требование к игроку.
