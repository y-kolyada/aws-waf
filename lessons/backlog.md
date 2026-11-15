# Backlog

What was deliberately left out, and why it is not being done now.

## How to write a line

```markdown
- **What.** Why it is needed. Why not now.
```

Three fields and not one more. **"Why not now" matters most of the two others:** it is what separates a decision from forgetfulness. A line without it comes back as a reproach six weeks later, when nobody remembers whether it was weighed or dropped.

## Lines

- **Переводы на английский, украинский и немецкий языки.** Необходимы для полноценной международной публикации курса на GitHub Pages. Отложены до отдельной смены локализации после стабилизации русскоязычного ядра.
- **Интеграционные тесты с живым AWS WAF API.** Необходимы для динамической верификации поведения в реальной среде AWS. Отложены до фазы облачного тестирования, чтобы сохранить полную локальную автономность и независимость от сетевых учетных записей при сборке.
- **Динамический бенчмарк задержки WCU в AWS Lambda.** Необходим для измерения микросекундной деградации latency при росте WCU с 500 до 2500. Отложен до подготовки стенда в рамках практической лаборатории.
