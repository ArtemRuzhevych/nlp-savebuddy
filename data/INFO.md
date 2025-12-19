## Training Data Generation

Synthetic Training Data Generator for Finance Intent Parsing with Clarification Logic and Group Context Awareness.

The script (`gen.py`) generates synthetic training samples for a finance-focused natural language understanding model. Each sample consists of a **natural language prompt**, a **user context**, and a **structured JSON interpretation**.

### Key characteristics and enforced constraints

#### Action Info

- **Supported intents:**
  - `individual_saving`
  - `group_saving` (supports both new and existing groups via `is_existing_group` detection)

- **Amount range:**
  - Minimum: 5
  - Maximum: 500
  - Support for **decimal values** (e.g., 15.50)

- **Frequencies (Expanded):**
  - `daily`
  - `weekly` (randomized days of week, including weekends/weekdays)
  - `monthly`
  - `bi-weekly` / `fortnightly`
  - `quarterly`
  - `n-times`

- **Conditions:**
  - `until a date`
  - `until goal reached`
  - `skip holidays`
  - `starting from next week`
  - `as long as I have money`

#### Context Awareness (User Groups)

- Each sample includes a `context` object containing a list of `user_groups` (ID and Name).
- The model is responsible for resolving a user's verbal reference (e.g., "my roommates squad") to a specific `group_id` from the provided context.
- `is_existing_group` flag is set to `True` if keywords like "existing", "my", "our", or specific synonyms (squad, pot, fund) are used.

#### Prompt Info

- **Language:** Natural English with varied prefixes (*"Hey Buddy,"*, *"Automatically,"*) and verbs (*"Stash,"*, *"Allocate,"* *"Invest"*).
- **Chaos Injection:**
  - Realistic typos (*svae*, *wekly*, *vaction*).
  - Missing spaces.
  - Contradictory instructions (multi-goal or multi-frequency).
- **Currency handling (Advanced):**
  - Standard formats: €15, 15€, EUR 15, $20, 20 USD, £30, PLN 100.
  - Colloquial formats: "50 bucks", "20 quid".
  - Multi-currency detection triggers clarification.

#### Interpretation Logic

- **Needs Clarification:** Set to `True` if amount, currency, frequency, or goal is missing or ambiguous.
- **Clarification Question:** Generates a targeted question based on the missing information.
- **Group Mapping:** `group_name` is extracted for backend lookup, and `group_id` is resolved if the group exists in the user's context.

#### Output

- **1000 samples** saved as `training_samples.json`
- Each sample includes:
  - `prompt`: The raw natural language input.
  - `context`: The user's environment (e.g., existing groups).
  - `interpretation`: The structured intent and extracted parameters.
