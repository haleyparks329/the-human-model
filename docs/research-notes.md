# Research Notes

This file captures the current research direction without exposing raw personal tracking data or unfiltered private notes.

## Working Model

The project currently follows this working model:

```text
recovery -> physiological state -> training prescription -> execution / effort -> performance output
```

The long-term system should make those relationships more visible over time.

Recent product research sharpened the model into four connected questions:

```text
Did they recover?
Did they execute?
Did they push?
Did they adapt?
```

That framing keeps the project from becoming just another readiness tracker. Recovery data is useful, but the differentiating direction is connecting recovery with training execution, effort estimation, and adaptation history.

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
- How should the dashboard distinguish between missing data, low-confidence interpretation, and a real recommendation?
- Which product surface should own daily decisions: Telegram, the local dashboard, Notion, or a future dedicated app?

## Product Landscape Notes

The most relevant adjacent categories are:

- Recovery/readiness wearables such as Oura, WHOOP, Garmin, Apple Watch, Polar, Fitbit, and Samsung Health
- Training analytics and coach platforms such as TrainingPeaks, Smartabase, CoachMePlus, TeamBuildr, and REGMON
- Movement and biomechanics tools such as MediaPipe, OpenPose, OpenSim, Xsens, Noraxon, Delsys, and VALD
- Velocity-based training and smart strength systems such as Vitruve, PUSH, RepOne, Tonal, Tempo, and OxeFit
- Digital physical therapy and remote movement platforms such as Hinge Health, Sword Health, Kaia Health, and OneStep

The public positioning should avoid "fitness tracker" or "another recovery app." The stronger portfolio framing is:

```text
personalized human performance modeling:
recovery, execution, effort, and adaptation
```

## Current Dashboard Research Direction

Coach Dashboard V1 is the first local review surface. Its job is not to look impressive in isolation; it should make the data spine trustworthy by showing source freshness, computed readiness, training context, body metrics, notes, and blocked/unavailable states.

The implementation rule from the dashboard audit is useful beyond V1: every displayed field needs a source mapping, a manual entry path, or a visible unavailable state.

## Current Modeling Direction

The first readiness model is deliberately transparent. It uses personal HRV and resting-HR baselines, sleep duration, subjective recovery inputs, and data-quality notes to produce a baseline band and a short report. LLMs may explain the result later, but they should not generate the model decision.

The next research step is calibration: compare the model's daily call against actual workout execution, Apple Watch movement output, perceived effort, soreness, and follow-up recovery rather than treating a readiness score as self-validating. Apple Watch active energy is useful as a rough movement-output context signal, not as exact calorie truth or a complete training-load model.

## Engineering Questions

- How should schemas be versioned?
- What should count as a valid recovery entry?
- How should missing or ambiguous values be handled?
- When should the chatbot ask a follow-up question?
- What belongs in Notion versus code versus analytics notebooks?
- How can the system avoid overfitting to tiny datasets?
- Where should SQLite, Notion, and future analytics notebooks each own data?
- How should app-native edits, Notion edits, Telegram logs, and imports resolve conflicts?
- How should baseline readiness calls be evaluated against actual training outcomes before recommendations become stronger?
