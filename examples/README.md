# Public Code Examples

These examples are sanitized slices of the private Human Model implementation.
They use mock data and omit private Notion database IDs, health records, secrets,
local file paths, and automation credentials.

The goal is to show the shape of the system without publishing the whole working
prototype:

- `readiness_scoring_demo.py` shows a small recovery/readiness scoring loop.
- `bridget_prompt_demo.py` shows rhythm-aware prompt decisions and quick replies.
- `daily_card_demo.py` renders a simple SVG daily card from mock readiness data.
- `dashboard_data_shaping_demo.py` shows dashboard aggregation for body trends,
  training-session summaries, weekly volume, parse warnings, progression
  signals, and import health.

Run all examples:

```bash
python3 examples/readiness_scoring_demo.py
python3 examples/bridget_prompt_demo.py
python3 examples/daily_card_demo.py
python3 examples/dashboard_data_shaping_demo.py
```

Run tests:

```bash
python3 -m unittest discover -s examples/tests
```

These files are intentionally small. They are portfolio examples, not the live
private automation system.
