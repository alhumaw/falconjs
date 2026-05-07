#!/usr/bin/env python3

import glob, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

apis = sorted(
    os.path.splitext(os.path.basename(f))[0]
    for f in glob.glob(os.path.join(root, 'src', 'apis', '*Api.ts'))
)

def member_name(api):
    return api[0].lower() + api.removesuffix('Api')[1:]

sections = {
    'imports':     "\n".join(f"    {a}," for a in apis),
    'properties':  "\n".join(f"    {member_name(a)}: {a};" for a in apis),
    'assignments': "\n".join(f"        this.{member_name(a)} = new {a}(this.config);" for a in apis),
}

client_path = os.path.join(root, 'src', 'client.ts')
lines = open(client_path).read().splitlines(keepends=True)

output = []
skip = False
for line in lines:
    tag = line.strip()
    if tag == '// @generated:end':
        skip = False
        output.append(line)
        continue
    if skip:
        continue
    output.append(line)
    for key, content in sections.items():
        if tag == f'// @generated:{key}':
            skip = True
            output.append(content + '\n')

open(client_path, 'w').write(''.join(output))
