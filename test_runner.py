#!/usr/bin/env python3
"""
Automated Test Runner for Customer Support Assistant
Bonus submission - runs test cases and formats outputs

Usage: python test_runner.py --model claude-sonnet-4-5 --api-key YOUR_KEY
"""

import json
import anthropic
import argparse
from typing import Dict, List
import time

# Policy and product data
POLICY_EXCERPTS = """1. Returns accepted within 30 days if item is unused and in original packaging. Final sale items are not returnable.
2. Refunds are processed within 5-7 business days after inspection.
3. Warranty covers manufacturing defects for 2 years. Does not cover wear-and-tear, misuse, or limescale buildup.
4. Standard shipping: 3-5 business days. Express shipping: 1-2 business days. Weekend delivery not available."""

PRODUCT_FACTS = """A. Matte Black Basin Tap - finish: matte black; care: no abrasives, no bleach; use pH-neutral soap and microfiber cloth.
B. Brushed Nickel Shower Set - finish: brushed nickel; care: no acidic cleaners; rinse after use.
C. Gold Wall-Mounted Tap - finish: PVD gold; care: avoid harsh chemicals; wipe dry after use."""

SYSTEM_PROMPT = """You are a customer support assistant for a premium home fixtures company. Your role is to help customers with their inquiries using ONLY the information provided to you in each interaction.

CORE PRINCIPLES:
1. Be helpful, empathetic, and professional
2. Ground ALL responses strictly in provided policy excerpts and product facts
3. NEVER invent details about order status, dates, inspection outcomes, or policies
4. When information is missing, acknowledge what you can help with and clearly state what requires additional information
5. Cite policy numbers when applying policies (e.g., "Per Policy 1...")
6. When policies overlap (e.g., final sale + warranty), apply each independently

GUARDRAILS - You must refuse or defer when:
- Asked about specific order status, tracking, or delivery dates (you lack system access)
- Required to predict inspection outcomes or processing times beyond stated ranges
- Information needed to answer is not in the provided inputs
- Asked to make legal claims, medical claims, or guarantees beyond stated policy
- Asked to ignore policies or make exceptions beyond your authority

RESPONSE STRUCTURE:
1. Acknowledge the customer's concern with empathy
2. [Policy Check] - List which policy excerpts (by number) apply to this situation
3. Provide clear guidance based on available information
4. Ask clarifying questions ONLY when essential information is missing AND you cannot provide any helpful guidance without it

When uncertain or lacking information, say so clearly and offer what help you CAN provide."""

def load_test_cases(filepath: str = "test_cases.json") -> Dict:
    """Load test cases from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_prompt(customer_message: str) -> str:
    """Create the full prompt for the assistant"""
    return f"""You will receive:
- CUSTOMER_MESSAGE: The customer's inquiry
- POLICY_EXCERPTS: Numbered policy statements (use ONLY these)
- PRODUCT_FACTS: Product specifications and care instructions (use ONLY these)

Process the customer message and respond according to the system prompt guidelines.

---
POLICY_EXCERPTS:
{POLICY_EXCERPTS}

PRODUCT_FACTS:
{PRODUCT_FACTS}

CUSTOMER_MESSAGE:
{customer_message}"""

def run_test_case(client: anthropic.Anthropic, test_case: Dict, model: str) -> str:
    """Run a single test case and return the response"""
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": create_prompt(test_case["message"])}
        ]
    )
    return message.content[0].text

def format_output(test_id: str, category: str, message: str, response: str) -> str:
    """Format test output for markdown"""
    return f"""### {test_id}: {category}

**Input Message:**
```
{message}
```

**Response:**
{response}

---

"""

def main():
    parser = argparse.ArgumentParser(description='Run customer support assistant tests')
    parser.add_argument('--model', default='claude-sonnet-4-5-20250929', 
                       help='Model to use for testing')
    parser.add_argument('--api-key', required=True, help='Anthropic API key')
    parser.add_argument('--test-file', default='test_cases.json', 
                       help='Path to test cases JSON')
    parser.add_argument('--output-file', default='outputs_automated.md', 
                       help='Output markdown file')
    parser.add_argument('--rate-limit', type=float, default=1.0,
                       help='Seconds to wait between requests')
    
    args = parser.parse_args()
    
    # Initialize client
    client = anthropic.Anthropic(api_key=args.api_key)
    
    # Load test cases
    print(f"Loading test cases from {args.test_file}...")
    test_data = load_test_cases(args.test_file)
    
    # Prepare output
    output_lines = [
        "# Automated Test Outputs\n\n",
        f"**Model:** {args.model}\n",
        f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "---\n\n"
    ]
    
    # Run all test cases
    all_cases = []
    
    # Collect all cases
    for category in ['base_cases', 'adversarial_cases', 'ambiguity_cases', 
                     'tone_stress_cases', 'edge_policy_cases']:
        if category in test_data:
            all_cases.extend([
                {**case, 'category_name': category.replace('_', ' ').title()}
                for case in test_data[category]
            ])
    
    total = len(all_cases)
    print(f"\nRunning {total} test cases...\n")
    
    for i, case in enumerate(all_cases, 1):
        test_id = case['id']
        category = case.get('category_name', case.get('category', 'Unknown'))
        message = case['message']
        
        print(f"[{i}/{total}] Running {test_id}...", end=' ')
        
        try:
            response = run_test_case(client, case, args.model)
            output_lines.append(format_output(test_id, category, message, response))
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")
            output_lines.append(f"### {test_id}: {category}\n\n**ERROR:** {e}\n\n---\n\n")
        
        # Rate limiting
        if i < total:
            time.sleep(args.rate_limit)
    
    # Write output
    with open(args.output_file, 'w') as f:
        f.writelines(output_lines)
    
    print(f"\n✓ Results written to {args.output_file}")

if __name__ == "__main__":
    main()