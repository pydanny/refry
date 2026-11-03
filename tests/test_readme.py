"""Exercise the basic README example against the public package."""

from pathlib import Path
import re
import unittest
from unittest.mock import call, patch


class TestReadme(unittest.TestCase):
    """Check that the documented basic example exercises real retries."""

    def test_basic_example_retries_before_raising(self) -> None:
        """Retry the README example five times before its final exception."""
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(
            encoding="utf-8"
        )
        section = readme.split("### Basic usage\n", 1)[1].split("\n### ", 1)[0]
        example = re.search(r"```python\n(.*?)```", section, re.DOTALL)
        self.assertIsNotNone(example)

        # Skip real delays, but execute the documented example and real retry loop.
        with patch("refry.main.time.sleep") as sleep:
            with self.assertRaises(Exception) as raised:
                exec(compile(example.group(1), "<README basic example>", "exec"), {})

        self.assertIs(type(raised.exception), Exception)
        self.assertEqual(
            sleep.call_args_list, [call(5), call(10), call(15), call(20), call(25)]
        )
