"""
Simple standalone test for command parsing logic.
This can run without the full huckleberry-api dependencies.
"""

import re
from typing import Dict, Tuple, Optional, Any


def parse_command(command: str) -> Tuple[Optional[str], Dict[str, Any]]:
    """Parse voice command - same logic as main.py"""
    if not command:
        return None, {}

    cmd = command.lower().strip()
    activity_type = None
    details: Dict[str, Any] = {}

    # Bottle feeding
    bottle_keywords = ['bottle']
    if any(keyword in cmd for keyword in bottle_keywords):
        activity_type = 'bottle'
        ml_match = re.search(r'(\d+)\s*ml', cmd)
        oz_match = re.search(r'(\d+(?:\.\d+)?)\s*oz', cmd)
        if ml_match:
            details['amount_ml'] = int(ml_match.group(1))
        elif oz_match:
            oz_amount = float(oz_match.group(1))
            details['amount_ml'] = int(oz_amount * 29.5735)
        else:
            details['amount_ml'] = 120

    # Breastfeeding
    feed_keywords = ['feed', 'feeding', 'breast', 'nurse', 'nursing']
    if not activity_type and any(keyword in cmd for keyword in feed_keywords):
        activity_type = 'feed'
        if 'right' in cmd:
            details['side'] = 'right'
        elif 'left' in cmd:
            details['side'] = 'left'
        else:
            details['side'] = 'left'

    # Sleep
    sleep_keywords = ['sleep', 'nap', 'sleeping', 'napping']
    if not activity_type and any(keyword in cmd for keyword in sleep_keywords):
        activity_type = 'sleep'

    # Diaper
    diaper_keywords = ['diaper', 'poo', 'poop', 'pee', 'wee', 'wet']
    if not activity_type and any(keyword in cmd for keyword in diaper_keywords):
        activity_type = 'diaper'
        has_poo = any(word in cmd for word in ['poo', 'poop'])
        has_pee = any(word in cmd for word in ['pee', 'wee', 'wet'])

        if has_poo and has_pee:
            details['type'] = 'both'
        elif has_poo:
            details['type'] = 'poo'
        elif has_pee:
            details['type'] = 'pee'
        else:
            details['type'] = 'poo'

        if details['type'] in ['poo', 'both']:
            if any(word in cmd for word in ['big', 'large', 'huge']):
                details['poo_size'] = 'large'
            elif any(word in cmd for word in ['small', 'tiny', 'little']):
                details['poo_size'] = 'small'
            elif 'medium' in cmd:
                details['poo_size'] = 'medium'

            if 'yellow' in cmd:
                details['poo_color'] = 'yellow'
            elif 'brown' in cmd:
                details['poo_color'] = 'brown'
            elif 'green' in cmd:
                details['poo_color'] = 'green'
            elif 'dark' in cmd:
                details['poo_color'] = 'dark'
            elif 'black' in cmd:
                details['poo_color'] = 'black'

        if details['type'] in ['pee', 'both']:
            if any(word in cmd for word in ['big', 'large', 'huge']):
                details['pee_amount'] = 'large'
            elif any(word in cmd for word in ['small', 'tiny', 'little']):
                details['pee_amount'] = 'small'
            else:
                details['pee_amount'] = 'medium'

    return activity_type, details


def test_parsing():
    """Test command parsing"""
    tests = [
        ("log a poo", "diaper", {"type": "poo"}),
        ("log a big yellow poo", "diaper", {"type": "poo", "poo_size": "large", "poo_color": "yellow"}),
        ("log a left feed", "feed", {"side": "left"}),
        ("log a right feed", "feed", {"side": "right"}),
        ("log a feed", "feed", {"side": "left"}),
        ("log a 120ml bottle", "bottle", {"amount_ml": 120}),
        ("log a bottle", "bottle", {"amount_ml": 120}),
        ("start sleep", "sleep", {}),
        ("log a pee", "diaper", {"type": "pee"}),
        ("log a poo and pee", "diaper", {"type": "both"}),
        ("", None, {}),
    ]

    passed = 0
    failed = 0

    for command, expected_type, expected_details in tests:
        activity_type, details = parse_command(command)

        if activity_type == expected_type:
            # Check if all expected details are present
            all_match = all(details.get(k) == v for k, v in expected_details.items())
            if all_match:
                print(f"✓ PASS: '{command}'")
                passed += 1
            else:
                print(f"✗ FAIL: '{command}' - Details mismatch")
                print(f"  Expected: {expected_details}")
                print(f"  Got: {details}")
                failed += 1
        else:
            print(f"✗ FAIL: '{command}'")
            print(f"  Expected type: {expected_type}")
            print(f"  Got type: {activity_type}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{passed + failed}")
    print(f"Tests failed: {failed}/{passed + failed}")
    print(f"{'='*50}")

    return failed == 0


if __name__ == '__main__':
    success = test_parsing()
    exit(0 if success else 1)
