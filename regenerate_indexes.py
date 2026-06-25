"""
Regenerate the cluster index.md pages to include all articles in each cluster.
This makes the new articles discoverable from the navigation.
"""
from pathlib import Path
import re

VI_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki\docs')
EN_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki-en\docs')

VI_CLUSTER_LABELS = {
    'technique': ('💪 Kỹ thuật & Kình lực', 'Kỹ thuật'),
    'health': ('🌿 Sức khỏe & Trường thọ', 'Sức khỏe'),
    'tennis': ('🎾 Ứng dụng Tennis', 'Tennis'),
    'forms': ('🌊 Quyền thức & Ứng dụng', 'Quyền thức'),
    'training': ('🧘 Luyện tập & Bài tập', 'Luyện tập'),
    'history': ('📜 Lịch sử & Triết lý', 'Lịch sử'),
    'essentials': ('🎯 Thập Yếu & Nguyên lý', 'Thập Yếu'),
    'foundations': ('🌱 Nền tảng', 'Nền tảng'),
}

EN_CLUSTER_LABELS = {
    'technique': ('💪 Technique & Power', 'Technique'),
    'health': ('🌿 Health & Longevity', 'Health'),
    'tennis': ('🎾 Tennis Applications', 'Tennis'),
    'forms': ('🌊 Forms & Applications', 'Forms'),
    'training': ('🧘 Training & Drills', 'Training'),
    'history': ('📜 History & Philosophy', 'History'),
    'essentials': ('🎯 Ten Essentials', 'Essentials'),
    'foundations': ('🌱 Foundations', 'Foundations'),
}


def extract_title(md_path):
    for line in md_path.read_text(encoding='utf-8').split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return md_path.stem


def build_index_vi(cluster_dir, title_emoji, label):
    articles = []
    for md in sorted(cluster_dir.glob('*.md')):
        if md.name == 'index.md':
            continue
        title = extract_title(md)
        slug = md.stem
        articles.append((title, slug))
    if not articles:
        return None
    body = f"# {title_emoji}\n\nPhần này có **{len(articles)} bài viết** về {label}.\n\n"
    for title, slug in articles:
        body += f"- [{title}]({slug}.md)\n"
    body += "\n[← Về trang chủ](../index.md)\n"
    return body


def build_index_en(cluster_dir, title_emoji, label):
    articles = []
    for md in sorted(cluster_dir.glob('*.md')):
        if md.name == 'index.md':
            continue
        title = extract_title(md)
        slug = md.stem
        articles.append((title, slug))
    if not articles:
        return None
    body = f"# {title_emoji}\n\nThis section contains **{len(articles)} articles** on {label}.\n\n"
    for title, slug in articles:
        body += f"- [{title}]({slug}.md)\n"
    body += "\n[← Back to homepage](../index.md)\n"
    return body


def main():
    # VI
    print('=== VI Wiki ===')
    for cluster, (title, label) in VI_CLUSTER_LABELS.items():
        cluster_dir = VI_ROOT / cluster
        if not cluster_dir.exists():
            continue
        body = build_index_vi(cluster_dir, title, label)
        if body:
            (cluster_dir / 'index.md').write_text(body, encoding='utf-8')
            print(f'  {cluster}: regenerated index')

    # EN
    print('=== EN Wiki ===')
    for cluster, (title, label) in EN_CLUSTER_LABELS.items():
        cluster_dir = EN_ROOT / cluster
        if not cluster_dir.exists():
            continue
        body = build_index_en(cluster_dir, title, label)
        if body:
            (cluster_dir / 'index.md').write_text(body, encoding='utf-8')
            print(f'  {cluster}: regenerated index')


if __name__ == '__main__':
    main()