import pytest


class MyClass:
    def foo(self):
        return 1


@pytest.fixture(scope='session', autouse=True)
def my_class() -> MyClass:
    return MyClass()


def test_foo(my_class: MyClass) -> None:
    assert my_class.foo() == 1


def test_bar(my_class: MyClass) -> None:
    assert my_class.foo() == 1


def test_smth() -> None:
    assert 1 == 1