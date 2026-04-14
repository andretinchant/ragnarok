#!/usr/bin/env python3
"""
Update item level descriptions in client's bRO.lua.
Changes all "Nível necessário: ^777777XXX^" where XXX > 99 to 99.
"""
import re
import os

CLIENT_FILE = r"N:\Users\tinch\Games\Ragnarok\PatchBaccon\Patch Baccon\system\bRO.lua"

def update_levels(filepath):
    # Read with latin1 encoding (the file uses cp1252/latin1)
    with open(filepath, 'r', encoding='latin1') as f:
        content = f.read()

    # Pattern: "Nível necessário: ^777777XXX^000000"
    # The é and á are encoded as \xe9 and \xe1 in latin1
    pattern = r'(N\xe9vel necess\xe1rio: \^777777)(\d+)(\^000000)'

    count = 0
    def replacer(match):
        nonlocal count
        level = int(match.group(2))
        if level > 99:
            count += 1
            return f"{match.group(1)}99{match.group(3)}"
        return match.group(0)

    new_content = re.sub(pattern, replacer, content)

    with open(filepath, 'w', encoding='latin1') as f:
        f.write(new_content)

    return count

if __name__ == '__main__':
    print(f"Updating {CLIENT_FILE}...")
    count = update_levels(CLIENT_FILE)
    print(f"Updated {count} item level descriptions to 99")
