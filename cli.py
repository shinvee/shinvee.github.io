import datetime
import hashlib
import os

import click
import frontmatter
from jinja2 import Template


def get_last_block(block_path='blocks'):
    blocks = os.listdir(block_path)
    if len(blocks) == 0:
        return None
    else:
        linked = []
        for block_hash in blocks:
            block = frontmatter.load(f'{block_path}/{block_hash}')
            if 'prev' in block:
                linked.append(block['prev'])
        return [i for i in blocks if i not in linked][0]


@click.command()
@click.option('--message', '-m',
              help='message to write in a block',
              prompt='Message')
def create_block(message):
    meta = dict()
    block_path = 'blocks'
    last_block = get_last_block(block_path)
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
    with open(f'{block_path}/{block_hash}', 'w') as block_file:
        print(data, file=block_file)
        print(data)

    with open('index.html.jinja2') as file_:
        template = Template(file_.read())
        with open('index.html', 'w') as index:
            print(template.render(block_hash=block_hash), file=index)


if __name__ == '__main__':
    create_block()
