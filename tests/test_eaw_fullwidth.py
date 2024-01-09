from util import check_width

def test_eaw_fullwidth():
    err = check_width('../locale-eaw/dist/UTF-8-EAW-FULLWIDTH', 'build/EAW-FULLWIDTH-Regular.ttf')
    assert err == 0

