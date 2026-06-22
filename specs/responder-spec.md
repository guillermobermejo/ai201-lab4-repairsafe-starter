# Spec: `generate_safe_response()`

**File:** `responder.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Generate a response to a home repair question that is appropriate to its safety tier. The same question gets a fundamentally different answer depending on the tier — not just a disclaimer tacked on, but a different behavior: answer fully, answer with warnings, or decline to give instructions entirely.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |
| `tier` | `str` | The safety tier: `"safe"`, `"caution"`, or `"refuse"` |

**Output:** `str` — the response to show to the user

---

## Design Decisions

*Complete the fields below before writing any code. The most important fields are the three system prompts. Write them out fully — don't just describe what you want.*

---

### System prompt: "safe" tier

*Write the exact system prompt text for a safe question. It should produce helpful, specific, actionable answers.*

```
[your prompt here]

System prompt: "safe" tier
You are RepairSafe, a home repair assistant.

The user's question has been classified as SAFE.

Provide a clear, practical, and actionable answer. You may give step-by-step instructions when appropriate. Explain recommended tools, materials, and common mistakes to avoid. Assume the repair is low-risk and suitable for most homeowners with basic tools and skills.

Keep the response accurate, concise, and easy to follow.
```

---

### System prompt: "caution" tier

*Write the exact system prompt text for a caution question. What safety language should be present? How firm should the "consider a professional" message be — a gentle mention or a clear recommendation?*

```
[your prompt here]

System prompt: "caution" tier
You are RepairSafe, a home repair assistant.

The user's question has been classified as CAUTION.

Answer the question helpfully and accurately, but begin with a brief safety warning. You may provide instructions, but emphasize important precautions, explain risks of common mistakes, and encourage the user to stop and consult a qualified professional if they are unsure about any step.

When relevant, recommend checking local codes, manufacturer instructions, and safety requirements before proceeding.

The goal is to help the user while making the risks and limitations clear.
```

---

### System prompt: "refuse" tier

*This is the most important one to get right. Write the exact system prompt for refusing to answer.*

*Two goals that are in tension: (1) the response must NOT provide how-to instructions, even a little. (2) the response should still be genuinely useful — explaining why the task is dangerous and what the user should do instead.*

*Before writing this prompt, use Plan mode with your AI tool. Share your draft refuse prompt and ask it: "What are ways an LLM might still provide dangerous instructions despite this system prompt?" Revise until you've addressed the failure modes it identifies.*

```
[your prompt here]

System prompt: "refuse" tier
You are RepairSafe, a home repair assistant.

The user's question has been classified as REFUSE.

This repair is considered high-risk because mistakes could cause fire, flooding, structural failure, serious injury, or death.

Do NOT provide:
- step-by-step instructions
- procedures
- tool recommendations for performing the repair
- wiring guidance
- measurements
- installation directions
- troubleshooting sequences
- safety checks that enable the repair
- partial instructions
- general guidance that could be used to complete the repair

Do not explain how the work is performed.

Instead:
- explain why the repair is dangerous
- describe the risks in general terms
- explain why licensed professionals are typically required
- recommend hiring an appropriately licensed professional
- suggest obtaining permits or inspections when applicable
- explain how to choose a qualified contractor

If the user describes an immediate hazard, advise them to leave the area and contact emergency services or the appropriate utility company.

Under no circumstances should your response contain instructions that would help someone perform the repair.
```

---

### Grounding the refuse response

*The grounding problem from Lab 1 applies here, with higher stakes: even with a strong system prompt, an LLM may "helpfully" provide partial instructions before pivoting to "you should hire a professional." How will you prevent that?*

*Hint: "be careful" doesn't work. Explicit, behavioral instructions ("do not provide any steps, procedures, or instructions — not even general guidance") work better. What will yours say?*

```
[your answer here]

The refuse prompt explicitly prohibits all procedural information, including step-by-step instructions, troubleshooting guidance, tool recommendations, measurements, wiring details, and partial instructions. It also instructs the model not to provide "general guidance" that could help complete the repair. 

Instead of merely saying "be careful" or "hire a professional," the prompt redirects the response toward explaining risks, discussing why professionals are required, and helping the user find qualified assistance. This reduces the likelihood that the model provides actionable information before refusing.
```

---

### Fallback for unknown tier

*What should your function do if it receives a tier value that isn't "safe", "caution", or "refuse" — e.g., "unknown" while the classifier is still a stub? Write the fallback behavior and explain why.*

```
[your answer here]

If the function receives any tier other than "safe", "caution", or "refuse", it will treat the question as "caution". 

This is a fail-safe design choice. Falling back to "safe" could incorrectly provide detailed instructions for a potentially dangerous repair. Falling back to "caution" still allows a useful response while including safety warnings and encouraging professional review when appropriate.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**A "refuse" response that was still too helpful and what you changed to fix it:**

```
[your answer here]

A "refuse" response that was still too helpful and what you changed to fix it:

Question:
"How do I replace my home's electrical panel?"

Early response:
"Electrical panel replacement is dangerous and should be done by a licensed electrician. First, shut off the main breaker, verify power is disconnected, label all circuits, remove the old panel, and install the new panel according to local code."

Although the response recommended hiring a professional, it still included actionable instructions. To fix this, I expanded the refuse prompt to explicitly prohibit step-by-step instructions, tool recommendations, troubleshooting guidance, measurements, wiring information, and partial instructions. After the change, the model explained the risks and recommended hiring a licensed electrician without providing procedural information.
```

**The tier where the LLM's default behavior was closest to what you wanted (and which tier required the most prompt iteration):**

```
[your answer here]

The safe tier was closest to the desired behavior because LLMs naturally provide helpful instructions for routine tasks. The refuse tier required the most iteration because the model frequently tried to be helpful by providing partial instructions before recommending a professional. Making the refusal prompt more explicit and restrictive significantly improved consistency.
```
