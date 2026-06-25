"""
Extract articles from 4 curated vault MDs into VI/EN wiki docs/.
Each H2/H3 becomes one article. Skip sections that look like navigation.
"""
import os
import re
import json
from pathlib import Path

VAULT = Path(r'C:\Users\Henry\Documents\MY VAULT\Documents\Tai Chi Books')
VI_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki\docs')
EN_ROOT = Path(r'C:\Users\Henry\Documents\taichi-wiki-en\docs')

DIACRITICS = {
    'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'đ': 'd', 'Đ': 'd',
}


def slugify(text):
    text = text.lower().strip()
    # Strip leading ** and chapter numbers like "1.1." or "Chương 17:"
    text = re.sub(r'^\*+|\*+$', '', text).strip()
    text = re.sub(r'^\d+\.\d+\.?\s*', '', text)
    text = re.sub(r'^chương\s+\d+[.:]?\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^phần\s+[ivx]+[.:]?\s*', '', text, flags=re.IGNORECASE)
    out = []
    for ch in text:
        if ch in DIACRITICS:
            out.append(DIACRITICS[ch])
        elif ch.isalnum():
            out.append(ch)
        elif ch in ' -_':
            out.append('-')
    slug = ''.join(out)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-')[:80]


def clean_title(text):
    """Clean markdown bold/chapter prefixes from title."""
    text = re.sub(r'^\*+|\*+$', '', text).strip()
    return text


def split_md(content):
    """Split markdown by H2/H3. Returns list of (title, body)."""
    lines = content.split('\n')
    sections = []
    current_title = None
    current_body = []
    pre_lines = []

    for line in lines:
        if re.match(r'^##\s+', line) and not re.match(r'^###\s+', line):
            if current_title:
                sections.append((current_title, current_body))
            current_title = re.sub(r'^##\s+', '', line).strip()
            current_body = []
        elif re.match(r'^###\s+', line):
            if current_title:
                sections.append((current_title, current_body))
            current_title = re.sub(r'^###\s+', '', line).strip()
            current_body = []
        else:
            if current_title is not None:
                current_body.append(line)
            else:
                pre_lines.append(line)

    if current_title:
        sections.append((current_title, current_body))

    return sections


# Filter patterns: skip these section types
SKIP_PATTERNS = [
    r'^lời\s+giới\s+thiệu',
    r'^mục\s+lục',
    r'^lời\s+cuối',
    r'^tài\s+liệu\s+tham\s+khảo',
    r'^giới\s+thiệu$',
    r'^lời\s+mở',
    r'^phụ\s+lục',
    r'^mở\s+đầu',
    r'^kết\s+luận',
    r'^lời\s+cảm\s+ơn',
    r'^lời\s+tựa',
    r'^\*\*lời\s',
]

def should_skip(title):
    t = title.lower().strip()
    for pat in SKIP_PATTERNS:
        if re.search(pat, t):
            return True
    # Also skip empty/very short
    if len(t) < 4:
        return True
    return False


def make_vi_article(title, body, cluster, source_label):
    """Build a VI markdown article."""
    clean = clean_title(title)
    body_text = '\n'.join(body).strip()
    return f"""# {clean}

> *Source: {source_label}*

{body_text}
"""


def make_en_article(title, body, cluster, source_label):
    """Build an EN markdown article. We keep title as-is (Vietnamese title acts as reference)
    and add a notice that this is the Vietnamese source for now.
    EN versions need translation later - for now, mirror VI content with English notice."""
    clean = clean_title(title)
    body_text = '\n'.join(body).strip()
    return f"""# {clean}

> *Source: {source_label}*
> *Note: This article currently mirrors the Vietnamese source. A translated English version will be added later.*

{body_text}
"""


def main():
    sources = [
        ('HƯỚNG DẪN KỸ THUẬT THÁI CỰC QUYỀN.md', 'technique', 'Hướng dẫn kỹ thuật Thái Cực Quyền'),
        ('THÁI CỰC QUYỀN - NGHỆ THUẬT SỐNG KHỎE - PHẦN III VÀ TIẾP THEO.md', 'health', 'Nghệ thuật sống khỏe (Phần III)'),
        ('Taichi và tennis - Phòng thí nghiệm ứng dụng Taichi trong tennis.md', 'tennis', 'Taichi & Tennis Lab'),
        ('Taichi và cuộc sống - Cẩm nang giữ gìn sức khỏe và kéo dài tuổi thọ.md', 'health', 'Cẩm nang giữ gìn sức khỏe và kéo dài tuổi thọ'),
    ]

    # Map of existing slugs to avoid collisions
    used_slugs = {}  # cluster -> set of slugs
    new_articles = []  # (cluster, slug, title, source_label)

    for fname, cluster, source_label in sources:
        path = VAULT / fname
        if not path.exists():
            print(f'NOT FOUND: {path}')
            continue

        content = path.read_text(encoding='utf-8')
        sections = split_md(content)

        # Track used slugs per cluster
        if cluster not in used_slugs:
            used_slugs[cluster] = set()

        # Skip parent overview sections (only keep H3 leaf sections)
        leaf_sections = []
        for title, body in sections:
            if should_skip(title):
                continue
            # Only keep sections with enough content
            content_len = len(''.join(body).strip())
            if content_len < 200:
                continue
            leaf_sections.append((title, body))

        print(f'\n=== {source_label} ({cluster}) ===')
        print(f'   {len(leaf_sections)} usable sections (after filtering)')

        for title, body in leaf_sections:
            slug = slugify(title)
            # Ensure slug uniqueness
            base = slug
            n = 2
            while slug in used_slugs[cluster]:
                slug = f'{base}-{n}'
                n += 1
            used_slugs[cluster].add(slug)

            clean = clean_title(title)
            # Write VI version
            vi_article = make_vi_article(clean, body, cluster, source_label)
            vi_path = VI_ROOT / cluster / f'{slug}.md'
            vi_path.write_text(vi_article, encoding='utf-8')

            # Write EN version (mirror with note)
            en_article = make_en_article(clean, body, cluster, source_label)
            en_path = EN_ROOT / cluster / f'{slug}.md'
            en_path.write_text(en_article, encoding='utf-8')

            new_articles.append((cluster, slug, clean, source_label))

    print(f'\n=== Total new articles ===')
    print(f'  {len(new_articles)} articles written to both VI and EN wikis')
    for cluster in ['technique', 'health', 'tennis']:
        count = sum(1 for a in new_articles if a[0] == cluster)
        if count > 0:
            print(f'  {cluster}: {count}')

    # Save a manifest for later use (rebuilds, navigations, etc.)
    manifest_path = Path(r'C:\Users\Henry\Documents\taichi-wiki\curated_articles.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump([{'cluster': a[0], 'slug': a[1], 'title': a[2], 'source': a[3]}
                   for a in new_articles], f, ensure_ascii=False, indent=2)
    print(f'\nManifest saved: {manifest_path}')


if __name__ == '__main__':
    main()