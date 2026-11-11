import json
from pathlib import Path
from urllib.parse import urlsplit
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'sources.json').read_text(encoding='utf-8'))
assert catalog['schema_version']==1 and isinstance(catalog['config_version'],int) and catalog['config_version']>0
for path in [root/'sources.json', *sorted((root/'catalogs').glob('*.json'))]:
    document=json.loads(path.read_text(encoding='utf-8'))
    assert document['schema_version']==1 and type(document['config_version']) is int and document['config_version']>0
    discovery_catalog = path.name in {'switch-homebrew-discovered.json', 'switch2-homebrew-discovered.json', 'ps5-homebrew-discovered.json'}
    assert isinstance(document['sources'], list) and len(document['sources']) <= 64
    assert document['sources'] or discovery_catalog
    ids=set()
    for source in document['sources']:
        assert source['id'] not in ids
        ids.add(source['id'])
        p=urlsplit(source['url'])
        assert p.scheme=='https' and p.hostname and not p.username and not p.password
        assert source.get('kind','feed')=='feed' and not source.get('parent_id')
        assert not source.get('images') or source['id'] in {'example-gamer520', 'gamer520-switch2', 'nsthwj-games', 'nsthwj-switch', 'nsthwj-pc', 'nsthwj-ps4', '4gamers-zh', 'gamesradar-calendar', '4gamers-game-guides', 'switch-homebrew-guides', 'retroarch-official-guides', 'nswiki-switch-guides', 'mushroom-switch', 'mushroom-pc', 'mushroom-ps4'}
        assert source.get('fullContent',False)==(bool(source.get('repo')) or source['id'] in {'fzgamer-archive', '4gamers-zh', 'gamesradar-calendar'})
for path in sorted((root/'feeds').glob('*.json')):
    if path.name.endswith('.health.json'):continue
    assert path.stat().st_size<=2*1024*1024
    doc=json.loads(path.read_text(encoding='utf-8'))
    assert doc['schema_version']==1 and doc['status']=='ok' and isinstance(doc['items'],list) and len(doc['items'])<=100
    for item in doc['items']:
        assert item['title'] and item['original_url'].startswith('https://')
        if path.name == 'gamesradar-calendar.json':
            assert item.get('content_scope') == 'full_feed' and item.get('content')
            assert item['original_url'].startswith('https://www.gamesradar.com/video-game-release-dates/#section-')
            assert not item.get('image_url') or urlsplit(item['image_url']).hostname == 'cdn.mos.cms.futurecdn.net'
        elif path.name in {'mushroom-switch.json', 'mushroom-pc.json', 'mushroom-ps4.json'}:
            assert item.get('content_scope') == 'metadata' and not item.get('content') and not item.get('download_links')
            assert item.get('published_at') or item.get('updated_at')
            assert item['original_url'].startswith('https://www.xn--ogtt23ghrb.cn/SEO/')
            cover = urlsplit(item.get('image_url', ''))
            assert not cover.geturl() or (cover.scheme == 'https' and cover.netloc == 'www.oupai.xyz')
        else:
            assert not item.get('content') and not item.get('image_url')
        assert isinstance(item.get('updated_at',''),str)
        assert isinstance(item.get('summary',''),str) and len(item.get('summary',''))<=241
        assert isinstance(item.get('tags',[]),list) and all(t in {'game_update','firmware_update','research'} for t in item.get('tags',[]))
        links=item.get('download_links',[])
        assert isinstance(links,list) and len(links)<=4
        for link in links:
            target=urlsplit(link['url'])
            assert target.scheme=='https' and target.hostname in {'pan.baidu.com','pan.quark.cn','pan.xunlei.com'} and target.path.startswith('/s/')
            assert not target.username and not target.password and target.port in (None,443) and len(link['url'])<=1024
print('Catalog and public metadata JSON verified')
