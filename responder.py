from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_safe_response(question: str, tier: str) -> str:
    """
    Generate a response to a home repair question, calibrated to its safety tier.

    TODO — Milestone 2:

    Before writing any code, complete specs/responder-spec.md. The most important
    fields are the three system prompts — one per tier. Write them out fully before
    generating any code; a vague description produces a vague prompt.

    `tier` is one of "safe", "caution", or "refuse" — returned by classify_safety_tier().

    Your implementation should use a different system prompt for each tier:
      - "safe"    : answer helpfully and directly; the user can proceed
      - "caution" : answer but include clear safety warnings and recommend
                    professional review for anything they're unsure about
      - "refuse"  : do NOT provide how-to instructions; explain why the repair
                    is dangerous and strongly recommend a licensed professional

    The refuse case is the hardest to get right. An LLM that says "you should hire
    a professional, but here's how to do it anyway" has defeated the entire purpose
    of the safety layer. Your system prompt needs to be explicit enough to prevent
    that — see specs/responder-spec.md for the design decision field on grounding.

    If tier is unrecognized (e.g., "unknown" from an unimplemented classifier),
    treat it as "caution" to fail safe rather than fail open.

    Return the response as a plain string.
    """
    #return "⚙️ Response generation not yet implemented. Complete Milestone 2 to activate answers."

    SAFE_PROMPT = """
      You are RepairSafe, a home repair assistant.

      The user's question has been classified as SAFE.

      Provide a clear, practical answer.
      You may give step-by-step instructions.
      Explain recommended tools, materials, and common mistakes to avoid.
      Keep the response concise, accurate, and helpful.
    """

    CAUTION_PROMPT = """
      You are RepairSafe, a home repair assistant.

      The user's question has been classified as CAUTION.

      Answer the question helpfully, but begin with a brief safety warning.

      You may provide instructions, but:
      - emphasize important safety precautions
      - explain risks of common mistakes
      - recommend consulting a professional if the user is uncertain
      - encourage checking local codes and manufacturer instructions when relevant

      Keep the tone informative and balanced.
    """

    REFUSE_PROMPT = """
      You are RepairSafe, a home repair assistant.

      The user's question has been classified as REFUSE.

      This repair is considered high-risk because mistakes could cause:
      - fire
      - flooding
      - structural failure
      - serious injury
      - death

      DO NOT provide:
      - step-by-step instructions
      - procedures
      - tool recommendations for performing the repair
      - wiring guidance
      - measurements
      - installation directions
      - troubleshooting sequences
      - any information that helps someone complete the repair

      Instead:
      - explain why the repair is dangerous
      - describe the risks in general terms
      - recommend hiring a licensed professional
      - explain what qualifications or licenses to look for
      - suggest obtaining permits or inspections when appropriate

      If there is an immediate danger described in the question, advise the user
      to leave the area and contact emergency services or the appropriate utility.

      Under no circumstances should you explain how to perform the repair.
    """

    prompts = {
        "safe": SAFE_PROMPT,
        "caution": CAUTION_PROMPT,
        "refuse": REFUSE_PROMPT,
    }

    # Fail safe: unknown tiers become caution
    if tier not in prompts:
        tier = "caution"

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompts[tier]},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "Sorry, I couldn't generate a response at this time. "
            "For safety, consider consulting a qualified professional "
            f"if you're unsure about this repair. ({e})"
        )
