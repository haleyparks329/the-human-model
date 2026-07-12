# Project Log Automation

The public Notion homepage and the Live Project Log use the same public project-log database, but they do not show the same amount of text.

## Public Log Fields

- `Summary` is the fuller standalone project update. It belongs on the individual update page and can be long enough to explain what changed, why it matters, and how it fits into the Human Model.
- `Front Page Summary` is the short homepage excerpt. It should be 1-3 public-safe sentences and should not include private health data, internal cleanup notes, raw transcripts, credentials, local paths, or details that only make sense inside the private workspace.

## Homepage Layout

The homepage `Latest Update` section shows the newest intended `Featured` Live Project Log row. Its card should include:

- Date
- Update title
- `Front Page Summary`
- A `Read full update` link to the individual update page

The broader `Live Project Log` archive stays available as a separate `See all updates` link below the card.

## Detail Page Layout

Each public update row should also work as a standalone detail view. The automation keeps `Summary` as the canonical full update text and writes that same fuller text into the individual row page body.

## Automation Rules

The publishing automation is model/provider agnostic and idempotent:

- Fetch Notion schemas before writing.
- Reuse `Front Page Summary` if it already exists, or add it as a rich-text/text property if it does not.
- Promote at most one public row per run.
- Duplicate-check by date, title, `Summary`, and `Front Page Summary` before creating a new row.
- Mark only the intended current row as `Featured`.
- If multiple rows are already featured, use the newest featured row for the homepage, log a warning, and unfeature older rows when safe.
- Replace only the homepage `## Latest Update` section, preserving the next top-level section and everything after it exactly.
