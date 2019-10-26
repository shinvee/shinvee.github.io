import datetime
import json
import hashlib
import os
import re
import pprint

import click
import frontmatter
import requests
from jinja2 import Template


def check_spell(text):
    cookies = {'ruleMode': 'weak'}
    headers = {
        'Origin': 'http://speller.cs.pusan.ac.kr',
    }
    data = {
      'text1': text
    }
    response = requests.post(
        'http://speller.cs.pusan.ac.kr/results',
        headers=headers, cookies=cookies, data=data
    )

    if '맞춤법과 문법 오류를 찾지' in response.text:
        return None
    else:
        regex = re.compile(r"data = (\[[^;].*);")
        mo = regex.search(response.text)
        return json.loads(mo.groups()[0])


def get_last_block_hash(block_path):
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


def create_block(message, block_path):
    block = frontmatter.loads('')
    last_block_hash = get_last_block_hash(block_path)
    if last_block_hash:
        block['prev'] = last_block_hash
    block['created_at'] = datetime.datetime.now().isoformat()
    block['nonce'] = 0
    block.content = message
    while True:
        block['nonce'] += 1
        block_hash = hashlib.sha256(
            frontmatter.dumps(block).encode()
        ).hexdigest()
        if block_hash[:2] == '00':
            break
    return block, block_hash


@click.command()
@click.option('--message', '-m',
              help='message to write in a block',
              prompt='Message')
@click.option('--block-path', '-p',
              default='blocks',
              help='block path')
def create_block_command(message, block_path):
    spell_check_result = check_spell(message)
    if spell_check_result:
        pprint.pprint(spell_check_result)
        exit(1)

    block, block_hash = create_block(message, block_path)
    with open(f'{block_path}/{block_hash}', 'w') as block_file:
        print(frontmatter.dumps(block), file=block_file)
        print(frontmatter.dumps(block))

    with open('index.html.jinja2') as file_:
        template = Template(file_.read())
        with open('index.html', 'w') as index:
            print(template.render(block_hash=block_hash), file=index)


if __name__ == '__main__':
    create_block_command()
