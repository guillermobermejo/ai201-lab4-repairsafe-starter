# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
[your definition here]
Routine home maintenance or low-risk repairs that most homeowners can complete safely with basic tools and where mistakes are unlikely to cause injury or major property damage.
```

**caution:**
```
[your definition here]
Home repairs that require moderate skill or care and where mistakes may cause minor injury, equipment damage, leaks, or significant expense but are unlikely to cause fire, structural failure, serious injury, or death.
```

**refuse:**
```
[your definition here]
The LLM will be given both tier definitions and representative examples for each tier. It will classify the question directly rather than generating chain-of-thought reasoning. The prompt will instruct the model to choose the most conservative tier when a question is ambiguous. Questions near the boundary, such as outlet replacement or electrical work, should be classified as "refuse" whenever the potential consequences of an error include fire, electrocution, flooding, structural damage, or other serious harm.
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
[your answer here]
The LLM will be given both tier definitions and representative examples for each tier. It will classify the question directly rather than generating chain-of-thought reasoning. The prompt will instruct the model to choose the most conservative tier when a question is ambiguous. Questions near the boundary, such as outlet replacement or electrical work, should be classified as "refuse" whenever the potential consequences of an error include fire, electrocution, flooding, structural damage, or other serious harm.
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
[your answer here]
The model will be instructed to return exactly: 

TIER: <safe|caution|refuse> 
REASON: <brief explanation> 


Example: 

TIER: caution 

REASON: Replacing a faucet is a moderate-skill plumbing repair that can cause leaks if done incorrectly but is unlikely to create life-threatening hazards. The parser will extract the tier using a case-insensitive regex, normalize it to lowercase, validate it against VALID_TIERS, and default to "caution" if parsing fails.
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
[your prompt here]
You are a home repair safety classifier. 

Classify the user's repair question into exactly one tier. 

safe: 
- Routine maintenance and low-risk repairs. 
- Most homeowners can safely perform them. 
- Examples: patching drywall, painting, replacing a light bulb, unclogging a drain, tightening hardware, replacing weather stripping. 

caution: 
- Requires moderate skill, planning, or care. 
- Mistakes may cause leaks, property damage, minor injury, or costly repairs. 
- Examples: replacing a faucet, replacing a toilet flapper, resetting a GFCI outlet, installing a ceiling fan, basic tile work. 

refuse: 
- Mistakes can cause fire, flooding, structural failure, serious injury, or death. 
- Includes electrical panel work, gas line work, structural modifications, main water line repairs, load-bearing wall removal, roof framing, and similar high-risk repairs. 
- Choose refuse whenever the potential consequences of failure include major safety hazards. 

If uncertain between caution and refuse, choose refuse. 
Respond using exactly this format:

TIER: <safe|caution|refuse> 
REASON: <one brief sentence>
```

**User message:**
```
[your prompt here]
Classify this home repair question:
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
[your rule and examples here]

Rule: If performing the repair incorrectly could reasonably result in fire, flooding, structural failure, serious injury, or death, classify it as refuse; otherwise classify it as caution. 

Example 1: Question: "Can I replace my own electrical outlet?" Tier: refuse Reason: Although homeowners sometimes do this work, mistakes can cause electrical shock or fire hazards. 

Example 2: Question: "How do I replace a leaking bathroom faucet?" 

Tier: caution 
Reason: Incorrect installation may cause leaks or water damage, but the consequences are generally less severe than fire, structural failure, or serious injury.
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
[your answer here]

If the LLM response cannot be parsed or does not contain a recognizable tier, the function returns: 

{ "tier": "caution", "reason": "Could not reliably classify question." }
 
 If the extracted tier is not in VALID_TIERS after normalization and validation, the function also falls back to "caution". 
 
 Failing closed with "caution" is safer than failing open with "safe" because an incorrectly permissive classification could allow risky repairs to be treated as low-risk.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
[your answer here]

One classification that surprised you — question, tier you expected, tier it returned, and why:

Question: "Can I replace my own outlets?"
Expected: caution
Returned: refuse

The result makes sense because outlet replacement involves direct electrical wiring and mistakes can create shock or fire hazards, which places it on the refuse side of the boundary. 
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
[your answer here]

I added the instruction "If uncertain between caution and refuse, choose refuse." Before this change, the model sometimes classified electrical and plumbing questions inconsistently. The change made borderline high-risk questions much more conservative and consistent.
```
