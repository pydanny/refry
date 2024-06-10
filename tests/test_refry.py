import refry


def test_refry_simple():
    @refry.retry()
    def check():
        return True

    check()


def test_refry_rate_division():
    @refry.retry(ZeroDivisionError, backoff_increment=1, retries=3)
    def function_with_bad_division():
        1 / 0

    function_with_bad_division()
