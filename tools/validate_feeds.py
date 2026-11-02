import json
from pathlib import Path
from urllib.parse import urlsplit
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'sources.json').read_text(encoding='utf-8'))
assert catalog['schema_version']==1 and isinstance(catalog['config_version'],int) and catalog['config_version']>0
assert 0<len(catalog['sources'])<=128
ids=set()
for source in catalog['sources']:
    assert source['id'] not in ids
    ids.add(source['id'])
    p=urlsplit(source['url'])
    assert p.scheme=='https' and p.hostname and not p.username and not p.password
for path in sorted((root/'feeds').glob('*.json')):
    if path.name.endswith('.health.json'):continue
    assert path.stat().st_size<=2*1024*1024
    doc=json.loads(path.read_text(encoding='utf-8'))
    assert doc['schema_version']==1 and doc['status']=='ok' and isinstance(doc['items'],list)
    for item in doc['items']:
        assert item['title'] and item['original_url'].startswith('https://')
        assert not item.get('content') and not item.get('image_url')
print('Catalog and public metadata JSON verified')
