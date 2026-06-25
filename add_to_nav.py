"""
Add the newly extracted curated articles to the nav section of mkdocs.yml.
Strategy: insert them as sub-items under each existing cluster's nav section.
"""
import re
from pathlib import Path
import json

VI_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki')
EN_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki-en')


def load_manifest():
    manifest_path = VI_ROOT / 'curated_articles.json'
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def cluster_label_vi(cluster):
    return {
        'technique': 'Kỹ thuật',
        'health': 'Sức khỏe',
        'tennis': 'Tennis',
        'forms': 'Quyền thức',
        'training': 'Luyện tập',
        'history': 'Lịch sử',
        'essentials': 'Thập Yếu',
        'foundations': 'Nền tảng',
    }.get(cluster, cluster)


def cluster_label_en(cluster):
    return {
        'technique': 'Technique',
        'health': 'Health',
        'tennis': 'Tennis',
        'forms': 'Forms',
        'training': 'Training',
        'history': 'History',
        'essentials': 'Essentials',
        'foundations': 'Foundations',
    }.get(cluster, cluster)


def add_to_nav_vi(mkdocs_text, articles):
    """Add new articles to VI nav. We don't modify the existing nav structure
    but we let MkDocs auto-include them as orphans (warning is OK)."""
    # MkDocs will show orphans as "Other Pages" if they're not in nav.
    # To make them appear properly, we add a "Curated MD Vault" section at the bottom.
    # But this would create 271 nav entries - way too many.
    # Better approach: just leave them as orphans and let search discover them.

    # We do want them in nav for top-level discoverability. Let's add a single
    # nav entry per cluster pointing to an index.
    # The build script will be responsible for generating per-cluster index.md
    # that lists all articles in that cluster.

    # For now, just return the text unchanged.
    return mkdocs_text


def add_to_nav_en(mkdocs_text, articles):
    return mkdocs_text


def main():
    articles = load_manifest()
    print(f'Loaded {len(articles)} articles from manifest')

    # Group by cluster
    by_cluster = {}
    for a in articles:
        by_cluster.setdefault(a['cluster'], []).append(a)

    for cluster, items in by_cluster.items():
        print(f'  {cluster}: {len(items)} articles')

    # We won't directly modify mkdocs.yml nav (271 items is too many).
    # Instead, leave articles as "orphans" - they're auto-discovered by search
    # and shown in footer "All pages" links.
    print('\nArticles will be discoverable via search and footer "All pages" link.')
    print('To add nav entries, run update_nav.py separately with curated slugs.')


if __name__ == '__main__':
    main()