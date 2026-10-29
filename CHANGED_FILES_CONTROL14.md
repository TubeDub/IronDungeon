# CONTROL1.4 — точные файлы патча

Пути относительно ROOT, содержащего foundation/. Только перечисленные файлы. DELETE: **0**. Хеши и допустимые базы — PATCH_MANIFEST_14.json.

## REPLACE: 26
- `foundation/README_RU.md`
- `foundation/docs/architecture/ARCHITECTURE.md`
- `foundation/docs/architecture/CHANGELOG.md`
- `foundation/docs/architecture/CURRENT_STATE.md`
- `foundation/docs/architecture/DEPENDENCIES.md`
- `foundation/docs/architecture/NEXT_SESSION.md`
- `foundation/docs/architecture/PROJECT_MAP.md`
- `foundation/docs/architecture/SOURCE_INDEX.json`
- `foundation/docs/architecture/WORKLOG.md`
- `foundation/docs/architecture/modules/environment-assets.md`
- `foundation/docs/architecture/modules/graphics-tanks.md`
- `foundation/docs/architecture/modules/lifecycle.md`
- `foundation/docs/architecture/modules/progression-scenes.md`
- `foundation/docs/architecture/modules/world-combat.md`
- `foundation/docs/native-provenance.json`
- `foundation/index.html`
- `foundation/scripts/build-single.mjs`
- `foundation/scripts/generate-native.mjs`
- `foundation/src/graphics/EnvironmentStone.js`
- `foundation/src/graphics/RuinsVisuals.js`
- `foundation/src/graphics/native/weapons/Weapon3D.js`
- `foundation/src/main.js`
- `foundation/src/session/SessionModule.js`
- `foundation/src/session/nativeSession.js`
- `foundation/src/ui/nativeHUD.js`
- `foundation/src/world/destructible/DestructibleSystem.js`

## ADD: 8
- `foundation/docs/control14-material.json`
- `foundation/public/art/control14_floor.jpg`
- `foundation/public/art/control14_floor_normal.png`
- `foundation/public/art/control14_floor_rough.png`
- `foundation/public/art/control14_floor_wet.png`
- `foundation/src/session/CampaignSession.js`
- `foundation/tests/control14.test.mjs`
- `foundation/tools/control14_material.py`

## Вспомогательные файлы поставки
`apply_control14.py`, `READY_131_TO_14_DELTA.json`, manifest/install/report/file list, QA evidence, rollback_originals для REPLACE. Они не копируются в game source. SOURCE_INDEX перечисляет весь graph для навигации, но в payload находятся только изменения. Браузерные saves не затрагиваются installer/rollback.
