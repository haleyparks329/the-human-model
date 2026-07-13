# Design Principles

These principles translate the philosophy of The Human Model into product and engineering rules. They are meant to guide architecture, feature design, documentation, and future audits.

## 1. Model First

Interfaces, dashboards, chatbots, and reports are surfaces. The evolving personalized model is the durable system.

Implementation should avoid coupling the model to one interface. Bridget, the dashboard, public examples, and future surfaces should be able to read from shared structured context. The model should survive changes in presentation.

When a new feature is proposed, the first question should be what it contributes to the model. A surface can be temporary. The structured context it creates should remain useful.

## 2. Records Are Evidence, Not Understanding

CRUD systems, tables, events, and logs are necessary inputs, but they are not the model itself.

Preserve raw records, but also preserve relationships and context. Distinguish what was captured from what was interpreted. Do not confuse more fields with deeper understanding.

This matters in documentation as much as code. A commit log, table, or data export can show evidence, but it should not be presented as the full understanding layer. The system needs room for meaning, provenance, and uncertainty.

## 3. Separate Evidence, Inference, And Recommendation

The system should distinguish what was observed, what was derived, what is uncertain, and what action is suggested.

Model outputs should be inspectable. Confidence and data-quality states should be explicit. Inference should not silently become fact, especially when recommendations may affect training, recovery, or behavior.

This principle protects the boundary between data and advice. A bad night's sleep is evidence. A reduced readiness score is inference. A recommendation to modify training is a suggested action. Those layers should stay visibly separate.

## 4. Preserve Longitudinal Memory

Personalization requires history across time, not only the latest event.

Preserve prior context, corrections, and user feedback. Avoid repeatedly asking for information already known. Design for patterns across weeks and months, because many useful signals only appear longitudinally.

Memory should also include correction history. If the user repeatedly fixes the same assumption, the system should treat that as model feedback, not as isolated text.

## 5. Human Review Before Stronger Automation

The system should support decisions without quietly becoming the authority.

Recommendations should remain reviewable. Human override should be available. Automation boundaries should stay conservative until evidence, calibration, and trust improve.

The goal is not to avoid automation forever. The goal is to earn stronger automation through evidence, review, and calibration instead of adding authority because the interface feels polished.

## 6. Local-First And User-Owned Where Possible

Personal data, memory, and models should remain under the person's control where practical.

Minimize unnecessary data exposure. Preserve portability. Separate public demos from private records. Treat the personal model as personal infrastructure, not as a hidden asset owned by an interface provider.

Public examples should use mock data. Private records should stay private. Integrations should be designed so useful context can move with the person when possible.

## 7. Low-Friction Model Acquisition

A model only becomes useful if interacting with it fits real life.

Ask for the smallest useful correction. Support natural-language capture. Avoid repetitive forms. Use defaults and prior context responsibly, while making correction easy when the model is wrong.

This is especially important for Bridget. The value of a conversational surface is not that it can ask unlimited questions. The value is that it can collect useful context with very little friction.

## 8. Show Uncertainty

A trustworthy system should expose what it does not know.

Use missing-data states, confidence labels, unsupported rows, visible limitations, and cautious defaults. A weak signal should remain a weak signal, not become a polished answer.

Uncertainty should be part of the user experience, not hidden in logs. If the model lacks evidence, the interface should say so plainly and still offer the next useful step.

## 9. Optimize For Understanding, Not Engagement

The system should help the person make sense of themselves rather than maximize time spent in the product.

Avoid unnecessary notifications and addictive engagement loops. Prioritize clarity and actionability. Let the interface disappear when it is not needed.

A good outcome may be fewer prompts, fewer screens, and less time spent managing the system. The product should earn attention only when it can give attention back.

## 10. Technology Can Be Serious Without Being Sterile

Personal software can be warm, expressive, playful, and enjoyable while remaining technically rigorous.

Personality and aesthetics are legitimate product concerns. Approachable interfaces should not hide reasoning. Playful surfaces can coexist with inspectable systems.

This principle matters because personal software is used inside real routines, not abstract demos. Warmth can reduce friction. Expressiveness can make the system easier to return to. Neither should replace evidence.

## 11. Machines Carry Coordination; Humans Keep Agency

> Give the machines the burden of remembering, coordinating, searching, and connecting. Give people their attention back.

Automate glue work. Reduce cognitive overhead. Preserve judgment, choice, and correction for the human.

This means the system should remember context, search across prior information, coordinate between surfaces, and bring back the relevant detail at the right time. The human should keep control over meaning and action.

## 12. Build From Real Use, Not Idealized Data

The model should survive missing logs, contradictory signals, subjective uncertainty, stale data, and real-life interruptions.

Test with imperfect workflows. Represent data quality explicitly. Avoid designing only for clean datasets. Prefer narrow working loops over broad speculative claims.

Real use includes skipped entries, delayed imports, inconsistent exercise names, tired replies, unexpected schedule changes, and ambiguous signals. The system should treat those as normal operating conditions.

## How To Use These Principles

These principles are decision filters, not fixed implementation rules. When architecture or product choices conflict, they should help clarify the tradeoff: protect the model, preserve evidence, expose uncertainty, reduce cognitive overhead, and keep the human in the loop.
