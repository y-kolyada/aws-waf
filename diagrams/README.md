# Diagram sources

A diagram on a page is **inline SVG**, not an image file: the page must work from `file://`, and inline vector inherits the theme colour through `currentColor`, so it survives the day/night switch without a second copy. A shared `assets/NN.svg` would also show one language's labels on all four language pages. The full rule is `AGENTS.md` section 5 rule 18, and `node tools/check-diagrams.mjs` guards it.

This folder holds the **source** of each diagram in Mermaid: `NN-name.mmd`, where `NN` is the page the diagram lives on. Every source answers a diagram and every diagram answers a source; the check says so out loud when they drift apart.

The SVGs embedded in the course pages are drawn strictly conforming to the Mermaid sources below and validated via `node tools/check-diagrams.mjs`.

| Source | Page | What it shows |
| :-- | :-- | :-- |
| `index-perimeter.mmd` | `ru/index.html` | Архитектура эшелонированного периметра: Edge PoP CloudFront, региональные VPC и AWS Shield. |
| `01-evaluation-priority.mmd` | `ru/01.html` | Каскад приоритетов правил Web ACL и шкала бюджета емкости WCU. |
| `02-scopes-associations.mmd` | `ru/02.html` | Архитектурный мост областей видимости Scope: CLOUDFRONT против REGIONAL. |
| `03-managed-rules-hierarchy.mmd` | `ru/03.html` | Иерархия AWS Managed Rules и три механизма управления переопределениями. |
| `04-custom-inspection-pipeline.mmd` | `ru/04.html` | Четырехуровневый конвейер инспекции: от извлечения полей до логических предикатов. |
| `05-rate-limiting-sliding-window.mmd` | `ru/05.html` | Замкнутый контур скользящего окна Rate Limiting с петлей восстановления. |
| `06-actions-verdict-decision.mmd` | `ru/06.html` | Дерево пяти терминальных и нетерминальных действий правил Web ACL. |
| `07-bot-control-challenge-flow.mmd` | `ru/07.html` | Пошаговый протокол Silent Challenge: JavaScript SDK и выдача крипто-токена. |
| `08-streaming-logging-pipeline.mmd` | `ru/08.html` | Топология звезда (Hub-and-Spoke): шина логирования и каналы доставки. |
| `09-staged-rollout-lifecycle.mmd` | `ru/09.html` | Пирамида стадий безопасного релиза правил от Count к Enforce Block. |
| `10-noob-perimeter-stack.mmd` | `ru/10.html` | Ступени эшелона Noob: IP Allowlist, CRS сигнатуры и лимиты размера. |
| `11-pro-jwt-rate-limit.mmd` | `ru/11.html` | Матрица защитных механизмов уровня Pro: 2x2 квадранта с центральным хабом. |
| `12-igl-soar-auto-mitigation.mmd` | `ru/12.html` | Автономный контур реагирования SOAR: замкнутый цикл самовосстановления. |
| `13-assessment-noob-tree.mmd` | `ru/13.html` | Иерархическое дерево квалификационного банка Noob: 5 тематических ветвей. |
| `14-assessment-pro-pipeline.mmd` | `ru/14.html` | Сетевая топология компетенций инженера Pro: перекрестные связи пяти доменов. |
| `15-assessment-igl-governance.mmd` | `ru/15.html` | Корпоративное управление безопасностью: AWS Firewall Manager и мультиаккаунт. |
| `navigator-lenses.mmd` | `ru/navigator.html` | Матрица 3x3 девяти инженерных линз вокруг архитектурного ядра WAFv2. |
