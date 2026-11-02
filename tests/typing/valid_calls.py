from typing import Callable, overload

from refry import retry


@retry(backoff_increment=0)
def render(index: int, /, label: str = "item", *, enabled: bool = True) -> str:
    return label if enabled else str(index)


text: str = render(1, enabled=False)
default_text: str = render(2)


class Renderer:
    @retry(backoff_increment=0)
    def render(self, value: int) -> str:
        return str(value)


method_text: str = Renderer().render(3)
bound: Callable[[int], str] = Renderer().render


@overload
def identity(value: int) -> int: ...


@overload
def identity(value: str) -> str: ...


def identity(value):
    return value


retried_identity = retry(backoff_increment=0)(identity)
integer: int = retried_identity(4)
string: str = retried_identity("four")
