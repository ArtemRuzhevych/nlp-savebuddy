# data/gen.py

import json
import random
import datetime

# =========================
# Configuration
# =========================

NUM_SAMPLES = 175

INTENTS = ["individual_saving", "group_saving"]
GROUPS = ["family", "roommates", "trip", "wedding", "friends"]
GOALS = ["gym", "rent", "vacation", "groceries", "emergency fund", "new phone"]

FREQUENCIES = ["daily", "weekly", "monthly", "n-times"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


CURRENCY_FORMATS = [
    lambda a: f"€{a}",
    lambda a: f"{a}€",
    lambda a: f"EUR{a}",
    lambda a: f"EUR {a}",
    lambda a: f"{a} EUR",
    lambda a: f"${a}",
    lambda a: f"{a} USD",
    lambda a: f"USD{a}",
    lambda a: f"USD {a}",
    lambda a: f"£{a}",
    lambda a: f"PLN {a}",
    lambda a: f"PLN{a}",
    lambda a: f"{a}zł",
    lambda a: f"{a}zl",
    lambda a: f"{a} zl",
    lambda a: f"{a} zł",
]

TYPO_MAP = {
    "save": ["svae", "saev", "sav", "sve"],
    "every": ["evry", "evey", "evvery"],
    "weekly": ["wekly", "weekyl", "wekely"],
    "monthly": ["montly", "monhtly"],
    "until": ["untill", "til", "till"],
    "Wednesday": ["wednedsay", "wednsday"]
}

# =========================
# Utilities
# =========================

def random_amount():
    return random.randint(5, 500)

def random_date():
    start = datetime.date.today()
    end = start + datetime.timedelta(days=180)
    return str(start + (end - start) * random.random())

def inject_typos(text: str) -> str:
    for word, typos in TYPO_MAP.items():
        if word.lower() in text.lower() and random.random() < 0.3:
            text = text.replace(word, random.choice(typos))
    if random.random() < 0.15:
        text = text.replace(" ", "")
    return text

def confidence_from_nulls(data: dict) -> float:
    nulls = sum(1 for v in data.values() if v is None)
    return round(max(0.35, 1 - nulls * 0.12), 2)

def extract_currency(prompt: str):
    currencies = set()

    if "€" in prompt or "EUR" in prompt:
        currencies.add("EUR")
    if "$" in prompt or "USD" in prompt:
        currencies.add("USD")
    if "£" in prompt or "GBP" in prompt:
        currencies.add("GBP")
    if any(currency_code in prompt for currency_code in ("zł", "PLN", "zl")):
        currencies.add("GBP")

    if len(currencies) == 1:
        return currencies.pop(), False
    return None, True

# =========================
# Clarification Logic
# =========================

def generate_clarification(issues: list) -> str:
    priority = [
        ("currency", "Which currency should be used for this saving?"),
        ("amount", "How much should be saved each time?"),
        ("frequency", "How often should this saving happen?"),
        ("condition", "When should this saving stop?"),
        ("goal", "Which goal should this saving be assigned to?")
    ]

    for key, question in priority:
        if key in issues:
            return question

    return "Can you clarify how this saving should be set up?"

# =========================
# Prompt Construction
# =========================

def money_string(amount: int) -> str:
    return random.choice(CURRENCY_FORMATS)(amount)

def frequency_phrase(freq: str) -> str:
    if freq == "daily":
        return "every day"
    if freq == "weekly":
        return f"every {random.choice(DAYS)}"
    if freq == "monthly":
        return "every month"
    return f"{random.randint(2,10)} times"

def maybe_conflicting_frequency(freq: str):
    if random.random() < 0.25:
        return f"{frequency_phrase(freq)} {frequency_phrase(random.choice(FREQUENCIES))}"
    return frequency_phrase(freq)

def maybe_conflicting_condition():
    if random.random() < 0.25:
        return "until March until I reach my goal"
    return random.choice([
        f"until {random_date()}",
        "until I reach my goal",
        "but skip holidays",
        ""
    ])

def maybe_conflicting_goal(goal: str):
    if random.random() < 0.2:
        return f"{goal} for {random.choice(GOALS)}"
    return goal

def build_prompt(intent, amount, freq, goal, group):
    parts = [
        f"Save {money_string(amount)}",
        maybe_conflicting_frequency(freq)
    ]

    if intent == "group_saving":
        parts.append(f"for {group}")
    else:
        parts.append(f"for {maybe_conflicting_goal(goal)}")

    condition = maybe_conflicting_condition()
    if condition:
        parts.append(condition)

    return inject_typos(" ".join(parts))

# =========================
# Interpretation Logic
# =========================

def interpret(prompt, intent, amount, freq, goal, group):
    needs_clarification = False
    issues = []

    currency, currency_conflict = extract_currency(prompt)
    if currency_conflict:
        needs_clarification = True
        issues.append("currency")

    frequency = freq
    if "every" in prompt and "times" in prompt:
        frequency = None
        needs_clarification = True
        issues.append("frequency")

    condition = None
    end_date = None
    if prompt.count("until") > 1:
        needs_clarification = True
        issues.append("condition")
    elif "reach my goal" in prompt:
        condition = "until goal reached"
    elif "skip holidays" in prompt:
        condition = "skip holidays"
    elif "until" in prompt:
        condition = "until a date"
        end_date = random_date()

    if intent == "individual_saving" and prompt.count("for") > 1:
        needs_clarification = True
        issues.append("goal")

    amount_value = amount if random.random() > 0.1 else None
    if amount_value is None:
        needs_clarification = True
        issues.append("amount")

    data = {
        "amount": amount_value,
        "currency": currency,
        "frequency": frequency,
        "day_of_week": random.choice(DAYS) if frequency == "weekly" else None,
        "start_date": None,
        "end_date": end_date,
        "conditions": condition
    }

    clarification_question = (
        generate_clarification(issues) if needs_clarification else None
    )

    interpretation = {
        "intent": intent,
        "goal": goal if intent == "individual_saving" else None,
        "group": group if intent == "group_saving" else None,
        "data": data,
        "needs_clarification": needs_clarification,
        "clarification_question": clarification_question,
        "raw_prompt": prompt,
        "confidence": confidence_from_nulls(data)
    }

    return interpretation

# =========================
# Dataset Generation
# =========================

samples = []

for i in range(NUM_SAMPLES):
    intent = random.choice(INTENTS)
    amount = random_amount()
    freq = random.choice(FREQUENCIES)
    goal = random.choice(GOALS)
    group = random.choice(GROUPS) if intent == "group_saving" else None

    prompt = build_prompt(intent, amount, freq, goal, group)

    interpretation = interpret(
        prompt=prompt,
        intent=intent,
        amount=amount,
        freq=freq,
        goal=goal,
        group=group
    )

    samples.append({
        "prompt": prompt,
        "interpretation": interpretation
    })

with open("training_samples.json", "w", encoding="utf-8") as f:
    json.dump(samples, f, indent=2)
