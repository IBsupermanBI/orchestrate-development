# Orchestrate Development V4

Самостоятельный явный skill для substantial development: Terra High владеет WHAT, декомпозицией и лёгкой приёмкой Goals; Astra Low — реализацией; Luna Medium Scout — только дешёвым read-only mapping незнакомой поверхности; Luna XHigh — bounded repair и final validation; Sol Medium — независимым review. Scout опционален: при уже узкой карте Astra идёт напрямую к коду.

## Текущее состояние: V4

V4 сохраняет Terra High как Root: он владеет scope, декомпозицией, оркестрацией, интеграцией и лёгкой приёмкой отдельных Goal. Astra реализует выбранные Goals. Luna Medium Scout подключается только когда карте репозитория ещё не хватает узости для уверенного старта Astra: он возвращает read-only `RESEARCH_CAPSULE` и остаётся leaf-ролью.

Финальная приёмка отделена от приёмки Goals: Terra High Gate — read-only роль, которая принимает завершённый stage/capability после интеграции, требуемого review/rework и Luna final validation. Публичный вызов не зависит от версии: используйте `@Orchestrate Development`.

## Эволюция

V3 начинался с LunaMix как агента-оркестратора. Затем Root был перенесён на Terra High, чтобы контур scope, декомпозиции и интеграции оставался у роли, предназначенной для высокоуровневого управления. V4 сохраняет это решение и добавляет Luna Medium Scout: незнакомая поверхность исследуется отдельно и ограниченно, поэтому Astra получает достаточно узкую карту, а не расходует контекст на широкое первичное исследование.

Это не попытка сделать каждую задачу многоагентной: при уже понятной поверхности Scout пропускается. Краткая история релизов и обоснование ключевых изменений — в [CHANGELOG.md](CHANGELOG.md).

## Установка

Python 3.11+ и внешние зависимости не нужны:

```sh
python install.py --project /path/to/project
python install.py --project /path/to/project --apply
```

Первый вызов показывает только план. Проектная установка кладёт skill в `.agents/skills/orchestrate-development-v4/` и семь versioned profiles в `.codex/agents/`; `AGENTS.md`, hooks, Git и чужие файлы не меняются. При конфликте `--apply --force` сохраняет заменяемый файл в `.backups/`. Для user scope используйте `--user` (при необходимости `--home`).

### Переход с V3

Сначала проверьте план, затем примените безопасную миграцию:

```sh
python scripts/upgrade_from_v3.py --project /path/to/project
python scripts/upgrade_from_v3.py --project /path/to/project --apply
```

Она устанавливает V4, затем переносит известные V3 skill/profile assets и v3-only backup copies в `.agents/skills/archive-orchestrate-development-v3-pending-removal/<timestamp>/`. Эта папка намеренно помечена для ручной проверки и последующего удаления. Она не меняет `AGENTS.md`, hooks, Git и другие профили; mixed or non-V3 backup directories остаются на месте. Локальные изменения V3 сохраняются в том же архиве. Для user scope доступны `--user --home`; при конфликте существующей V4 добавьте `--force`. Обратный путь — вручную вернуть сохранённые файлы после проверки.

## Запуск

Выберите `gpt-5.6-terra` / `high`, затем используйте `@Orchestrate Development`. Роли и точные модели находятся в [SKILL.md](SKILL.md); наличие TOML не доказывает effective binding, поэтому host schema сверяется перед dispatch.

Пакет не зависит от Loop Review, hooks или telemetry и не публикует изменения сам. Проверка пакета: `python scripts/validate_package.py`; диагностика установленной копии: `python scripts/orchestration_doctor.py diagnose --project <project>`.
