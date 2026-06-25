"""
Rebuild graph-data.json to include the new curated articles.
The graph already lists nodes by ID - we just need to add nodes for the new
articles (with cluster and a basic description).
"""
import json
from pathlib import Path
import re

VI_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki')
EN_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki-en')


def extract_title(content):
    """Extract first H1 from markdown."""
    for line in content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return 'Untitled'


def main():
    for root in [VI_ROOT, EN_ROOT]:
        graph_path = root / 'docs' / 'assets' / 'graph-data.json'
        with open(graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        existing_ids = {n['id'] for n in data.get('nodes', [])}
        added = 0

        # Scan all docs/ for new articles
        for md_file in (root / 'docs').rglob('*.md'):
            rel = md_file.relative_to(root / 'docs')
            parts = rel.parts
            if parts[-1] == 'index.md':
                continue
            cluster = parts[0] if len(parts) > 1 else 'foundations'
            slug = str(rel.with_suffix('')).replace('\\', '/')
            if slug in existing_ids:
                continue

            content = md_file.read_text(encoding='utf-8')
            title = extract_title(content)
            # Skip the '> *Source:*' line for description
            desc_lines = []
            in_source = False
            for line in content.split('\n'):
                if line.startswith('> *Source:'):
                    in_source = True
                    continue
                if in_source and line.startswith('>'):
                    in_source = False
                    continue
                if in_source:
                    continue
                if line.startswith('# '):
                    continue
                if line.strip():
                    desc_lines.append(line.strip())
                    if len('\n'.join(desc_lines)) > 250:
                        break

            description = ' '.join(desc_lines)[:250]

            node = {
                'id': slug,
                'name': title,
                'cluster': cluster,
                'url': slug + '/',
                'description': description,
            }
            data['nodes'].append(node)
            added += 1

        # Update topIds to include all nodes (now sorted by ID for determinism)
        data['topIds'] = sorted([n['id'] for n in data['nodes']])

        with open(graph_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f'{root.name}: added {added} nodes, total {len(data["nodes"])}')


if __name__ == '__main__':
    main()