from refry import retry


@retry(backoff_increment=0)
def render(index: int, /, *, enabled: bool = True) -> str:
    return str(index) if enabled else ""


render("wrong")
render(1, False)
render(index=1)
render(1, missing=True)
number: int = render(1)


class Renderer:
    @retry(backoff_increment=0)
    def render(self, value: int) -> str:
        return str(value)


Renderer().render("wrong")
method_number: int = Renderer().render(1)
