import json
import os
from datetime import datetime
from config import LOG_FILE


def log_interaction(question: str, tier: str, response: str) -> None:
    """
    Append a structured record of this interaction to the audit log.

    TODO — Milestone 3:

    Before writing any code, complete specs/auditor-spec.md. The key decisions
    are what fields to log, how much of the question and response to include,
    and how to handle the logs/ directory not existing yet.

    Each record should be a JSON object written as a single line to LOG_FILE
    (defined in config.py as "logs/audit.jsonl").

    Required fields:
      - "timestamp"        : ISO 8601 datetime string
      - "tier"             : the safety tier assigned to this question
      - "question"         : the user's question (truncate to 300 chars if longer)
      - "response_preview" : first 200 characters of the response

    If the logs/ directory doesn't exist, create it before writing.

    Also print a one-line summary to the terminal so you can see logged
    interactions in real time without opening the file:
      e.g. [LOGGED] tier=caution | "How do I replace a faucet?" → 47 chars

    Design your log entry in specs/auditor-spec.md before implementing here.
    """
    #pass

    # Create logs directory if needed
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # Truncate fields according to spec
    truncated_question = question[:300]
    response_preview = response[:200]

    record = {
        "timestamp": datetime.now().isoformat(),
        "tier": tier,
        "question": truncated_question,
        "response_preview": response_preview,
    }

    # Append one JSON object per line
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    # Console summary
    preview_question = (
        truncated_question[:50] + "..."
        if len(truncated_question) > 50
        else truncated_question
    )

    print(
        f'[LOGGED] tier={tier} | "{preview_question}" → {len(response)} chars'
    )