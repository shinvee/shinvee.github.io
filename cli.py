import datetime
import hashlib
import os

import click
import frontmatter


def get_last_block():
    blocks = os.listdir('blocks')
    if len(blocks) == 0:
        return None
    else:
        linked = []
        for block_hash in blocks:
            block = frontmatter.load(f'blocks/{block_hash}')
            if 'prev' in block:
                linked.append(block['prev'])
        return [i for i in blocks if i not in linked][0]


@click.command()
@click.option('--message', help='message to write in a block', prompt='Message')
def create_block(message):
    meta = dict()
    last_block = get_last_block()
    if last_block:
        meta['prev'] = last_block
    meta['created_at'] = datetime.datetime.now().isoformat()
    meta['nonce'] = 0
    while True:
        meta['nonce'] += 1
        meta_string = '\n'.join([f'{k}: {v}' for k, v in meta.items()])
        data = f'---\n{meta_string}\n---\n{message}'
        block_hash = hashlib.sha256(data.encode()).hexdigest()
        if block_hash[:2] == '00':
            break
    with open(f'blocks/{block_hash}', 'w') as block_file:
        print(data, file=block_file)
        print(data)

    with open('index.html', 'w') as index:
        print(f"""
            <html>
            <head>
            <script src="https://code.jquery.com/jquery-3.4.0.min.js"></script>
            </head>
            <body>
            <article></article>
            <script>$('article').load('blocks/{block_hash}')</script>
            </body>
            </html>
        """, file=index)

if __name__ == '__main__':
    create_block()
