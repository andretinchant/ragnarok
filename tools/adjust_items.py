#!/usr/bin/env python3
"""
Adjust items:
1. EquipLevelMin > 99 -> 99
2. Classes: All_Third/Fourth -> Normal (libera para 2nd classes)
3. Generate report of items with 3rd/4th class skill references

Generates db/import/item_db.yml and itens_retrabalho.txt
"""
import re
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEM_DB = os.path.join(REPO, "db", "re", "item_db_equip.yml")
OUTPUT = os.path.join(REPO, "db", "import", "item_db.yml")
REPORT = os.path.join(REPO, "itens_retrabalho.txt")

# 3rd/4th class skill prefixes (ONLY truly 3rd/4th exclusive)
# Excluded false positives: AC_ (Archer), AM_ (Alchemist), SU_ (Summoner/expanded),
# RL_ (Rebellion/expanded), KO_ (Kagerou-Oboro/expanded), RB_ (Rebellion/expanded),
# SE_ (Star Emperor/expanded)
THIRD_FOURTH_PREFIXES = [
    'RK_', 'NC_', 'AB_', 'SC_', 'GC_', 'RA_', 'WL_', 'SR_', 'SO_',
    'WM_', 'LG_', 'GN_', 'SH_',
    'DK_', 'MT_', 'SX_', 'CD_', 'WH_', 'IG_', 'BO_',
    'EM_', 'IQ_', 'TR_', 'TV_', 'NW_', 'HN_',
]

# Skill prefix -> class mapping for report
SKILL_CLASS_MAP = {
    'RK_': 'Rune Knight -> Knight',
    'NC_': 'Mechanic -> Blacksmith',
    'AB_': 'Arch Bishop -> Priest',
    'SC_': 'Shadow Chaser -> Rogue',
    'GC_': 'Guillotine Cross -> Assassin',
    'RA_': 'Ranger -> Hunter',
    'WL_': 'Warlock -> Wizard',
    'SR_': 'Sura -> Monk',
    'SO_': 'Sorcerer -> Sage',
    'WM_': 'Minstrel/Wanderer -> Bard/Dancer',
    'LG_': 'Royal Guard -> Crusader',
    'GN_': 'Genetic -> Alchemist',
    'SU_': 'Summoner (Expandida)',
    'RL_': 'Rebellion (Expandida)',
    'KO_': 'Kagerou/Oboro (Expandida)',
    'SH_': 'Spirit Handler',
    'RB_': 'Rebellion',
    'SE_': 'Star Emperor',
    'DK_': 'Dragon Knight (4th)',
    'MT_': 'Meister (4th)',
    'SX_': 'Shadow Cross (4th)',
    'AM_': 'Arch Mage (4th)',
    'CD_': 'Cardinal (4th)',
    'WH_': 'Windhawk (4th)',
    'IG_': 'Imperial Guard (4th)',
    'BO_': 'Biolo (4th)',
    'AC_': 'Abyss Chaser (4th)',
    'EM_': 'Elemental Master (4th)',
    'IQ_': 'Inquisitor (4th)',
    'TR_': 'Troubadour (4th)',
    'TV_': 'Trouvere (4th)',
    'NW_': 'Night Watch (4th)',
    'HN_': 'Hyper Novice (4th)',
}

def parse_items(filepath):
    """Parse item entries from item_db_equip.yml using regex."""
    items = []
    current = {}
    in_script = False
    script_lines = []
    in_classes = False
    in_jobs = False

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # New item entry
            m = re.match(r'^\s+-\s+Id:\s+(\d+)', line)
            if m:
                if current:
                    if in_script:
                        current['Script'] = '\n'.join(script_lines)
                    items.append(current)
                current = {'Id': int(m.group(1)), 'Classes': {}, 'Jobs': {}}
                in_script = False
                in_classes = False
                in_jobs = False
                script_lines = []
                continue

            if not current:
                continue

            # Detect sections
            if re.match(r'^\s+Script:\s*\|', line):
                in_script = True
                in_classes = False
                in_jobs = False
                script_lines = []
                continue

            if re.match(r'^\s+Classes:\s*$', line):
                in_classes = True
                in_jobs = False
                in_script = False
                continue

            if re.match(r'^\s+Jobs:\s*$', line):
                in_jobs = True
                in_classes = False
                in_script = False
                continue

            # End of indented section
            if in_script and line.strip() and not line.startswith('      ') and not line.startswith('\t\t'):
                current['Script'] = '\n'.join(script_lines)
                in_script = False

            if in_script:
                script_lines.append(line.rstrip())
                continue

            # Parse class entries
            if in_classes:
                m = re.match(r'^\s+(\w+):\s+(true|false)', line)
                if m:
                    current['Classes'][m.group(1)] = m.group(2) == 'true'
                    continue
                elif line.strip() and not line.startswith('      '):
                    in_classes = False

            # Parse job entries
            if in_jobs:
                m = re.match(r'^\s+(\w+):\s+(true|false)', line)
                if m:
                    current['Jobs'][m.group(1)] = m.group(2) == 'true'
                    continue
                elif line.strip() and not line.startswith('      '):
                    in_jobs = False

            # Simple fields
            m = re.match(r'^\s+AegisName:\s+(\S+)', line)
            if m:
                current['AegisName'] = m.group(1)
                continue

            m = re.match(r'^\s+Name:\s+(.+)', line)
            if m:
                current['Name'] = m.group(1).strip()
                continue

            m = re.match(r'^\s+EquipLevelMin:\s+(\d+)', line)
            if m:
                current['EquipLevelMin'] = int(m.group(1))
                continue

    # Last entry
    if current:
        if in_script:
            current['Script'] = '\n'.join(script_lines)
        items.append(current)

    return items

def has_third_fourth_restriction(item):
    """Check if item is restricted to 3rd/4th classes."""
    classes = item.get('Classes', {})
    return (classes.get('All_Third', False) or
            classes.get('Third', False) or
            classes.get('Third_Upper', False) or
            classes.get('Fourth', False))

def find_skill_references(script):
    """Find 3rd/4th class skill references that REQUIRE the skill to be learned.
    bAutoSpell/bAutoSpellWhenHit work regardless of class, so we skip those.
    We only flag: bSkillAtk, bSkillUseSP, getskilllv (need the skill learned)."""
    if not script:
        return []
    skills = set()
    for line in script.split('\n'):
        line_stripped = line.strip()
        # Skip autocast lines - these work for any class
        if 'bAutoSpell' in line_stripped or 'bAutoSpellWhenHit' in line_stripped:
            continue
        # Only flag lines with bSkillAtk, bSkillUseSP, getskilllv
        if 'bSkillAtk' in line_stripped or 'bSkillUseSP' in line_stripped or 'getskilllv' in line_stripped:
            for prefix in THIRD_FOURTH_PREFIXES:
                matches = re.findall(rf'"({re.escape(prefix)}\w+)"', line_stripped)
                skills.update(matches)
    return sorted(skills)

def generate_import(items):
    """Generate db/import/item_db.yml with overrides."""
    lines = []
    lines.append("# Auto-generated: Item level and class adjustments for Level 99 cap")
    lines.append("# Do not edit manually - regenerate with tools/adjust_items.py")
    lines.append("")
    lines.append("Header:")
    lines.append("  Type: ITEM_DB")
    lines.append("  Version: 3")
    lines.append("")
    lines.append("Body:")

    count_level = 0
    count_class = 0

    for item in items:
        needs_level = item.get('EquipLevelMin', 0) > 99
        needs_class = has_third_fourth_restriction(item)

        if not needs_level and not needs_class:
            continue

        lines.append(f"  - Id: {item['Id']}")
        comment = f"    # {item.get('AegisName', '')} - {item.get('Name', '')}"
        lines.append(comment)

        if needs_level:
            lines.append(f"    EquipLevelMin: 99")
            count_level += 1

        if needs_class:
            lines.append(f"    Classes:")
            lines.append(f"      Normal: true")
            count_class += 1

    return '\n'.join(lines) + '\n', count_level, count_class

def generate_report(items):
    """Generate report of items with 3rd/4th class skill references."""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("RELATÓRIO: Itens com Skills de 3rd/4th Classes")
    report_lines.append("Estes itens precisam de retrabalho manual nos bônus de skill.")
    report_lines.append("As skills referenciadas NÃO existem para classes 2nd.")
    report_lines.append("=" * 80)
    report_lines.append("")

    items_with_skills = []
    for item in items:
        script = item.get('Script', '')
        skills = find_skill_references(script)
        if skills and (has_third_fourth_restriction(item) or item.get('EquipLevelMin', 0) > 99):
            items_with_skills.append((item, skills))

    # Group by class
    by_class = {}
    for item, skills in items_with_skills:
        for skill in skills:
            prefix = skill.split('_')[0] + '_'
            cls = SKILL_CLASS_MAP.get(prefix, f'Unknown ({prefix})')
            if cls not in by_class:
                by_class[cls] = []
            by_class[cls].append((item, skill))

    for cls in sorted(by_class.keys()):
        report_lines.append(f"\n{'='*60}")
        report_lines.append(f"  {cls}")
        report_lines.append(f"{'='*60}")

        # Deduplicate by item ID
        seen = set()
        for item, skill in by_class[cls]:
            if item['Id'] in seen:
                continue
            seen.add(item['Id'])
            all_skills = find_skill_references(item.get('Script', ''))
            cls_skills = [s for s in all_skills if s.startswith(skill.split('_')[0] + '_')]

            report_lines.append(f"\n  ID: {item['Id']}")
            report_lines.append(f"  Nome: {item.get('Name', item.get('AegisName', '?'))}")
            report_lines.append(f"  AegisName: {item.get('AegisName', '?')}")
            report_lines.append(f"  EquipLevelMin: {item.get('EquipLevelMin', '?')}")
            report_lines.append(f"  Jobs: {', '.join(item.get('Jobs', {}).keys())}")
            report_lines.append(f"  Skills 3rd/4th: {', '.join(cls_skills)}")

    report_lines.append(f"\n\n{'='*80}")
    report_lines.append(f"RESUMO: {len(items_with_skills)} itens precisam de retrabalho")
    report_lines.append(f"{'='*80}")

    return '\n'.join(report_lines) + '\n', len(items_with_skills)

if __name__ == '__main__':
    print(f"Parsing {ITEM_DB}...")
    items = parse_items(ITEM_DB)
    print(f"Parsed {len(items)} items total")

    # Generate import file
    output, count_level, count_class = generate_import(items)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Generated {OUTPUT}")
    print(f"  - {count_level} items with EquipLevelMin -> 99")
    print(f"  - {count_class} items with Classes -> Normal")

    # Generate report
    report, count_report = generate_report(items)
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Generated {REPORT}")
    print(f"  - {count_report} items need manual rework (3rd/4th class skills)")
