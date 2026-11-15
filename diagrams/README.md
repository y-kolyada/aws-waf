# Diagram sources

A diagram on a page is **inline SVG**, not an image file: the page must work from `file://`, and inline vector inherits the theme colour through `currentColor`, so it survives the day/night switch without a second copy. A shared `assets/NN.svg` would also show one language's labels on all four language pages. The full rule is `AGENTS.md` section 5 rule 18, and `node tools/check-diagrams.mjs` guards it.

This folder holds the **source** of each diagram in Mermaid: `NN-name.mmd`, where `NN` is the page the diagram lives on. Every source answers a diagram and every diagram answers a source; the check says so out loud when they drift apart.

The SVGs embedded in the course pages are drawn strictly conforming to the Mermaid sources below and validated via `node tools/check-diagrams.mjs`.

| Source | Page | What it shows |
| :-- | :-- | :-- |
| `index-perimeter.mmd` | `ru/index.html` | Схема 1. Эшелонированный периметр AWS WAFv2: Anycast Edge, Regional VPC и аналитика. |
| `01-evaluation-priority.mmd` | `ru/01.html` | Схема 2. Конвейер последовательной оценки правил Web ACL и емкость WCU. |
| `02-scopes-associations.mmd` | `ru/02.html` | Схема 3. Топология областей видимости Scope: CLOUDFRONT против REGIONAL. |
| `03-managed-rules-hierarchy.mmd` | `ru/03.html` | Схема 4. Иерархия пакетов правил AWS Managed Rules и механизм переопределений. |
| `04-custom-inspection-pipeline.mmd` | `ru/04.html` | Схема 5. Конвейер инспекции кастомного правила: FieldToMatch и предикаты. |
| `05-rate-limiting-sliding-window.mmd` | `ru/05.html` | Схема 6. Динамическое скользящее окно Rate-based правила и составной ключ. |
| `06-actions-verdict-decision.mmd` | `ru/06.html` | Схема 7. Матрица вердиктов Action: терминирующие действия и браузерные испытания. |
| `07-bot-control-challenge-flow.mmd` | `ru/07.html` | Схема 8. Поведенческий анализ Bot Control и генерация токена WAF Token. |
| `08-streaming-logging-pipeline.mmd` | `ru/08.html` | Схема 9. Потоковый конвейер доставки логов через Kinesis Data Firehose в S3. |
| `09-staged-rollout-lifecycle.mmd` | `ru/09.html` | Схема 10. Жизненный цикл безопасного релиза правил (Staged Rollout). |
| `10-noob-perimeter-stack.mmd` | `ru/10.html` | Схема 11. Базовый эшелон защиты Noob: IP Allowlist, CRS и изоляция /admin. |
| `11-pro-jwt-rate-limit.mmd` | `ru/11.html` | Схема 12. Продвинутая архитектура Pro: JWT Rate Limiting и интеграция ATP. |
| `12-igl-soar-auto-mitigation.mmd` | `ru/12.html` | Схема 13. Автоматизированный контур SOAR и реагирование на L7-инциденты. |
| `13-assessment-noob-tree.mmd` | `ru/13.html` | Схема 14. Дерево квалификационной оценки Noob: базовые понятия и синтаксис. |
| `14-assessment-pro-pipeline.mmd` | `ru/14.html` | Схема 15. Профиль компетенций Pro: поведенческий контроль и автоматизация. |
| `15-assessment-igl-governance.mmd` | `ru/15.html` | Схема 16. Системное лидерство IGL: корпоративное управление и SRE-практики. |
| `navigator-lenses.mmd` | `ru/navigator.html` | Схема 17. Девять инженерных линз вокруг архитектурного ядра AWS WAFv2. |
