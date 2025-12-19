# data/gen.py

import json
import secrets
import datetime
import random

# Use SystemRandom for float-based randomness where secrets doesn't provide a direct equivalent
secure_gen = random.SystemRandom()

# =========================
# Configuration
# =========================

NUM_SAMPLES = 1000

INTENTS = ["individual_saving", "group_saving"]
# Simulated Database of Groups
GROUP_DATABASE = [
    {"id": 1, "name": "family"},
    {"id": 2, "name": "roommates"},
    {"id": 3, "name": "trip"},
    {"id": 4, "name": "wedding"},
    {"id": 5, "name": "friends"},
    {"id": 6, "name": "hiking club"},
    {"id": 7, "name": "colleagues"},
    {"id": 8, "name": "band"},
    {"id": 9, "name": "travel buddies"},
    {"id": 10, "name": "apartment"},
    {"id": 11, "name": "startup"},
    {"id": 12, "name": "neighbors"}
]
GROUPS = [g["name"] for g in GROUP_DATABASE]
GROUP_SYNONYMS = ["group", "squad", "pool", "pot", "savings", "fund", "team", "circle"]
GOALS = [
    "gym", "rent", "vacation", "groceries", "emergency fund", "new phone",
    "laptop", "bitcoin", "gifts", "car", "insurance", "investment", "education",
    "concert", "gaming pc", "charity", "house downpayment"
]

FREQUENCIES = ["daily", "weekly", "monthly", "n-times", "bi-weekly", "fortnightly", "quarterly"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "weekend", "weekday"]

SAVING_VERBS = [
    "Save", "Put aside", "Stash", "Deposit", "Transfer", "Add", "Invest", "Move", 
    "Set aside", "Keep", "Allocate", "Budget"
]

PROMPT_PREFIXES = [
    "", "I want to ", "Please ", "Hey Buddy, ", "Can you ", "Start to ", 
    "I'd like to ", "Automatically ", "Setup a plan to ", "Need to "
]


def format_amount(amount):
    if secure_gen.random() < 0.3:
        return f"{amount}.{secrets.randbelow(100):02d}"
    return str(amount)

CURRENCY_FORMATS = [
    lambda a: f"€{format_amount(a)}",
    lambda a: f"{format_amount(a)}€",
    lambda a: f"EUR{format_amount(a)}",
    lambda a: f"EUR {format_amount(a)}",
    lambda a: f"{format_amount(a)} EUR",
    lambda a: f"${format_amount(a)}",
    lambda a: f"{format_amount(a)} USD",
    lambda a: f"USD{format_amount(a)}",
    lambda a: f"USD {format_amount(a)}",
    lambda a: f"£{format_amount(a)}",
    lambda a: f"{format_amount(a)} GBP",
    lambda a: f"GBP {format_amount(a)}",
    lambda a: f"PLN {format_amount(a)}",
    lambda a: f"PLN{format_amount(a)}",
    lambda a: f"{format_amount(a)}zł",
    lambda a: f"{format_amount(a)}zl",
    lambda a: f"{format_amount(a)} zl",
    lambda a: f"{format_amount(a)} zł",
    lambda a: f"{format_amount(a)} bucks",
    lambda a: f"{format_amount(a)} quid",
]

TYPO_MAP = {
    "save": ["svae", "saev", "sav", "sve", "seve"],
    "every": ["evry", "evey", "evvery", "evryone"],
    "weekly": ["wekly", "weekyl", "wekely", "weely"],
    "monthly": ["montly", "monhtly", "mothly"],
    "until": ["untill", "til", "till", "untl"],
    "Wednesday": ["wednedsay", "wednsday", "wednesday"],
    "Thursday": ["thrusday", "thursdy"],
    "emergency": ["emergncy", "emergensy"],
    "vacation": ["vaca", "vaction"],
    "friends": ["freinds", "frends"],
    "deposit": ["depost", "deposite"],
    "quarterly": ["quaterly", "quartely"]
}

# =========================
# Utilities
# =========================

def random_amount():
    return secrets.randbelow(496) + 5  # 5 to 500

def random_date():
    start = datetime.date.today()
    end = start + datetime.timedelta(days=secure_gen.randint(30, 365))
    random_days = secure_gen.randint(0, (end - start).days)
    return str(start + datetime.timedelta(days=random_days))

def inject_typos(text: str) -> str:
    for word, typos in TYPO_MAP.items():
        if word.lower() in text.lower() and secure_gen.random() < 0.3:
            text = text.replace(word, secrets.choice(typos))
    if secure_gen.random() < 0.15:
        text = text.replace(" ", "")
    return text


def extract_currency(prompt: str):
    currencies = set()

    if any(kw in prompt for kw in ("€", "EUR", "euro")):
        currencies.add("EUR")
    if any(kw in prompt for kw in ("$", "USD", "bucks")):
        currencies.add("USD")
    if any(kw in prompt for kw in ("£", "GBP", "quid")):
        currencies.add("GBP")
    if any(kw in prompt for kw in ("zł", "PLN", "zl", "zloty", "złoty")):
        currencies.add("PLN")

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
    return secrets.choice(CURRENCY_FORMATS)(amount)

def frequency_phrase(freq: str) -> str:
    if freq == "daily":
        return secrets.choice(["every day", "daily", "each day", "on a daily basis"])
    if freq == "weekly":
        return secrets.choice([f"every {secrets.choice(DAYS)}", "weekly", "each week", "once a week"])
    if freq == "monthly":
        return secrets.choice(["every month", "monthly", "each month", "once a month", "at the end of the month"])
    if freq == "fortnightly":
        return secrets.choice(["every two weeks", "fortnightly", "bi-weekly"])
    if freq == "quarterly":
        return secrets.choice(["every three months", "quarterly", "each quarter"])
    if freq == "bi-weekly":
        return "bi-weekly"
    return secrets.choice([f"{secure_gen.randint(2, 10)} times", f"{secure_gen.randint(2, 5)} times a week"])

def maybe_conflicting_frequency(freq: str):
    if secure_gen.random() < 0.20:
        return f"{frequency_phrase(freq)} and also {frequency_phrase(secrets.choice(FREQUENCIES))}"
    return frequency_phrase(freq)

def maybe_conflicting_condition():
    if secure_gen.random() < 0.20:
        return "until March until I reach my goal"
    return secrets.choice([
        f"until {random_date()}",
        "until I reach my goal",
        "but skip holidays",
        "starting from next week",
        "as long as I have money",
        ""
    ])

def maybe_conflicting_goal(goal: str):
    if secure_gen.random() < 0.15:
        return f"{goal} for {secrets.choice(GOALS)}"
    return goal

def build_prompt(intent, amount, freq, goal, group):
    prefix = secrets.choice(PROMPT_PREFIXES)
    verb = secrets.choice(SAVING_VERBS)
    
    parts = [
        f"{prefix}{verb} {money_string(amount)}",
        maybe_conflicting_frequency(freq)
    ]

    if intent == "group_saving":
        group_ref = secrets.choice([
            f"{group}",
            f"the {group} {secrets.choice(GROUP_SYNONYMS)}",
            f"my {group} {secrets.choice(GROUP_SYNONYMS)}",
            f"our {group} {secrets.choice(GROUP_SYNONYMS)}",
            f"{group} squad",
            f"existing {group} group",
            f"existing {group} squad",
            f"the {group} squad",
            f"my {group} squad"
        ])
        parts.append(secrets.choice(["for", "to", "with", "into", "towards"]))
        parts.append(group_ref)
    else:
        parts.append(f"for {maybe_conflicting_goal(goal)}")

    condition = maybe_conflicting_condition()
    if condition:
        parts.append(condition)

    return inject_typos(" ".join(filter(None, parts)))

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

    is_existing_group = False
    if intent == "group_saving":
        # Logic to detect if the prompt refers to an existing group
        existing_keywords = ["existing", "my ", "our ", "the ", "towards "]
        if any(kw in prompt.lower() for kw in existing_keywords):
            is_existing_group = True
        
        # Also check for group synonyms that strongly suggest an existing pot
        pot_keywords = ["pot", "pool", "circle", "squad", "fund", "team"]
        if any(kw in prompt.lower() for kw in pot_keywords):
             is_existing_group = True

    group_id = None
    if intent == "group_saving" and is_existing_group:
        # Find the ID from the database based on the name
        for g in GROUP_DATABASE:
            if g["name"] == group:
                group_id = g["id"]
                break

    data = {
        "amount": amount_value,
        "currency": currency,
        "frequency": frequency,
        "day_of_week": secrets.choice(DAYS) if frequency == "weekly" else None,
        "start_date": None,
        "end_date": end_date,
        "conditions": condition,
        "is_existing_group": is_existing_group,
        "group_name": group if intent == "group_saving" else None,
        "group_id": group_id
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
        "raw_prompt": prompt
    }

    return interpretation

# =========================
# Dataset Generation
# =========================

samples = []

for i in range(NUM_SAMPLES):
    intent = secrets.choice(INTENTS)
    amount = random_amount()
    freq = secrets.choice(FREQUENCIES)
    goal = secrets.choice(GOALS)
    
    # Generate a random subset of groups representing "user's groups"
    available_groups = secure_gen.sample(GROUP_DATABASE, secure_gen.randint(2, 6))
    
    # If group saving, pick one that is likely to be "mine"
    group_obj = secrets.choice(available_groups)
    group = group_obj["name"] if intent == "group_saving" else None

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
        "context": {
            "user_groups": available_groups
        },
        "interpretation": interpretation
    })

with open("training_samples.json", "w", encoding="utf-8") as f:
    json.dump(samples, f, indent=2)