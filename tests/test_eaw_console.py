from util import check_width

def test_eaw_console():
    err = check_width('../locale-eaw/dist/UTF-8-EAW-CONSOLE', 'build/EAW-CONSOLE-Regular.ttf')
    assert err == 0

