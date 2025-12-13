## Training Data Generation

Synthetic Training Data Generator for Finance Intent Parsing
with Clarification Question Generation

The script (`gen.py`) generates synthetic training samples for a finance-focused
natural language understanding model. Each sample consists of a natural
language prompt and a structured JSON interpretation.

### Key characteristics and enforced constraints:
#### Action Info
- Supported intents:
  - individual_saving
  - group_saving (restricted to existing user groups)

- Amount range:
  - Minimum: 5
  - Maximum: 500

- Frequencies:
  - daily
  - weekly
  - monthly
  - n-times

- Conditions:
  - until a date
  - until goal reached
  - skip holidays

#### Prompt Info 
- Prompts:
  - **English** only
  - Natural, varied phrasing
  - Includes realistic user errors such as typos, missing spaces,
    and contradictory instructions

- Currency handling:
  - Locale-specific money formats are mixed in prompts<br>
    Examples: €15, 15€, EUR 15, $20, 20 USD, £30
  - Currency is explicitly extracted from the prompt
  - If exactly one currency is detected, it is stored in structured output
  - If no currency or multiple currencies are detected:
    - currency is set to null
    - needs_clarification is set to True

- Ambiguity and conflicts:
  - Conflicting frequencies, goals, amounts, currencies, or conditions
    force clarification
  - Affected fields are set to null
  - needs_clarification is set to True
  - A targeted clarification_question is generated
  - Confidence score is reduced accordingly

#### Output:
  - 150 samples saved as `training_samples.json`
  - Each sample includes:
    - prompt
    - interpretation
    - clarification_question (nullable)
