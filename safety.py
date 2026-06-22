from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing any code, complete specs/classifier-spec.md. The blank fields
    there are the decisions that drive this implementation — prompt design, tier
    definitions, output format, and edge case handling.

    Your implementation should:
      1. Build a prompt using your tier definitions that asks the LLM to classify
         the question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the raw response text
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the
         response can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned

    The three tiers:
      - "safe"    : routine, low-risk repairs most homeowners can handle safely
      - "caution" : doable with care, but mistakes have real cost or mild risk
      - "refuse"  : high-risk repairs that require a licensed professional —
                    mistakes can cause fire, flooding, injury, or structural damage
    """
    #return {
    #    "tier": "unknown",
    #    "reason": "Classification not yet implemented. Complete Milestone 1.",
    #}

    system_prompt = """
      You are a home-repair safety classifier.

      Classify the user's question into exactly one tier:

      safe:
      - Routine maintenance and low-risk repairs.
      - Most homeowners can safely perform them.
      - Examples: patching drywall, painting, replacing a light bulb,
        unclogging a drain, tightening hardware, replacing weather stripping.

      caution:
      - Requires some skill or care.
      - Mistakes may be costly or cause minor injury/property damage.
      - Examples: replacing a faucet, resetting a GFCI outlet,
        replacing a toilet flapper, installing a ceiling fan,
        basic tile work.

      refuse:
      - Mistakes can cause fire, flooding, structural failure,
        serious injury, or death.
      - May require a licensed professional or code compliance.
      - Examples: electrical panel work, gas line repair,
        structural modifications, main water line work,
        load-bearing wall removal, roof framing.

      Important rule:
      If you are unsure between caution and refuse, choose refuse.

      Respond in exactly this format:

      TIER: <safe|caution|refuse>
      REASON: <one brief sentence>
      """

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0,
        )

        raw_text = response.choices[0].message.content.strip()

        tier_match = re.search(
            r"TIER:\s*[\"']?\s*(safe|caution|refuse)\s*[\"']?",
            raw_text,
            flags=re.IGNORECASE,
        )

        if tier_match:
            tier = tier_match.group(1).strip().lower()
        else:
            tier = "caution"

        if tier not in VALID_TIERS:
            tier = "caution"

        reason_match = re.search(
            r"REASON:\s*(.+)",
            raw_text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not tier_match:
            return {
                "tier": "caution",
                "reason": "Could not reliably classify question.",
            }

        tier = tier_match.group(1).lower()

        if tier not in VALID_TIERS:
            tier = "caution"

        reason = (
            reason_match.group(1).strip()
            if reason_match
            else "No reason provided."
        )

        return {
            "tier": tier,
            "reason": reason,
        }

    except Exception as e:
        return {
            "tier": "caution",
            "reason": f"Classification error: {str(e)}",
        }