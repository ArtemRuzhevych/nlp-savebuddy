# SaveBuddy (NLP Engine)

SaveBuddy is the intelligent conversational interface of SmartSave, converting natural language commands into structured financial transactions.

## Overview

Unlike traditional banking apps that rely on rigid forms, SaveBuddy allows users to interact with their finances naturally. It serves as an **Interpretation Layer** that parses user intent, extracts transaction details, and validates them against the user's existing financial context.

---

## Core Capabilities

### 1. Intent Recognition
SaveBuddy uses semantic analysis to distinguish between unrelated concepts:
- **Personal Goals**: "Save $20 for my new bike."
- **Group Contributions**: "Chip in 50 EUR for the Berlin Trip."

### 2. Smart Entity Extraction
The engine identifies and normalizes complex data points:
- **Monetary Values**: Handles various formats (`$100`, `100 eur`, `50 zł`).
- **Currencies**: Normalizes colloquial inputs to ISO codes (USD, EUR, PLN, GBP).
- **Schedules**: Distinguishes between one-time transfers ("on Thursday") and recurring commitments ("every Thursday").
- **Dates**: Resolves relative dates ("next Friday", "tomorrow") to concrete timestamps.

### 3. Contextual Awareness
SaveBuddy doesn't work in isolation. It injects the user's current context (existing groups, active goals) into the interpretation result.
- **Fuzzy Matching**: If a user says "Trip", it matches it to the existing "Berlin Trip 2024" group.
- **Ambiguity Resolution**: If a request is unclear, it asks clarifying questions before executing any transaction.

---

## Technical Architecture

The system employs a **Hybrid NLP Strategy** for maximum accuracy and flexibility.

### Models
- **Question Answering (QA)**: Uses a fine-tuned Transformer (e.g., `deepset/roberta-base-squad2`) to extract specific answers from prompts as if they were reading comprehension tasks.
- **Semantic Search**: Uses `SentenceTransformers` (`all-MiniLM-L6-v2`) to perform vector-based matching against known entity lists.

### Workflow
1.  **Augmentation**: The user's prompt is enriched with current date and context.
2.  **Hypothesis Testing**: The model generates hypotheses ("Is this for a group?") and validates them against known data.
3.  **Extraction**: Specific details (Amount, Date, Frequency) are extracted using QA probes.
4.  **Normalization**: Raw text is converted into strict backend schemas (Enums, ISO Dates).

---

## Scope Summary

This feature demonstrates:

-   **Applied AI**: Practical use of HuggingFace Transformers in a fintech context.
-   **Data Validation**: Strict typing and normalization to prevent financial errors.
-   **User-Centric Design**: Prioritizing natural interaction over rigid inputs.
