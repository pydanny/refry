import refry


def test_refry_simple():
    
    @refry.retry()
    def check():
        return True
    
    check()