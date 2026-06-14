# Data Pipeline Ideas

Early pipeline direction:

```text
chat message
-> parser
-> structured fields
-> Notion database
-> SQLite dashboard store
-> local dashboard / future notebook
-> weekly review
```

## Near-Term Needs

- Recovery data contract
- Validation for missing fields
- Simple parser output format
- Notion database connection
- Export path for analysis
- Source freshness and conflict policy
- Clear boundary between local canonical data and Notion mirrors
