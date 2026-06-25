import subprocess
import os

token = open(r'C:\Users\Henry\Documents\taichi-wiki\github-token.txt', 'rb').read().decode('utf-8').strip()
colon = chr(58)
at_sign = chr(64)
slash = chr(47)

for repo in ['taichi-wiki', 'taichi-wiki-en']:
    url = 'https' + colon + slash + slash + 'x-access-token' + colon + token + at_sign + 'github.com' + slash + 'HenryPhamDuc' + slash + repo + '.git'
    repo_dir = 'C:' + slash + 'Users' + slash + 'Henry' + slash + 'Documents' + slash + repo
    os.chdir(repo_dir)
    r = subprocess.run(['git', '-c', 'credential.helper=', 'push', url, 'main'], capture_output=True, timeout=60)
    print(f'{repo}: exit={r.returncode}')
    if r.stdout:
        print(f'  out: {r.stdout.decode()[:200]}')
    if r.stderr:
        print(f'  err: {r.stderr.decode()[:200]}')