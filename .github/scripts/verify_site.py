"""Verify the approved static PWA bytes before publishing; stdlib only."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json


def verify(site, approval):
    site = Path(site)
    if approval['schema'] != 1:
        raise ValueError('Unsupported release approval')
    for name, key in [('pwa-assets.json', 'assetsSha256'), ('sw.js', 'workerSha256')]:
        if hashlib.sha256((site / name).read_bytes()).hexdigest() != approval[key]:
            raise ValueError(f'Approved file mismatch: {name}')
    spec = json.loads((site / 'pwa-assets.json').read_text(encoding='utf-8'))
    if spec['release'] != approval['release'] or len(spec['audio']) != approval['audioFiles']:
        raise ValueError('Release identity or audio coverage mismatch')
    expected = {'pwa-assets.json', 'sw.js', '.nojekyll'}
    for asset in spec['shell'] + spec['audio']:
        rel = asset['path']
        path = PurePosixPath(rel)
        if path.is_absolute() or '..' in path.parts or path.as_posix() != rel or '\\' in rel or ':' in rel or rel in expected:
            raise ValueError(f'Invalid or duplicate asset path: {rel}')
        expected.add(rel)
        data = (site / rel).read_bytes()
        if len(data) != asset['bytes'] or hashlib.sha256(data).hexdigest() != asset['sha256']:
            raise ValueError(f'Asset bytes mismatch: {rel}')
    actual = set()
    for path in site.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlink not allowed: {path.relative_to(site)}')
        if path.is_file():
            actual.add(path.relative_to(site).as_posix())
    if actual != expected or len(actual) != approval['files']:
        raise ValueError('Website file whitelist mismatch')
    if (site / '.nojekyll').read_bytes() != b'':
        raise ValueError('.nojekyll must remain empty')
    return {'status': 'PASS_SITE_ARTIFACT', 'release': spec['release'],
            'files': len(actual), 'audioFiles': len(spec['audio']),
            'htmlSha256': hashlib.sha256((site / 'index.html').read_bytes()).hexdigest()}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=root / 'pwa-site')
    parser.add_argument('--approval', type=Path, default=root / '.github/pwa-release.json')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.site, json.loads(args.approval.read_text(encoding='utf-8')))))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'PUBLISH BLOCKED: {error}\n')
