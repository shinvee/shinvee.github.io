from cli import get_last_block


def test_get_last_block():
    last = get_last_block('test_blocks')
    assert last == '00517baba6aed0172711aa9d6d28096378ae1a847e22a8c2829fc0a6523830ab' # noqa
