# Краткое руководство V4

Передайте результат, критерии приёмки, известные контракты и нужный scope. Root сам исследует доступные факты, держит Plan + Goals + Progress и спрашивает пользователя только о решениях, которые действительно принадлежат человеку.

## Как работает V4

Terra High сохраняет роль Root: он определяет WHAT, разбивает работу, координирует исполнителей, интегрирует результат и легко принимает отдельные Goals. Это не заменяет финальную приёмку stage/capability: её после integration, нужного review/rework и Luna validation выполняет read-only Terra High Gate. Root затем действует по решению Gate и сообщает принятый результат.

Главное дополнение V4 — Luna Medium Scout. Его запрашивают только если implementation seam, поток, тесты или существующие паттерны ещё не образуют достаточно узкую карту для Astra. Scout не пишет код и возвращает ограниченный `RESEARCH_CAPSULE`; при понятной поверхности fast path остаётся без Scout.

Публичное имя стабильно между версиями: используйте `@Orchestrate Development`. Внутренние имена пакета и профилей остаются versioned, чтобы установка и переход с V3 были предсказуемыми. Краткая эволюция V3 → V4 приведена в [CHANGELOG.md](CHANGELOG.md).

Для известной поверхности fast path остаётся первым: Terra -> narrow Goal -> Astra -> implementation -> review when warranted -> validation -> gate. Когда поиск implementation seam, flow, tests или existing patterns заметно расширил бы контекст Astra, Root, Astra или Gate могут запросить read-only Luna Medium Scout. Scout возвращает `RESEARCH_CAPSULE`, не код и не архитектурное решение.

Repair, Reviewer, Validator и Scout не используют Scout. После установки используйте `scripts/upgrade_from_v3.py` для opt-in перехода с V3; сначала запуск без `--apply` покажет все действия.
