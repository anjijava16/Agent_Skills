---
name: roll-dice
description: >
  Roll dice using a random number generator. Use when asked to roll a die
  (d4, d6, d8, d10, d12, d20, d100), roll multiple dice, or generate random
  dice rolls for tabletop RPGs, board games, or decision making.
license: MIT
metadata:
  author: welcome
  version: "1.0"
---

# Roll Dice

## When to use this skill

Use this skill when the user needs to:
- Roll a single die (d6, d20, etc.)
- Roll multiple dice (2d6, 4d8, etc.)
- Roll with modifiers (d20+5, 2d6-1)
- Generate random numbers for games or decisions

## Rolling a Single Die

Generate a random number from 1 to the given number of sides:

```bash
# Bash (macOS/Linux)
echo $((RANDOM % <sides> + 1))
```

```powershell
# PowerShell (Windows)
Get-Random -Minimum 1 -Maximum (<sides> + 1)
```

```python
# Python (more precise for large numbers)
import random
print(random.randint(1, <sides>))
```

Replace `<sides>` with the number of sides on the die (e.g., 6 for a standard die, 20 for a d20).

## Common Dice Types

| Notation | Sides | Common Use |
|----------|-------|-----------|
| d4 | 4 | Small damage rolls |
| d6 | 6 | Standard die, ability scores |
| d8 | 8 | Weapon damage |
| d10 | 10 | Percentile rolls (paired) |
| d12 | 12 | Greataxe damage |
| d20 | 20 | Attack rolls, skill checks, saving throws |
| d100 | 100 | Percentile rolls |

## Rolling Multiple Dice

For NdX notation (N dice with X sides):

```bash
# Roll 3d6 (three six-sided dice)
for i in {1..3}; do echo $((RANDOM % 6 + 1)); done | paste -sd+ | bc
```

```python
import random

def roll(n, sides, modifier=0):
    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + modifier
    return {"rolls": rolls, "modifier": modifier, "total": total}

# Examples
print(roll(3, 6))        # 3d6
print(roll(1, 20, 5))    # 1d20+5
print(roll(2, 8, -1))    # 2d8-1
```

## Parsing Dice Notation

When the user provides dice notation like "2d6+3", parse it:

```python
import re
import random

def parse_and_roll(notation: str) -> dict:
    match = re.match(r"(\d+)?d(\d+)([+-]\d+)?", notation.strip().lower())
    if not match:
        return {"error": f"Invalid notation: {notation}. Use format: NdX+M (e.g., 2d6+3)"}
    
    n = int(match.group(1) or 1)
    sides = int(match.group(2))
    modifier = int(match.group(3) or 0)
    
    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + modifier
    
    result = f"{notation} → {rolls}"
    if modifier:
        result += f" {'+' if modifier > 0 else ''}{modifier}"
    result += f" = {total}"
    
    return {"notation": notation, "rolls": rolls, "modifier": modifier, "total": total, "display": result}

# Usage
print(parse_and_roll("2d6+3"))
print(parse_and_roll("d20"))
print(parse_and_roll("4d8-2"))
```

## Gotchas

- **Bash `$RANDOM` range**: `$RANDOM` produces 0-32767. For dice this is fine, but for very large ranges use Python's `random.randint()`.
- **Inclusive ranges**: Dice rolls are always 1 to N inclusive. `random.randint(1, N)` is correct; `random.randrange(1, N)` excludes N.
- **Modifier can be negative**: "d20-2" means subtract 2 from the roll. The total can go below 1.
- **Always show individual rolls**: When rolling multiple dice, show each die result plus the total — users want to see the breakdown.

## Validation

After rolling:
1. Each individual die result is within 1 to sides (inclusive)
2. Total equals sum of individual rolls plus modifier
3. Display shows the full breakdown (individual rolls + modifier = total)
