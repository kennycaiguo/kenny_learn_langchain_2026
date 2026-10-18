from my_add import add

def test_add():
    """测试加法功能"""
    assert add(3, 2) == 5
    assert add(1, -1) == 0
    assert add(0, 0) == 0
    assert add(10, -5) == 5