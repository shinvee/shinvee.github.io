from cli import get_last_block_hash, create_block


def test_get_last_block_hash():
    last = get_last_block_hash('test_blocks')
    assert last == '00517baba6aed0172711aa9d6d28096378ae1a847e22a8c2829fc0a6523830ab' # noqa


def test_create_blocvk():
    block, block_hash = create_block('test', 'test_blocks')
    assert block['prev'] == get_last_block_hash('test_blocks')
    assert block.content == 'test'
