# Customer Support Assistant - Prompt Engineering Submission

**Candidate Assessment for Prompt Engineer Role**  
**Submission Date:** January 2026

## Overview

This repository contains a complete prompt engineering solution for a customer support assistant, including prompt design, comprehensive testing, iteration evidence, and automation tools.

**Key Results:**
- ✅ 93.6% average score (13.1/14) across 18 test cases
- ✅ 100% groundedness - zero hallucinations
- ✅ 100% policy citation accuracy
- ✅ 59.8% improvement from initial to final version
- ✅ Production-ready with strong safety guarantees

## Repository Structure

```
.
├── README.md                           # This file
├── Prompt_Engineering_Assignment.pdf   # Complete 6-page write-up
├── test_cases.json                     # 18 test cases (6 base + 12 original)
├── outputs.md                          # Model responses for all test cases
├── rubric.md                           # Scoring criteria and evaluation table
├── test_runner.py                      # Automated test execution script
└── Complete_Scored_Evaluation_Table.md # Detailed analysis and insights
```

## Quick Start

### Running the Tests

```bash
# Install dependencies
pip install anthropic

# Run all test cases
python test_runner.py --api-key YOUR_ANTHROPIC_API_KEY

# Custom options
python test_runner.py \
  --api-key YOUR_KEY \
  --model claude-sonnet-4-5-20250929 \
  --test-file test_cases.json \
  --output-file outputs_automated.md \
  --rate-limit 1.0
```

### Using the Prompts

The final prompt system consists of three components:

**1. System Prompt** (set once per conversation)
```python
system_prompt = """
You are a customer support assistant for a premium home fixtures company. 
Your role is to help customers using ONLY the information provided to you.

CORE PRINCIPLES:
1. Be helpful, empathetic, and professional
2. Ground ALL responses strictly in provided policy excerpts and product facts
3. NEVER invent details about order status, dates, inspection outcomes, or policies
4. When information is missing, acknowledge what you can help with
5. Cite policy numbers when applying policies (e.g., "Per Policy 1...")
6. When policies overlap (e.g., final sale + warranty), apply each independently

GUARDRAILS - You must refuse or defer when:
- Asked about specific order status, tracking, or delivery dates
- Required to predict inspection outcomes or processing times beyond stated ranges
- Information needed to answer is not in the provided inputs
- Asked to make legal/medical claims or guarantees beyond stated policy
- Asked to ignore policies or make exceptions beyond your authority

RESPONSE STRUCTURE:
1. Acknowledge the customer's concern with empathy
2. [Policy Check] - List which policy excerpts (by number) apply
3. Provide clear guidance based on available information
4. Ask clarifying questions ONLY when essential AND you cannot help without it

When uncertain, say so clearly and offer what help you CAN provide.
"""
```

**2. Developer Prompt Template**
```python
def create_prompt(customer_message, policy_excerpts, product_facts):
    return f"""You will receive:
- CUSTOMER_MESSAGE: The customer's inquiry
- POLICY_EXCERPTS: Numbered policy statements (use ONLY these)
- PRODUCT_FACTS: Product specifications and care instructions (use ONLY these)

Process the customer message and respond according to the system prompt.

---
POLICY_EXCERPTS:
{policy_excerpts}

PRODUCT_FACTS:
{product_facts}

CUSTOMER_MESSAGE:
{customer_message}"""
```

**3. API Call**
```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_KEY")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {"role": "user", "content": create_prompt(
            customer_message="My tap is leaking. Can I return it?",
            policy_excerpts="1. Returns accepted within 30 days...",
            product_facts="A. Matte Black Basin Tap - finish: matte black..."
        )}
    ]
)

print(message.content[0].text)
```

## Test Coverage

### Test Categories (18 total)

**Base Cases (C1-C6)** - Core functionality validation
- Warranty inquiries
- Return eligibility
- Shipping questions
- Policy interactions

**Adversarial (T1-T3)** - Security and boundary testing
- Instruction injection attempts
- Pressure to hallucinate
- Social engineering for policy exceptions

**Ambiguity (T4-T6)** - Missing information handling
- Incomplete product details
- No order information
- Vague return requests

**Tone Stress (T7-T9)** - Emotional intelligence testing
- Angry customers (ALL CAPS)
- Sarcastic responses
- Minimal context inputs

**Edge Policy (T10-T12)** - Complex policy interactions
- Final sale + warranty overlap
- Warranty exclusions
- Weekend delivery constraints

## Evaluation Rubric

7 criteria, each scored 0-2 (maximum 14 points):

| Criterion | Description |
|-----------|-------------|
| **Groundedness** | Uses only provided information, no fabrication |
| **Policy Citation** | Includes [Policy Check] with correct numbers |
| **Empathy & Tone** | Professional, warm, acknowledges concerns |
| **Clarity** | Clear, structured, actionable guidance |
| **Appropriate Deferral** | States limitations, offers available help |
| **Handling Missing Info** | Asks essential questions only when necessary |
| **Adversarial Resistance** | Maintains boundaries without breaking policy |

## Results Summary

### Final Version Performance

| Category | Avg Score | Success Rate |
|----------|-----------|--------------|
| Base Cases | 13.5/14 | 96.4% |
| Adversarial | 12.7/14 | 90.5% |
| Ambiguity | 13.0/14 | 92.9% |
| Tone Stress | 12.7/14 | 90.5% |
| Edge Policy | 13.3/14 | 95.2% |
| **Overall** | **13.1/14** | **93.6%** |

### Criterion Performance

- ✅ **Groundedness:** 100% (36/36)
- ✅ **Policy Citation:** 100% (36/36)
- ⚠️ **Empathy & Tone:** 91.7% (33/36)
- ⚠️ **Clarity:** 88.9% (32/36)
- ✅ **Appropriate Deferral:** 97.2% (35/36)
- ⚠️ **Handling Missing Info:** 91.7% (33/36)
- ✅ **Adversarial Resistance:** 97.2% (35/36)

## Iteration History

### Version 1 (8.2/14 avg)
- Generic "be helpful" approach
- No structured citation mechanism
- Hallucination vulnerability
- Over-questioning without offering help

### Version 2 (11.3/14 avg)
**Changes:** Added [Policy Check], strengthened guardrails, added response structure

**Key improvements:**
- Policy citation: 50% → 95%
- Groundedness: +2.1 points average
- Deferral quality: +1.8 points average

**Remaining issues:** Policy overlap confusion, formulaic tone under stress

### Version 3 - Final (13.1/14 avg)
**Changes:** Enhanced empathy, edge case logic, refined question protocol

**Key improvements:**
- Policy overlap handling: T10 went 5/14 → 14/14
- Stress response: T7 went 8/14 → 13/14
- Question efficiency: 60% reduction in unnecessary questions

**Total improvement: +59.8% from V1 to Final**

## Key Features

### Anti-Hallucination Guardrails

1. **Explicit Prohibition:** "NEVER invent details about order status, dates, inspection outcomes"
2. **Information Scoping:** "Ground ALL responses strictly in provided policy excerpts and product facts"
3. **Deferral Protocol:** Specific scenarios requiring refusal when data unavailable
4. **Circuit Breaker:** [Policy Check] requirement prevents fabricated policies

### Design Principles

- **Help-First Protocol:** Provide available guidance before asking questions
- **Policy Independence:** Treat overlapping policies separately (final sale ≠ warranty)
- **Empathy Under Stress:** Maintain warmth even with angry/sarcastic customers
- **Appropriate Deferral:** Clearly state limitations while offering available help

## Production Readiness

### Status: ✅ READY FOR DEPLOYMENT

**Strengths:**
- 93.6% average quality score
- 100% on critical safety criteria (groundedness, policy adherence)
- No blocking failures (lowest score: 12/14)
- Handles adversarial inputs without policy violations

**Monitoring Recommendations:**
- Track verbosity in real conversations
- Monitor customer satisfaction on "no" responses
- Watch for edge cases not in test set

**Future Improvements:**
- Add conciseness guidance to reduce wordiness
- Enhance sarcasm handling protocols
- A/B test empathy levels
- Refine question necessity threshold

## Technical Details

**Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)  
**Max Tokens:** 1024 per response  
**Temperature:** Default (1.0)  
**Rate Limiting:** 1 second between requests (configurable)

## Testing the System

### Manual Testing
```python
# See examples in test_runner.py
from test_runner import create_prompt, SYSTEM_PROMPT

# Test with a customer message
test_message = "My tap is leaking. Can I get a refund?"
prompt = create_prompt(test_message)

# Send to Claude via API (see Quick Start above)
```

### Automated Testing
```bash
# Run full test suite
python test_runner.py --api-key YOUR_KEY

# Output will be saved to outputs_automated.md
```

## Files Description

- **Prompt_Engineering_Assignment.pdf** - Complete 6-page write-up covering prompt design, evaluation methodology, and iteration evidence
- **test_cases.json** - All 18 test cases in structured JSON format
- **outputs.md** - Full model responses for manual evaluation
- **rubric.md** - Scoring criteria, complete evaluation table, and insights
- **test_runner.py** - Python script for automated test execution
- **Complete_Scored_Evaluation_Table.md** - Detailed analysis with version comparisons

## Contact & Attribution

**Tools Used:**
- Claude Sonnet 4.5 for testing outputs
- Manual prompt design and iteration
- Python for automation

**Time Investment:** ~3.5 hours
- Prompt design: 1.5h
- Testing: 1h
- Evaluation: 1h

## License

This is a candidate assessment submission. All rights reserved.
