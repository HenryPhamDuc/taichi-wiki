import subprocess
import os

token = open(r'C:\Users\Henry\Documents\taichi-wiki\github-token.txt', 'rb').read().decode('utf-8').strip()
c = chr(58)
a = chr(64)
s = chr(47)

for repo, dirname in [
    ('taichi-wiki', 'taichi-wiki'),
    ('taichi-wiki-en', 'taichi-wiki-en')
]:
    url = 'https' + c + s + s + 'x-access-token' + c + token + a + 'github.com' + s + 'HenryPhamDuc' + s + repo + '.git'
    os.chdir(r'C:\Users\Henry\Documents\\' + dirname)
    r = subprocess.run(
        ['git', '-c', 'credential.helper=', 'push', url, 'main'],
        capture_output=True,
        timeout=300
    )
    print(f'{repo}: exit={r.returncode}')
    print(f'  err: {r.stderr.decode()[:300]}')