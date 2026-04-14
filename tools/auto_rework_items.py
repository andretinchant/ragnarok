#!/usr/bin/env python3
"""
Auto-rework items with 3rd/4th class skill references.
Applies established patterns and generates a report of changes.
"""
import re
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEM_DB = os.path.join(REPO, "db", "re", "item_db_equip.yml")
REPORT = os.path.join(REPO, "itens_alterados.txt")

# === RULES ===

# bSkillAtk: add equivalent 2nd class skill with same value
SKILL_ATK_ADDITIONS = {
    # Arch Bishop -> Priest
    'AB_JUDEX': 'AL_HOLYLIGHT',
    'AB_ADORAMUS': 'AL_HOLYLIGHT',
    # Rune Knight -> Knight
    'RK_SONICWAVE': 'KN_BOWLINGBASH',
    'RK_HUNDREDSPEAR': 'KN_SPEARBOOMERANG',
    'RK_DRAGONBREATH': 'KN_BRANDISHSPEAR',
    'RK_DRAGONBREATH_WATER': 'KN_BRANDISHSPEAR',
    'RK_IGNITIONBREAK': 'KN_BOWLINGBASH',
    'RK_STORMBLAST': 'KN_BOWLINGBASH',
    'RK_PHANTOMTHRUST': 'KN_PIERCE',
    # Warlock -> Wizard
    'WL_CRIMSONROCK': 'WZ_METEOR',
    'WL_HELLINFERNO': 'WZ_VERMILION',
    'WL_JACKFROST': 'WZ_STORMGUST',
    'WL_CHAINLIGHTNING': 'WZ_VERMILION',
    'WL_EARTHSTRAIN': 'WZ_HEAVENDRIVE',
    'WL_COMET': 'WZ_METEOR',
    'WL_SOULEXPANSION': 'WZ_NAPALMVULCAN',
    'WL_DRAINLIFE': 'WZ_NAPALMVULCAN',
    # Ranger -> Hunter
    'RA_ARROWSTORM': 'HT_BLITZBEAT',
    'RA_AIMEDBOLT': 'HT_BLITZBEAT',
    'RA_WUGSTRIKE': 'HT_BLITZBEAT',
    'RA_WUGBITE': 'HT_BLITZBEAT',
    # Guillotine Cross -> Assassin
    'GC_ROLLINGCUTTER': 'AS_SONICBLOW',
    'GC_CROSSIMPACT': 'AS_SONICBLOW',
    'GC_CROSSRIPPERSLASHER': 'AS_SONICBLOW',
    'GC_COUNTERSLASH': 'AS_SONICBLOW',
    'GC_DARKILLUSION': 'AS_GRIMTOOTH',
    'GC_PHANTOMMENACE': 'AS_GRIMTOOTH',
    # Royal Guard -> Crusader
    'LG_BANISHINGPOINT': 'CR_HOLYCROSS',
    'LG_CANNONSPEAR': 'CR_HOLYCROSS',
    'LG_RAYOFGENESIS': 'CR_GRANDCROSS',
    'LG_SHIELDPRESS': 'CR_SHIELDCHARGE',
    'LG_OVERBRAND': 'CR_HOLYCROSS',
    'LG_MOONSLASHER': 'CR_HOLYCROSS',
    'LG_EARTHDRIVE': 'CR_SHIELDCHARGE',
    'LG_HESPERUSLIT': 'CR_HOLYCROSS',
    # Sura -> Monk
    'SR_DRAGONCOMBO': 'MO_CHAINCOMBO',
    'SR_SKYNETBLOW': 'MO_INVESTIGATE',
    'SR_EARTHSHAKER': 'MO_INVESTIGATE',
    'SR_FALLENEMPIRE': 'MO_FINGEROFFENSIVE',
    'SR_TIGERCANNON': 'MO_FINGEROFFENSIVE',
    'SR_RAMPAGEBLASTER': 'MO_FINGEROFFENSIVE',
    'SR_KNUCKLEARROW': 'MO_INVESTIGATE',
    'SR_WINDMILL': 'MO_CHAINCOMBO',
    'SR_RIDEINLIGHTNING': 'MO_INVESTIGATE',
    'SR_FLASHCOMBO': 'MO_COMBOFINISH',
    'SR_CRESCENTELBOW': 'MO_COMBOFINISH',
    'SR_GATEOFHELL': 'MO_EXTREMITYFIST',
    # Sorcerer -> Sage
    'SO_PSYCHIC_WAVE': 'SA_AUTOSPELL',
    'SO_VARETYR_SPEAR': 'SA_FLAMELAUNCHER',
    'SO_DIAMONDDUST': 'SA_FROSTWEAPON',
    'SO_POISON_BUSTER': 'SA_DELUGE',
    'SO_CLOUD_KILL': 'SA_VIOLENTGALE',
    'SO_EARTHGRAVE': 'SA_LANDPROTECTOR',
    # Minstrel/Wanderer -> Bard/Dancer
    'WM_METALICSOUND': 'CG_ARROWVULCAN',
    'WM_REVERBERATION': 'CG_ARROWVULCAN',
    'WM_SEVERE_RAINSTORM_MELEE': 'CG_ARROWVULCAN',
    'WM_GREAT_ECHO': 'CG_ARROWVULCAN',
    # Genetic -> Alchemist
    'GN_CARTCANNON': 'MC_CARTREVOLUTION',
    'GN_CART_TORNADO': 'MC_CARTREVOLUTION',
    'GN_CRAZYWEED': 'MC_CARTREVOLUTION',
    'GN_SPORE_EXPLOSION': 'MC_CARTREVOLUTION',
    'GN_FIRE_EXPANSION': 'MC_CARTREVOLUTION',
    'GN_HELLS_PLANT_ATK': 'MC_CARTREVOLUTION',
    # Shadow Chaser -> Rogue
    'SC_FATALMENACE': 'RG_BACKSTAP',
    'SC_TRIANGLESHOT': 'RG_BACKSTAP',
    'SC_FEINTBOMB': 'RG_BACKSTAP',
    # Mechanic -> Blacksmith
    'NC_AXEBOOMERANG': 'BS_HAMMERFALL',
    'NC_POWERSWING': 'BS_HAMMERFALL',
    'NC_AXETORNADO': 'BS_HAMMERFALL',
    'NC_ARMSCANNON': 'BS_HAMMERFALL',
    'NC_PILEBUNKER': 'BS_HAMMERFALL',
    'NC_VULCANARM': 'BS_HAMMERFALL',
    # 4th class skills -> same as their 3rd parent mapping
    'DK_SERVANTWEAPON': 'KN_BOWLINGBASH',
    'DK_SERVANT_W_SIGN': 'KN_BOWLINGBASH',
    'DK_HACKANDSLASHER': 'KN_BOWLINGBASH',
    'DK_MADNESS_CRUSHER': 'KN_BOWLINGBASH',
    'IG_OVERSLASH': 'CR_HOLYCROSS',
    'IG_CROSS_RAIN': 'CR_GRANDCROSS',
    'IG_SHIELD_SHOOTING': 'CR_SHIELDCHARGE',
    'CD_PETITIO': 'AL_HOLYLIGHT',
    'CD_ARBITRIUM': 'AL_HOLYLIGHT',
    'CD_FRAMEN': 'AL_HOLYLIGHT',
    'MT_AXE_STOMP': 'BS_HAMMERFALL',
    'MT_RUSH_QUAKE': 'BS_HAMMERFALL',
    'SX_CHAINRUSH': 'AS_SONICBLOW',
    'SX_SHADOWSTAB': 'AS_GRIMTOOTH',
    'WH_CRESCIVE_BOLT': 'HT_BLITZBEAT',
    'WH_GALESTORM': 'HT_BLITZBEAT',
    'BO_ACIDIFIED_ZONE_WIND': 'MC_CARTREVOLUTION',
    'BO_ACIDIFIED_ZONE_GROUND': 'MC_CARTREVOLUTION',
    'BO_ACIDIFIED_ZONE_WATER': 'MC_CARTREVOLUTION',
    'BO_ACIDIFIED_ZONE_FIRE': 'MC_CARTREVOLUTION',
    'TR_ROSEBLOSSOM': 'CG_ARROWVULCAN',
    'TR_ROSEBLOSSOM_ATK': 'CG_ARROWVULCAN',
    'TR_METALIC_FURY': 'CG_ARROWVULCAN',
    'TV_ENSEMBLE_FATIGUE': 'CG_ARROWVULCAN',
    'IQ_FIRST_BRAND': 'MO_INVESTIGATE',
    'IQ_SECOND_FAITH': 'MO_INVESTIGATE',
    'IQ_THIRD_EXOR_FLAME': 'MO_INVESTIGATE',
    'IQ_OLEUM_SANCTUM': 'MO_INVESTIGATE',
    'IQ_MASSIVE_F_BLASTER': 'MO_FINGEROFFENSIVE',
    'EM_ELEMENTAL_BUSTER': 'SA_AUTOSPELL',
    'EM_DIAMOND_STORM': 'SA_FROSTWEAPON',
    'NW_SPIRAL_SHOOTING': 'HT_BLITZBEAT',
    'NW_MAGAZINE_FOR_ONE': 'HT_BLITZBEAT',
    'NW_THE_VIGILANTE_AT_NIGHT': 'HT_BLITZBEAT',
    'NW_ONLY_ONE_BULLET': 'HT_BLITZBEAT',
    'HN_METEOR_STORM_BUSTER': 'WZ_METEOR',
    'HN_GROUND_GRAVITATION': 'WZ_HEAVENDRIVE',
    'HN_NAPALM_VULCAN_STRIKE': 'WZ_NAPALMVULCAN',
}

# Skills that should be kept as-is (work via equip grant or are fine)
KEEP_AS_IS_SKILLS = {
    'AB_DUPLELIGHT_MELEE', 'AB_DUPLELIGHT_MAGIC', 'AB_DUPLELIGHT',
}

# getskilllv replacements: AB_ skills -> refinement
# Format: pattern -> replacement
GETSKILLLV_REPLACE = {
    # These get replaced with .@r (refinement)
    'AB_SECRAMENT', 'AB_CANTO', 'AB_PRAEFATIO', 'AB_HIGHNESSHEAL',
    'AB_LAUDAAGNUS', 'AB_LAUDARAMUS', 'AB_ORATIO', 'AB_CLEARANCE',
    'AB_JUDEX', 'AB_ADORAMUS', 'AB_CLEMENTIA', 'AB_EPICLESIS',
    'RK_ENCHANTBLADE', 'RK_RUNEMASTERY',
    'NC_MADOLICENCE', 'NC_RESEARCHFE',
    'WL_RADIUS',
    'RA_RESEARCHTRAP',
    'GC_RESEARCHNEWPOISON',
    'LG_REFLECTDAMAGE', 'LG_PIETY',
    'SR_ASSIMILATEPOWER', 'SR_POWERVELOCITY',
    'SO_SPELLFIST',
    'WM_LESSON', 'WM_VOICEOFSIREN',
    'GN_REMODELING_CART', 'GN_CHANGEMATERIAL',
    'SC_REPRODUCE', 'SC_SHADOWFORM',
}


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # === Rule 1: Add equivalent 2nd class skill for bSkillAtk ===
    for skill_3rd, skill_2nd in SKILL_ATK_ADDITIONS.items():
        if skill_3rd in KEEP_AS_IS_SKILLS:
            continue
        # Find bSkillAtk lines with this skill
        pattern = rf'(bonus2 bSkillAtk,"{re.escape(skill_3rd)}",)([^;]+;)'
        matches = list(re.finditer(pattern, content))
        if matches:
            # Process in reverse to not mess up positions
            for m in reversed(matches):
                original_line = m.group(0)
                value = m.group(2)
                # Check if the equivalent line already exists nearby
                context_start = max(0, m.start() - 200)
                context_end = min(len(content), m.end() + 200)
                context = content[context_start:context_end]
                new_line = f'bonus2 bSkillAtk,"{skill_2nd}",{value}'
                if new_line not in context and f'"{skill_2nd}"' not in context[context.find(original_line):]:
                    # Find the indentation
                    line_start = content.rfind('\n', 0, m.start()) + 1
                    indent = ''
                    for ch in content[line_start:m.start()]:
                        if ch in ' \t':
                            indent += ch
                        else:
                            break
                    insertion = f'\n{indent}{new_line}'
                    content = content[:m.end()] + insertion + content[m.end():]
                    changes.append(f"[ADD] Item near line {content[:m.start()].count(chr(10))+1}: Added {skill_2nd} alongside {skill_3rd}")

    # === Rule 2: Replace getskilllv("AB_*") with .@r ===
    for skill in GETSKILLLV_REPLACE:
        pattern = rf'getskilllv\("{re.escape(skill)}"\)'
        if re.search(pattern, content):
            # Don't replace inside bAutoSpell lines
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if re.search(pattern, line) and 'bAutoSpell' not in line:
                    old_line = line
                    line = re.sub(pattern, '.@r', line)
                    if old_line != line:
                        changes.append(f"[REPLACE] getskilllv(\"{skill}\") -> .@r")
                new_lines.append(line)
            content = '\n'.join(new_lines)

    # === Rule 3: Replace getskilllv("AB_*") conditions like == 10 or >= 5 with refine checks ===
    # Already handled by Rule 2 since we replace getskilllv with .@r

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Deduplicate changes
    unique_changes = list(dict.fromkeys(changes))
    return unique_changes


def generate_report(changes):
    lines = []
    lines.append("=" * 80)
    lines.append("RELATÓRIO: Alterações Automáticas em Itens")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Total de alterações: {len(changes)}")
    lines.append("")

    add_count = sum(1 for c in changes if c.startswith('[ADD]'))
    replace_count = sum(1 for c in changes if c.startswith('[REPLACE]'))

    lines.append(f"  - Skills 2nd adicionadas (bSkillAtk): {add_count}")
    lines.append(f"  - getskilllv substituídos por refinamento: {replace_count}")
    lines.append("")
    lines.append("-" * 80)

    for change in changes:
        lines.append(f"  {change}")

    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    print(f"Processing {ITEM_DB}...")
    changes = process_file(ITEM_DB)
    print(f"Applied {len(changes)} changes")

    report = generate_report(changes)
    with open(REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Report saved to {REPORT}")
