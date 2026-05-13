# Research Notes

This file captures the current research direction without exposing raw personal tracking data or unfiltered private notes.

## Working Model

The project currently follows this working model:

```text
recovery -> physiological state -> training prescription -> performance output
```

The long-term system should make those relationships more visible over time.

## Questions Being Explored

- Which recovery signals are useful enough to track daily?
- How can natural language be converted into reliable structured data?
- What is the smallest data contract that still supports useful review?
- How should subjective readiness be compared with objective performance?
- Which movement-quality metrics can be captured with simple sensors?
- What feedback loops are useful without becoming overcomplicated?

## Product Questions

- What should the user log manually?
- What should the system infer?
- What should be automated only after enough data exists?
- How can the interface stay low-friction enough for daily use?
- What summaries would actually change behavior?

## Engineering Questions

- How should schemas be versioned?
- What should count as a valid recovery entry?
- How should missing or ambiguous values be handled?
- When should the chatbot ask a follow-up question?
- What belongs in Notion versus code versus analytics notebooks?
- How can the system avoid overfitting to tiny datasets?

