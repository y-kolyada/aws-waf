#!/usr/bin/env python3
"""Generate 17 visually distinct, topologically diverse SVG diagrams and Mermaid sources for AWS WAF course."""

import os
import re

DIAGRAMS = {
    # 1. Multi-Layer Perimeter Defense Map (Edge + Dual VPC Compute + Shield Base)
    "ru/index.html": {
        "num": 1,
        "key": "index-perimeter",
        "title": "Архитектура эшелонированного периметра: Edge PoP CloudFront, региональные VPC и AWS Shield.",
        "aria": "Схема эшелонированного периметра AWS WAF: CloudFront, ALB, API Gateway и Shield Advanced",
        "h": 230,
        "mmd": """flowchart TD
    Traffic["Интернет-трафик"] --> CF["CloudFront Edge PoP (Global WAF)"]
    CF --> ALB["ALB + Regional WAF (EKS)"]
    CF --> APIGW["API Gateway + WAF (Lambda)"]
    ALB --> Shield["AWS Shield Advanced (L3/L4/L7)"]
    APIGW --> Shield
""",
        "svg": """  <rect x="30" y="8" width="260" height="26" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="25" text-anchor="middle" font-size="12" fill="currentColor">Входящий интернет-трафик</text>

  <line x1="160" y1="34" x2="160" y2="46" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,54 156,46 164,46" fill="currentColor"/>

  <rect x="30" y="54" width="260" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="70" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">CloudFront Edge PoP (Global WAF)</text>
  <text x="160" y="82" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Фильтрация атак на периферии сети</text>

  <path d="M 160 88 L 160 102 L 85 102 L 85 114" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="85,122 81,114 89,114" fill="currentColor"/>

  <path d="M 160 88 L 160 102 L 235 102 L 235 114" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="235,122 231,114 239,114" fill="currentColor"/>

  <rect x="15" y="122" width="140" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="85" y="140" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">ALB + WAF</text>
  <text x="85" y="154" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Контейнеры EKS</text>

  <rect x="165" y="122" width="140" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="235" y="140" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">API Gateway</text>
  <text x="235" y="154" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Lambda функции</text>

  <line x1="85" y1="164" x2="85" y2="178" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="85,186 81,178 89,178" fill="currentColor"/>

  <line x1="235" y1="164" x2="235" y2="178" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="235,186 231,178 239,178" fill="currentColor"/>

  <rect x="30" y="186" width="260" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="206" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">AWS Shield Advanced (L3/L4/L7 DDoS)</text>"""
    },

    # 2. Stepped Priority Waterfall (Left) paired with Vertical WCU Budget Meter (Right)
    "ru/01.html": {
        "num": 2,
        "key": "01-evaluation-priority",
        "title": "Каскад приоритетов правил Web ACL и шкала бюджета емкости WCU.",
        "aria": "Схема каскадного конвейера приоритетов правил и шкалы бюджета емкости WCU",
        "h": 230,
        "mmd": """flowchart TD
    subgraph Cascade["Каскад приоритетов"]
        P0["Priority 0: IPSet (1 WCU)"] --> P10["Priority 10: CRS (700 WCU)"]
        P10 --> P20["Priority 20: Rate (10 WCU)"]
        P20 --> Def["DefaultAction: Allow / Block"]
    end
    subgraph Meter["Бюджет емкости"]
        WCU["Использовано 711 / 1500 WCU"]
    end
    Cascade -.-> Meter
""",
        "svg": """  <rect x="10" y="10" width="165" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="92" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Priority 0: IPSet</text>
  <text x="92" y="38" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Белый список (1 WCU)</text>

  <line x1="92" y1="42" x2="92" y2="52" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="92,60 88,52 96,52" fill="currentColor"/>

  <rect x="10" y="60" width="165" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="92" y="76" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Priority 10: CRS</text>
  <text x="92" y="88" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Managed CRS (700 WCU)</text>

  <line x1="92" y1="92" x2="92" y2="102" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="92,110 88,102 96,102" fill="currentColor"/>

  <rect x="10" y="110" width="165" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="92" y="126" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Priority 20: Rate</text>
  <text x="92" y="138" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Rate Limit (10 WCU)</text>

  <line x1="92" y1="142" x2="92" y2="152" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="92,160 88,152 96,152" fill="currentColor"/>

  <rect x="10" y="160" width="165" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.4"/>
  <text x="92" y="180" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">DefaultAction</text>

  <line x1="175" y1="76" x2="187" y2="76" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="195,76 187,72 187,80" fill="currentColor"/>

  <rect x="195" y="10" width="115" height="182" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="252" y="30" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Бюджет WCU</text>
  <text x="252" y="52" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Лимит: 1500</text>
  <text x="252" y="80" text-anchor="middle" font-size="12" fill="currentColor">В сумме:</text>
  <text x="252" y="98" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">711 WCU</text>
  <text x="252" y="126" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Запас: 789</text>
  <text x="252" y="152" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Макс: 5000</text>
  <text x="252" y="176" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">В норме</text>

  <rect x="10" y="198" width="300" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="214" text-anchor="middle" font-size="12" fill="currentColor">Строгий порядок: от Priority 0 до N</text>"""
    },

    # 3. Dual-Pillar Comparative Columns with Cross-Plane Control
    "ru/02.html": {
        "num": 3,
        "key": "02-scopes-associations",
        "title": "Архитектурный мост областей видимости Scope: CLOUDFRONT против REGIONAL.",
        "aria": "Схема разграничения глобальной области CLOUDFRONT и региональной REGIONAL с точками интеграции",
        "h": 230,
        "mmd": """flowchart TD
    API["WAFv2 Control Plane API"] --> CF["Scope CLOUDFRONT (us-east-1)"]
    API --> REG["Scope REGIONAL (Локальный регион)"]
    CF --> Edge["Edge PoP Anycast"]
    REG --> Target["ALB, API Gateway, Cognito"]
    Edge --> Backend["Целевой бэкенд в VPC"]
    Target --> Backend
""",
        "svg": """  <rect x="35" y="8" width="250" height="26" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="25" text-anchor="middle" font-size="12" fill="currentColor">WAFv2 Control Plane API</text>

  <path d="M 160 34 L 160 46 L 77 46 L 77 56" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="77,64 73,56 81,56" fill="currentColor"/>

  <path d="M 160 34 L 160 46 L 243 46 L 243 56" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="243,64 239,56 247,56" fill="currentColor"/>

  <rect x="10" y="64" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="77" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">CLOUDFRONT</text>
  <text x="77" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">us-east-1 Only</text>

  <rect x="175" y="64" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="242" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">REGIONAL</text>
  <text x="242" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Регион VPC</text>

  <line x1="77" y1="106" x2="77" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="77,124 73,116 81,116" fill="currentColor"/>

  <line x1="243" y1="106" x2="243" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="243,124 239,116 247,116" fill="currentColor"/>

  <rect x="10" y="124" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="77" y="141" text-anchor="middle" font-size="12" fill="currentColor">Edge PoP Anycast</text>
  <text x="77" y="154" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Периферия сети</text>

  <rect x="175" y="124" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="242" y="141" text-anchor="middle" font-size="12" fill="currentColor">ALB &amp; API Gateway</text>
  <text x="242" y="154" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Внутри сети VPC</text>

  <line x1="77" y1="164" x2="77" y2="176" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="77,184 73,176 81,176" fill="currentColor"/>

  <line x1="243" y1="164" x2="243" y2="176" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="243,184 239,176 247,176" fill="currentColor"/>

  <rect x="20" y="184" width="280" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="205" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Целевые серверы приложений в VPC</text>"""
    },

    # 4. 3-Pillar Managed Rules Hierarchy & Override Matrix
    "ru/03.html": {
        "num": 4,
        "key": "03-managed-rules-hierarchy",
        "title": "Иерархия AWS Managed Rules и три механизма управления переопределениями.",
        "aria": "Схема трех механизмов управления управляемыми пакетами: Default, Override Count и ExcludedRules",
        "h": 230,
        "mmd": """flowchart TD
    AMR["AWS Managed Rules (CRS)"] --> Def["1. Default: Block"]
    AMR --> Ovr["2. Override: Count"]
    AMR --> Exc["3. ExcludedRules"]
    Def --> Out["Итог: Безопасная адаптация правил"]
    Ovr --> Out
    Exc --> Out
""",
        "svg": """  <rect x="30" y="8" width="260" height="30" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="27" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">AWS Managed Rules (CRS 700 WCU)</text>

  <line x1="59" y1="38" x2="59" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="59,66 55,58 63,58" fill="currentColor"/>

  <line x1="160" y1="38" x2="160" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,66 156,58 164,58" fill="currentColor"/>

  <line x1="261" y1="38" x2="261" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,66 257,58 265,58" fill="currentColor"/>

  <rect x="12" y="66" width="94" height="92" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="59" y="84" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. Default</text>
  <text x="59" y="104" text-anchor="middle" font-size="12" fill="currentColor">Block</text>
  <text x="59" y="122" text-anchor="middle" font-size="12" fill="currentColor">Защита из</text>
  <text x="59" y="142" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">коробки</text>

  <rect x="113" y="66" width="94" height="92" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="84" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. Override</text>
  <text x="160" y="104" text-anchor="middle" font-size="12" fill="currentColor">Count</text>
  <text x="160" y="122" text-anchor="middle" font-size="12" fill="currentColor">Аудит логов</text>
  <text x="160" y="142" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Метрики CW</text>

  <rect x="214" y="66" width="94" height="92" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="261" y="84" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. Exclude</text>
  <text x="261" y="104" text-anchor="middle" font-size="12" fill="currentColor">Правило</text>
  <text x="261" y="122" text-anchor="middle" font-size="12" fill="currentColor">Исключение</text>
  <text x="261" y="142" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">без ложных</text>

  <line x1="160" y1="158" x2="160" y2="174" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,182 156,174 164,174" fill="currentColor"/>

  <rect x="25" y="182" width="270" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="203" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Безопасная адаптация правил без сбоев</text>"""
    },

    # 5. 4-Tier Inspection Funnel Stack
    "ru/04.html": {
        "num": 5,
        "key": "04-custom-inspection-pipeline",
        "title": "Четырехуровневый конвейер инспекции: от извлечения полей до логических предикатов.",
        "aria": "Схема конвейера инспекции кастомных правил: FieldToMatch, нормализация, предикаты и вердикт",
        "h": 230,
        "mmd": """flowchart TD
    Field["1. FieldToMatch: URI, Headers, Body"] --> Norm["2. Нормализация: URL_DECODE + LOWERCASE"]
    Norm --> Byte["ByteMatch / Regex"]
    Norm --> IP["IPSet / GeoMatch"]
    Byte --> Logic["4. Логика And / Or / Not -> Вердикт"]
    IP --> Logic
""",
        "svg": """  <rect x="25" y="8" width="270" height="28" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="26" text-anchor="middle" font-size="12" fill="currentColor">1. FieldToMatch (URI / Headers / Body)</text>

  <line x1="160" y1="36" x2="160" y2="50" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,58 156,50 164,50" fill="currentColor"/>

  <rect x="20" y="58" width="280" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="74" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. Нормализация (LOWER + URL_DECODE)</text>
  <text x="160" y="86" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Канонизация для защиты от обхода</text>

  <path d="M 160 92 L 160 106 L 85 106 L 85 114" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="85,122 81,114 89,114" fill="currentColor"/>

  <path d="M 160 92 L 160 106 L 235 106 L 235 114" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="235,122 231,114 239,114" fill="currentColor"/>

  <rect x="15" y="122" width="140" height="38" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="85" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Byte / Regex</text>
  <text x="85" y="152" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Поиск шаблона</text>

  <rect x="165" y="122" width="140" height="38" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="235" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">IPSet / Geo</text>
  <text x="235" y="152" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Списочный фильтр</text>

  <line x1="85" y1="160" x2="85" y2="168" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="85,176 81,168 89,168" fill="currentColor"/>

  <line x1="235" y1="160" x2="235" y2="168" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="235,176 231,168 239,168" fill="currentColor"/>

  <rect x="25" y="176" width="270" height="36" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="193" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">4. Логика And / Or / Not -> Action</text>
  <text x="160" y="206" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Терминальный вердикт или Count</text>"""
    },

    # 6. Circular Sliding Window Rate Limiting Loop
    "ru/05.html": {
        "num": 6,
        "key": "05-rate-limiting-sliding-window",
        "title": "Замкнутый контур скользящего окна Rate Limiting с петлей восстановления.",
        "aria": "Схема замкнутого контура скользящего окна Rate Limiting с порогом и автоматическим снятием блокировки",
        "h": 230,
        "mmd": """flowchart TD
    Req["Запросы: IP / JWT Key"] --> Win["Скользящее окно (60-600с)"]
    Win --> Comp{"Сравнение с лимитом"}
    Comp -->|Превышен| Block["Block / CAPTCHA (Бан)"]
    Block -->|Снижение частоты| Req
""",
        "svg": """  <rect x="35" y="8" width="250" height="30" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Поток запросов (IP / JWT)</text>
  <text x="160" y="35" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Окна 60с - 600с</text>

  <line x1="240" y1="38" x2="240" y2="68" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="240,76 236,68 244,68" fill="currentColor"/>

  <rect x="175" y="76" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="242" y="94" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Скользящее окно</text>
  <text x="242" y="108" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Агрегация ключей</text>

  <line x1="242" y1="118" x2="242" y2="142" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="242,150 238,142 246,142" fill="currentColor"/>

  <rect x="30" y="150" width="260" height="36" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="167" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Сравнение с порогом (Rate Limit)</text>
  <text x="160" y="179" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Превышение лимита (100 req/5m)</text>

  <line x1="75" y1="150" x2="75" y2="124" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="75,116 71,124 79,124" fill="currentColor"/>

  <rect x="10" y="76" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="77" y="93" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Block / CAPTCHA</text>
  <text x="77" y="107" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Временный бан</text>

  <line x1="75" y1="76" x2="75" y2="44" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="75,38 71,44 79,44" fill="currentColor"/>

  <rect x="30" y="196" width="260" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="212" text-anchor="middle" font-size="12" fill="currentColor">Автоматический сброс после паузы</text>"""
    },

    # 7. 3-Pillar Action Classification (Allow/Block, Count, Challenges)
    "ru/06.html": {
        "num": 7,
        "key": "06-actions-verdict-decision",
        "title": "Дерево пяти терминальных и нетерминальных действий правил Web ACL.",
        "aria": "Схема пяти вариантов вердикта правил WAF: Allow, Block, Count, CAPTCHA, Challenge",
        "h": 230,
        "mmd": """flowchart TD
    Match["Срабатывание правила WAFv2"] --> Term["Терминальные: Allow / Block"]
    Match --> NonTerm["Нетерминальное: Count"]
    Match --> Chall["Челленджи: CAPTCHA / Silent"]
    Term --> Out["Управление доступом L7"]
    NonTerm --> Out
    Chall --> Out
""",
        "svg": """  <rect x="30" y="8" width="260" height="30" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="27" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Срабатывание правила WAFv2</text>

  <line x1="59" y1="38" x2="59" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="59,66 55,58 63,58" fill="currentColor"/>

  <line x1="160" y1="38" x2="160" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,66 156,58 164,58" fill="currentColor"/>

  <line x1="261" y1="38" x2="261" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,66 257,58 265,58" fill="currentColor"/>

  <rect x="12" y="66" width="94" height="92" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="59" y="84" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Терминал</text>
  <text x="59" y="104" text-anchor="middle" font-size="12" fill="currentColor">Allow</text>
  <text x="59" y="122" text-anchor="middle" font-size="12" fill="currentColor">Block 403</text>
  <text x="59" y="142" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Финал</text>

  <rect x="113" y="66" width="94" height="92" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="84" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Метрика</text>
  <text x="160" y="104" text-anchor="middle" font-size="12" fill="currentColor">Count</text>
  <text x="160" y="122" text-anchor="middle" font-size="12" fill="currentColor">RuleLabel</text>
  <text x="160" y="142" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Пропуск</text>

  <rect x="214" y="66" width="94" height="92" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="261" y="84" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Челлендж</text>
  <text x="261" y="104" text-anchor="middle" font-size="12" fill="currentColor">CAPTCHA</text>
  <text x="261" y="122" text-anchor="middle" font-size="12" fill="currentColor">Challenge</text>
  <text x="261" y="142" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">JS токен</text>

  <line x1="160" y1="158" x2="160" y2="174" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,182 156,174 164,174" fill="currentColor"/>

  <rect x="20" y="182" width="280" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="198" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Пять вердиктов действий правил</text>
  <text x="160" y="210" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Управление доступом на уровне L7</text>"""
    },

    # 8. Protocol Sequence Ladder: Silent Challenge & Token Acquisition
    "ru/07.html": {
        "num": 8,
        "key": "07-bot-control-challenge-flow",
        "title": "Пошаговый протокол Silent Challenge: JavaScript SDK и выдача крипто-токена.",
        "aria": "Схема протокола Silent Challenge в виде диаграммы пошагового обмена сообщениями",
        "h": 220,
        "mmd": """sequenceDiagram
    participant Browser as Клиент (JS SDK)
    participant WAF as AWS WAF Edge
    Browser->>WAF: 1. GET /app (Первый запрос)
    WAF-->>Browser: 2. 202 Challenge + PoW Script
    Browser->>WAF: 3. Решение PoW + aws-waf-token
    WAF-->>Browser: 4. 200 OK (Immunity Time 300s)
""",
        "svg": """  <rect x="10" y="15" width="80" height="190" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="50" y="34" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Клиент</text>
  <text x="50" y="48" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">JS SDK</text>

  <rect x="230" y="15" width="80" height="190" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="270" y="34" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">AWS WAF</text>
  <text x="270" y="48" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Edge Filter</text>

  <line x1="90" y1="65" x2="222" y2="65" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="230,65 222,61 222,69" fill="currentColor"/>
  <text x="160" y="58" text-anchor="middle" font-size="12" fill="currentColor">1. GET /app</text>

  <line x1="230" y1="100" x2="98" y2="100" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="90,100 98,96 98,104" fill="currentColor"/>
  <text x="160" y="93" text-anchor="middle" font-size="12" fill="currentColor">2. 202 Challenge</text>

  <line x1="90" y1="135" x2="222" y2="135" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="230,135 222,131 222,139" fill="currentColor"/>
  <text x="160" y="128" text-anchor="middle" font-size="12" fill="currentColor">3. Токен PoW</text>

  <line x1="230" y1="170" x2="98" y2="170" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="90,170 98,166 98,174" fill="currentColor"/>
  <text x="160" y="163" text-anchor="middle" font-size="12" fill="currentColor">4. 200 OK (Доступ)</text>"""
    },

    # 9. Hub-and-Spoke Event Telemetry Star
    "ru/08.html": {
        "num": 9,
        "key": "08-streaming-logging-pipeline",
        "title": "Топология звезда (Hub-and-Spoke): шина логирования и каналы доставки.",
        "aria": "Схема радиальной топологии потокового логирования: ядро WAF и лучи Kinesis, CloudWatch, S3",
        "h": 230,
        "mmd": """flowchart TD
    WAF["WAF Logging Engine"] --> CW_Alarm["CloudWatch Alarms"]
    WAF --> Firehose["Kinesis Firehose"]
    WAF --> CW_Logs["CW Logs Insights"]
    WAF --> S3["Amazon S3 + Athena"]
""",
        "svg": """  <rect x="60" y="10" width="200" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="29" text-anchor="middle" font-size="12" fill="currentColor">CloudWatch Alarms</text>

  <line x1="160" y1="42" x2="160" y2="67" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,75 156,67 164,67" fill="currentColor"/>

  <rect x="10" y="75" width="70" height="46" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="45" y="94" text-anchor="middle" font-size="12" fill="currentColor">Kinesis</text>
  <text x="45" y="108" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Firehose</text>

  <line x1="105" y1="98" x2="88" y2="98" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="80,98 88,94 88,102" fill="currentColor"/>

  <rect x="105" y="75" width="110" height="46" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="94" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">WAF Logging</text>
  <text x="160" y="108" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">RedactedFields</text>

  <line x1="215" y1="98" x2="232" y2="98" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="240,98 232,94 232,102" fill="currentColor"/>

  <rect x="240" y="75" width="70" height="46" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="275" y="94" text-anchor="middle" font-size="12" fill="currentColor">CW Logs</text>
  <text x="275" y="108" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Insights</text>

  <line x1="160" y1="121" x2="160" y2="147" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,155 156,147 164,147" fill="currentColor"/>

  <rect x="60" y="155" width="200" height="34" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="172" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Amazon S3 &amp; Athena SQL</text>
  <text x="160" y="184" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Паркет архив</text>

  <rect x="30" y="198" width="260" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="214" text-anchor="middle" font-size="12" fill="currentColor">Полная аудируемость и маскирование PII</text>"""
    },

    # 10. Tiered Rollout Pyramid
    "ru/09.html": {
        "num": 10,
        "key": "09-staged-rollout-lifecycle",
        "title": "Пирамида стадий безопасного релиза правил от Count к Enforce Block.",
        "aria": "Схема 4-ступенчатой пирамиды внедрения правил WAF без ложных срабатываний",
        "h": 230,
        "mmd": """flowchart TD
    S1["1. Развертывание в Count (7-14 дней)"] --> S2["2. Анализ Sampled Requests"]
    S2 --> S3["3. Канареечный тест (Canary)"]
    S3 --> S4["4. Enforce Block (LockToken)"]
""",
        "svg": """  <rect x="15" y="10" width="290" height="34" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. Развертывание в Count</text>
  <text x="160" y="38" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Аудит объема без блокировок</text>

  <line x1="160" y1="44" x2="160" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,66 156,58 164,58" fill="currentColor"/>

  <rect x="35" y="66" width="250" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. Анализ сэмплов</text>
  <text x="160" y="94" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Поиск ложных срабатываний</text>

  <line x1="160" y1="100" x2="160" y2="114" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,122 156,114 164,114" fill="currentColor"/>

  <rect x="55" y="122" width="210" height="34" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. Канарейка (Canary)</text>
  <text x="160" y="150" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Тестовый сегмент</text>

  <line x1="160" y1="156" x2="160" y2="170" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,178 156,170 164,170" fill="currentColor"/>

  <rect x="65" y="178" width="190" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="195" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">4. Enforce Block</text>
  <text x="160" y="206" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">LockToken защита</text>"""
    },

    # 11. Stepping Stones Roadmap: Noob Practical Perimeter
    "ru/10.html": {
        "num": 11,
        "key": "10-noob-perimeter-stack",
        "title": "Ступени эшелона Noob: IP Allowlist, CRS сигнатуры и лимиты размера.",
        "aria": "Схема дорожной карты последовательных рубежей защиты уровня Noob",
        "h": 230,
        "mmd": """flowchart LR
    S1["1. IP Allowlist"] --> S2["2. Tor / Geo IP"]
    S2 --> S3["3. AWS CRS"]
    S3 --> S4["4. Size Limit"]
    S4 --> Goal["5. Изоляция /admin"]
""",
        "svg": """  <rect x="15" y="10" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. IP Allowlist</text>
  <text x="82" y="40" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Офис / VPN (Allow)</text>

  <line x1="150" y1="30" x2="162" y2="30" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="170,30 162,26 162,34" fill="currentColor"/>

  <rect x="170" y="10" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. Tor / Geo IP</text>
  <text x="237" y="40" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Блок аномалий</text>

  <line x1="237" y1="50" x2="237" y2="66" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,74 233,66 241,66" fill="currentColor"/>

  <rect x="170" y="74" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="90" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. AWS CRS</text>
  <text x="237" y="104" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Сигнатуры OWASP</text>

  <line x1="170" y1="94" x2="158" y2="94" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="150,94 158,90 158,98" fill="currentColor"/>

  <rect x="15" y="74" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="90" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">4. Size Limit</text>
  <text x="82" y="104" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Лимит тела 8 КБ</text>

  <line x1="82" y1="114" x2="82" y2="132" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,140 78,132 86,132" fill="currentColor"/>

  <rect x="20" y="140" width="280" height="38" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="157" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">5. Изоляция пути /admin</text>
  <text x="160" y="170" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Строгий доступ по белому списку</text>

  <line x1="160" y1="178" x2="160" y2="186" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,194 156,186 164,186" fill="currentColor"/>

  <rect x="30" y="194" width="260" height="26" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="211" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Готовый baseline начального периметра</text>"""
    },

    # 12. 2x2 Quadrant Security Grid with Central Synthesis Hub
    "ru/11.html": {
        "num": 12,
        "key": "11-pro-jwt-rate-limit",
        "title": "Матрица защитных механизмов уровня Pro: 2x2 квадранта с центральным хабом.",
        "aria": "Схема матрицы 2x2 инженерных решений уровня Pro: JWT, ATP, Firehose и Terraform",
        "h": 230,
        "mmd": """flowchart TD
    Q1["1. JWT Rate Limit"] --> Hub["Ядро WAFv2 Pro"]
    Q2["2. ATP Антифрод"] --> Hub
    Q3["3. PII Редактирование"] --> Hub
    Q4["4. CI/CD & Terraform"] --> Hub
    Hub --> Spec["Стандарт AWS Security Specialty"]
""",
        "svg": """  <rect x="15" y="8" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="25" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. JWT Rate Limit</text>
  <text x="82" y="39" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Скользящие окна</text>

  <rect x="170" y="8" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="25" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. ATP Антифрод</text>
  <text x="237" y="39" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Защита паролей</text>

  <line x1="82" y1="50" x2="82" y2="60" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,68 78,60 86,60" fill="currentColor"/>

  <line x1="237" y1="50" x2="237" y2="60" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,68 233,60 241,60" fill="currentColor"/>

  <rect x="15" y="68" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="85" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. Скрытие PII</text>
  <text x="82" y="99" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Фильтр логов</text>

  <rect x="170" y="68" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="85" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">4. Terraform IaC</text>
  <text x="237" y="99" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">CI/CD Gates</text>

  <line x1="82" y1="110" x2="82" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,128 78,120 86,120" fill="currentColor"/>

  <line x1="237" y1="110" x2="237" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,128 233,120 241,120" fill="currentColor"/>

  <rect x="20" y="128" width="280" height="38" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="145" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Ядро WAFv2 уровня Pro</text>
  <text x="160" y="158" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Адаптивная эшелонированная защита</text>

  <line x1="160" y1="166" x2="160" y2="178" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,186 156,178 164,178" fill="currentColor"/>

  <rect x="30" y="186" width="260" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="204" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Стандарт AWS Security Specialty</text>"""
    },

    # 13. Autonomous Closed Loop (SOAR Remediation Cycle)
    "ru/12.html": {
        "num": 13,
        "key": "12-igl-soar-auto-mitigation",
        "title": "Автономный контур реагирования SOAR: замкнутый цикл самовосстановления.",
        "aria": "Схема замкнутого цикла SOAR: обнаружение атаки, анализ в Athena, динамический бан в IPSet",
        "h": 230,
        "mmd": """flowchart TD
    Spike["1. Всплеск L7-атаки"] --> EB["2. EventBridge триггер"]
    EB --> Lambda["3. Lambda + Athena SQL"]
    Lambda --> Ban["4. Динамический бан IPSet"]
    Ban -->|Снижение аномалии| Spike
""",
        "svg": """  <rect x="35" y="8" width="250" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. Всплеск L7-атаки</text>
  <text x="160" y="35" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Аномалия 4xx / 5xx</text>

  <line x1="240" y1="40" x2="240" y2="68" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="240,76 236,68 244,68" fill="currentColor"/>

  <rect x="175" y="76" width="135" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="242" y="94" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. EventBridge</text>
  <text x="242" y="108" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Триггер события</text>

  <line x1="242" y1="118" x2="242" y2="142" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="242,150 238,142 246,142" fill="currentColor"/>

  <rect x="30" y="150" width="260" height="38" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="167" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. Lambda + Athena SQL</text>
  <text x="160" y="180" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Выявление IP атакующих ботов</text>

  <line x1="75" y1="150" x2="75" y2="124" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="75,116 71,124 79,124" fill="currentColor"/>

  <rect x="10" y="76" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="77" y="93" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">4. Бан в IPSet</text>
  <text x="77" y="107" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">TTL авто-снятие</text>

  <line x1="75" y1="76" x2="75" y2="46" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="75,40 71,46 79,46" fill="currentColor"/>

  <rect x="30" y="198" width="260" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="214" text-anchor="middle" font-size="12" fill="currentColor">MTTR менее 60 секунд без участия дежурного</text>"""
    },

    # 14. Hierarchical Tree with Branch Nodes (Noob Assessment)
    "ru/13.html": {
        "num": 14,
        "key": "13-assessment-noob-tree",
        "title": "Иерархическое дерево квалификационного банка Noob: 5 тематических ветвей.",
        "aria": "Схема дерева компетенций уровня Noob: 50 вопросов по ключевым темам базовой подготовки",
        "h": 230,
        "mmd": """flowchart TD
    Bank["Банк Noob: 50 вопросов"] --> N1["Web ACL (1-10)"]
    Bank --> N2["Scopes (11-20)"]
    Bank --> N3["Правила (21-30)"]
    N1 --> N4["Сэмплы (31-40)"]
    N3 --> N5["IPSet (41-50)"]
    N4 --> Goal["Junior Cloud Security"]
    N5 --> Goal
""",
        "svg": """  <rect x="20" y="8" width="280" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Банк Noob: 50 вопросов</text>

  <line x1="59" y1="36" x2="59" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="59,66 55,58 63,58" fill="currentColor"/>

  <line x1="160" y1="36" x2="160" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,66 156,58 164,58" fill="currentColor"/>

  <line x1="261" y1="36" x2="261" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,66 257,58 265,58" fill="currentColor"/>

  <rect x="12" y="66" width="94" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="59" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Web ACL</text>
  <text x="59" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">WCU (1-10)</text>

  <rect x="113" y="66" width="94" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Scopes</text>
  <text x="160" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Связи 11-20</text>

  <rect x="214" y="66" width="94" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="261" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Правила</text>
  <text x="261" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">21-30</text>

  <line x1="59" y1="108" x2="59" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="59,128 55,120 63,120" fill="currentColor"/>

  <line x1="261" y1="108" x2="261" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,128 257,120 265,120" fill="currentColor"/>

  <rect x="15" y="128" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="145" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Сэмплы (31-40)</text>
  <text x="82" y="159" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Диагностика</text>

  <rect x="170" y="128" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="145" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Списки (41-50)</text>
  <text x="237" y="159" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">IPSet и Geo</text>

  <line x1="82" y1="168" x2="82" y2="180" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,188 78,180 86,180" fill="currentColor"/>

  <line x1="237" y1="168" x2="237" y2="180" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,188 233,180 241,180" fill="currentColor"/>

  <rect x="20" y="188" width="280" height="30" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="206" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Готовность Junior Cloud Security</text>"""
    },

    # 15. Network Mesh with Central Certification Hub (Pro Assessment)
    "ru/14.html": {
        "num": 15,
        "key": "14-assessment-pro-pipeline",
        "title": "Сетевая топология компетенций инженера Pro: перекрестные связи пяти доменов.",
        "aria": "Схема сетевой структуры компетенций уровня Pro: боты, антифрод, логи и автоматизация",
        "h": 230,
        "mmd": """flowchart TD
    Top["1. Bot Control & JA4 (1-10)"] --> L1["2. ATP Антифрод (11-20)"]
    Top --> R1["3. S3 & Firehose (21-30)"]
    L1 --> Hub["Инженерный хаб Pro"]
    R1 --> Hub
    Hub --> L2["4. Правила (31-40)"]
    Hub --> R2["5. Terraform (41-50)"]
""",
        "svg": """  <rect x="30" y="8" width="260" height="30" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="27" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. Bot Control &amp; JA4 (1-10)</text>

  <line x1="82" y1="38" x2="82" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,66 78,58 86,58" fill="currentColor"/>

  <line x1="237" y1="38" x2="237" y2="58" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,66 233,58 241,58" fill="currentColor"/>

  <rect x="15" y="66" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. ATP Антифрод</text>
  <text x="82" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Защита (11-20)</text>

  <rect x="170" y="66" width="135" height="40" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. S3 &amp; Firehose</text>
  <text x="237" y="96" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Логи (21-30)</text>

  <line x1="82" y1="106" x2="82" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,124 78,116 86,116" fill="currentColor"/>

  <line x1="237" y1="106" x2="237" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,124 233,116 241,116" fill="currentColor"/>

  <rect x="20" y="124" width="280" height="40" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="141" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Инженерный хаб Pro (WAF)</text>
  <text x="160" y="155" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Синтез правил и автоматизации</text>

  <line x1="82" y1="164" x2="82" y2="174" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="82,182 78,174 86,174" fill="currentColor"/>

  <line x1="237" y1="164" x2="237" y2="174" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="237,182 233,174 241,174" fill="currentColor"/>

  <rect x="15" y="182" width="135" height="38" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="82" y="198" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Правила 31-40</text>
  <text x="82" y="211" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">ByteMatch / Regex</text>

  <rect x="170" y="182" width="135" height="38" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="237" y="198" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">IaC 41-50</text>
  <text x="237" y="211" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Terraform Gates</text>"""
    },

    # 16. Multi-Tier Enterprise Governance Architecture (IGL FMS Fan-Out)
    "ru/15.html": {
        "num": 16,
        "key": "15-assessment-igl-governance",
        "title": "Корпоративное управление безопасностью: AWS Firewall Manager и мультиаккаунт.",
        "aria": "Схема централизованного управления политиками WAF через AWS Firewall Manager в организации",
        "h": 230,
        "mmd": """flowchart TD
    Org["AWS Organizations & FMS Admin"] --> AccA["Аккаунт A (CloudFront)"]
    Org --> AccB["Аккаунт B (ALB Banking)"]
    Org --> AccC["Аккаунт C (API Gateway)"]
    AccA --> Arch["Principal Security Architect"]
    AccB --> Arch
    AccC --> Arch
""",
        "svg": """  <rect x="20" y="8" width="280" height="34" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="24" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">AWS Organizations &amp; FMS Admin</text>
  <text x="160" y="36" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Централизованные политики WAF</text>

  <line x1="59" y1="42" x2="59" y2="70" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="59,78 55,70 63,70" fill="currentColor"/>

  <line x1="160" y1="42" x2="160" y2="70" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,78 156,70 164,70" fill="currentColor"/>

  <line x1="261" y1="42" x2="261" y2="70" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,78 257,70 265,70" fill="currentColor"/>

  <rect x="12" y="78" width="94" height="74" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="59" y="96" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Аккаунт A</text>
  <text x="59" y="114" text-anchor="middle" font-size="12" fill="currentColor">Frontend</text>
  <text x="59" y="132" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">CloudFront</text>

  <rect x="113" y="78" width="94" height="74" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="96" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Аккаунт B</text>
  <text x="160" y="114" text-anchor="middle" font-size="12" fill="currentColor">Banking API</text>
  <text x="160" y="132" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">ALB + Bots</text>

  <rect x="214" y="78" width="94" height="74" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="261" y="96" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Аккаунт C</text>
  <text x="261" y="114" text-anchor="middle" font-size="12" fill="currentColor">Services</text>
  <text x="261" y="132" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">API Gateway</text>

  <line x1="59" y1="152" x2="59" y2="164" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="59,172 55,164 63,164" fill="currentColor"/>

  <line x1="160" y1="152" x2="160" y2="164" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,172 156,164 164,164" fill="currentColor"/>

  <line x1="261" y1="152" x2="261" y2="164" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="261,172 257,164 265,164" fill="currentColor"/>

  <rect x="20" y="172" width="280" height="38" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="189" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Роль Principal Security Architect (IGL)</text>
  <text x="160" y="202" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">FinOps оптимизация и SLO 99.99%</text>"""
    },

    # 17. 3x3 Radial Matrix of 9 Engineering Lenses
    "ru/navigator.html": {
        "num": 17,
        "key": "navigator-lenses",
        "title": "Матрица 3x3 девяти инженерных линз вокруг архитектурного ядра WAFv2.",
        "aria": "Схема аналитической матрицы 3x3 девяти инженерных линз вокруг ядра WAFv2",
        "h": 240,
        "mmd": """flowchart TD
    subgraph Row1["Фундамент"]
        L1["1. Core"]
        L2["2. Code"]
        L3["3. Strength"]
    end
    Row1 --> Hub["Ядро WAFv2: Web ACL & WCU"]
    Hub --> Row2["Контекст"]
    subgraph Row2["Контекст"]
        L4["4. Limits"]
        L5["5. Ecosys"]
        L6["6. AI Lens"]
    end
    Row2 --> Row3["Эксплуатация"]
    subgraph Row3["Эксплуатация"]
        L7["7. Cloud"]
        L8["8. DevOps"]
        L9["9. SRE"]
    end
""",
        "svg": """  <rect x="15" y="8" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">1. Core</text>

  <rect x="115" y="8" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">2. Code</text>

  <rect x="215" y="8" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="260" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">3. Strength</text>

  <line x1="60" y1="40" x2="60" y2="52" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="60,60 56,52 64,52" fill="currentColor"/>

  <line x1="160" y1="40" x2="160" y2="52" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,60 156,52 164,52" fill="currentColor"/>

  <line x1="260" y1="40" x2="260" y2="52" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="260,60 256,52 264,52" fill="currentColor"/>

  <rect x="20" y="60" width="280" height="38" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="77" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">Ядро WAFv2: Web ACL &amp; WCU</text>
  <text x="160" y="91" text-anchor="middle" font-size="12" opacity="0.75" fill="currentColor">Трансверсальный синтез по 9 линзам</text>

  <line x1="60" y1="98" x2="60" y2="110" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="60,118 56,110 64,110" fill="currentColor"/>

  <line x1="160" y1="98" x2="160" y2="110" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,118 156,110 164,110" fill="currentColor"/>

  <line x1="260" y1="98" x2="260" y2="110" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="260,118 256,110 264,110" fill="currentColor"/>

  <rect x="15" y="118" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">4. Limits</text>

  <rect x="115" y="118" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">5. Ecosys</text>

  <rect x="215" y="118" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="260" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">6. AI Lens</text>

  <line x1="60" y1="150" x2="60" y2="166" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="60,174 56,166 64,166" fill="currentColor"/>

  <line x1="160" y1="150" x2="160" y2="166" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,174 156,166 164,166" fill="currentColor"/>

  <line x1="260" y1="150" x2="260" y2="166" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="260,174 256,166 264,166" fill="currentColor"/>

  <rect x="15" y="174" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="194" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">7. Cloud</text>

  <rect x="115" y="174" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="194" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">8. DevOps</text>

  <rect x="215" y="174" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="260" y="194" text-anchor="middle" font-size="12" font-weight="bold" fill="currentColor">9. SRE</text>"""
    }
}

def apply():
    os.makedirs("diagrams", exist_ok=True)
    readme_rows = []

    for fpath, meta in DIAGRAMS.items():
        # 1. Write Mermaid source file
        src_path = os.path.join("diagrams", f"{meta['key']}.mmd")
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(meta["mmd"].strip() + "\n")
        readme_rows.append(f"| `{meta['key']}.mmd` | `{fpath}` | {meta['title']} |")

        # 2. Inject into HTML page
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()

        fig_block = f"""    <div class="box figure">
      <svg viewBox="0 0 320 {meta['h']}" style="max-width:320px;height:auto;display:block;margin:0 auto" role="img" aria-label="{meta['aria']}">
{meta['svg']}
      </svg>
      <p class="dim">Схема {meta['num']}. {meta['title']}</p>
    </div>"""

        # Replace existing figure box safely
        fig_re = re.compile(r'    <div class="box figure">\s*<svg.*?</svg>\s*<p class="dim">.*?</p>\s*</div>', re.DOTALL)
        if fig_re.search(html):
            html = fig_re.sub(fig_block, html, count=1)
        else:
            m = re.search(r'(<div class="box key" id="key-idea">.*?</div>\n\n)', html, re.DOTALL)
            if m:
                pos = m.end()
                html = html[:pos] + fig_block + "\n\n" + html[pos:]
            else:
                raise RuntimeError(f"Could not find injection point for {fpath}")

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated Diagram {meta['num']} in {fpath}")

    # 3. Write diagrams/README.md
    readme_content = f"""# Diagram sources

A diagram on a page is **inline SVG**, not an image file: the page must work from `file://`, and inline vector inherits the theme colour through `currentColor`, so it survives the day/night switch without a second copy. A shared `assets/NN.svg` would also show one language's labels on all four language pages. The full rule is `AGENTS.md` section 5 rule 18, and `node tools/check-diagrams.mjs` guards it.

This folder holds the **source** of each diagram in Mermaid: `NN-name.mmd`, where `NN` is the page the diagram lives on. Every source answers a diagram and every diagram answers a source; the check says so out loud when they drift apart.

The SVGs embedded in the course pages are drawn strictly conforming to the Mermaid sources below and validated via `node tools/check-diagrams.mjs`.

| Source | Page | What it shows |
| :-- | :-- | :-- |
""" + "\n".join(readme_rows) + "\n"

    with open("diagrams/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Updated diagrams/README.md")

if __name__ == "__main__":
    apply()
