#!/usr/bin/env python3
"""
Rescale monsters with Level > 99 to fit within 80-99 range.
Generates db/import/mob_db.yml with partial overrides.
"""
import re
import math
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOB_DB = os.path.join(REPO, "db", "re", "mob_db.yml")
OUTPUT = os.path.join(REPO, "db", "import", "mob_db.yml")

MAX_ORIGINAL = 265
MIN_NEW = 80
MAX_NEW = 99

def new_level(original):
    if original <= 100:
        return MIN_NEW
    if original >= MAX_ORIGINAL:
        return MAX_NEW
    return MIN_NEW + int(math.floor((MAX_NEW - MIN_NEW) * (original - 100) / (MAX_ORIGINAL - 100)))

def scale_stat(value, ratio, power=1.0):
    if value is None or value == 0:
        return 0
    return max(1, int(round(value * (ratio ** power))))

def parse_mobs(filepath):
    """Parse mob entries using regex - much faster than YAML parser for 120K lines."""
    mobs = []
    current = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # New mob entry
            m = re.match(r'^\s+-\s+Id:\s+(\d+)', line)
            if m:
                if current and current.get('Level', 0) > 99:
                    mobs.append(current)
                current = {'Id': int(m.group(1))}
                continue

            if not current:
                continue

            # Parse fields we care about
            for field in ['Level', 'Hp', 'Sp', 'BaseExp', 'JobExp', 'MvpExp',
                         'Attack', 'Attack2', 'Defense', 'MagicDefense',
                         'Str', 'Agi', 'Vit', 'Int', 'Dex', 'Luk']:
                m = re.match(rf'^\s+{field}:\s+(\d+)', line)
                if m:
                    current[field] = int(m.group(1))
                    break

            # Parse AegisName for reference
            m = re.match(r'^\s+AegisName:\s+(\S+)', line)
            if m:
                current['AegisName'] = m.group(1)

    # Don't forget last entry
    if current and current.get('Level', 0) > 99:
        mobs.append(current)

    return mobs

def generate_import(mobs):
    lines = []
    lines.append("# Auto-generated: Monster level rescaling (100-265 -> 80-99)")
    lines.append("# Do not edit manually - regenerate with tools/rescale_mobs.py")
    lines.append("")
    lines.append("Header:")
    lines.append("  Type: MOB_DB")
    lines.append("  Version: 5")
    lines.append("")
    lines.append("Body:")

    for mob in mobs:
        old_level = mob['Level']
        nl = new_level(old_level)
        ratio = nl / old_level

        lines.append(f"  - Id: {mob['Id']}")
        lines.append(f"    # Original: Lv{old_level} {mob.get('AegisName', '')}")
        lines.append(f"    Level: {nl}")

        if 'Hp' in mob and mob['Hp'] > 0:
            lines.append(f"    Hp: {scale_stat(mob['Hp'], ratio, 2.0)}")

        if 'BaseExp' in mob and mob['BaseExp'] > 0:
            lines.append(f"    BaseExp: {scale_stat(mob['BaseExp'], ratio, 1.5)}")

        if 'JobExp' in mob and mob['JobExp'] > 0:
            lines.append(f"    JobExp: {scale_stat(mob['JobExp'], ratio, 1.5)}")

        if 'MvpExp' in mob and mob['MvpExp'] > 0:
            lines.append(f"    MvpExp: {scale_stat(mob['MvpExp'], ratio, 1.5)}")

        if 'Attack' in mob and mob['Attack'] > 0:
            lines.append(f"    Attack: {scale_stat(mob['Attack'], ratio, 1.5)}")

        if 'Attack2' in mob and mob['Attack2'] > 0:
            lines.append(f"    Attack2: {scale_stat(mob['Attack2'], ratio, 1.5)}")

        if 'Defense' in mob and mob['Defense'] > 0:
            lines.append(f"    Defense: {scale_stat(mob['Defense'], ratio)}")

        if 'MagicDefense' in mob and mob['MagicDefense'] > 0:
            lines.append(f"    MagicDefense: {scale_stat(mob['MagicDefense'], ratio)}")

        for stat in ['Str', 'Agi', 'Vit', 'Int', 'Dex', 'Luk']:
            if stat in mob and mob[stat] > 0:
                lines.append(f"    {stat}: {scale_stat(mob[stat], ratio)}")

    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    print(f"Parsing {MOB_DB}...")
    mobs = parse_mobs(MOB_DB)
    print(f"Found {len(mobs)} monsters with Level > 99")

    output = generate_import(mobs)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Generated {OUTPUT}")
    print(f"Level range: {min(new_level(m['Level']) for m in mobs)} - {max(new_level(m['Level']) for m in mobs)}")
