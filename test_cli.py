from cli import get_last_block_hash


def test_get_last_block_hash():
    last = get_last_block_hash('test_blocks')
    assert last == '00517baba6aed0172711aa9d6d28096378ae1a847e22a8c2829fc0a6523830ab' # noqa
