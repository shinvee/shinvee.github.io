import os

from cli import (get_last_block_hash,
                 create_block,
                 create_block_command,
                 check_spell)
from click.testing import CliRunner


def test_get_last_block_hash():
    last = get_last_block_hash('test_blocks')
    assert last == '00517baba6aed0172711aa9d6d28096378ae1a847e22a8c2829fc0a6523830ab' # noqa

    new_dir_path = 'new_test_blocks'
    os.mkdir(new_dir_path)
    assert not get_last_block_hash(new_dir_path)
    os.rmdir(new_dir_path)


def test_create_blocvk():
    block, block_hash = create_block('test', 'test_blocks')
    assert block['prev'] == get_last_block_hash('test_blocks')
    assert block.content == 'test'


def test_cli():
    runner = CliRunner()
    result = runner.invoke(
        create_block_command,
        ['-m', 'test', '-p', 'test_blocks']
    )
    assert result.exit_code == 0
    assert result.output.find('test') > 0


def test_spell_checker():
    assert not check_spell('안녕하세요.')
