# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from doctest import ELLIPSIS

import pytest

from sybil import Sybil
from sybil.parsers import myst, rest

from tests.helpers import CloseMe


markdown_examples = Sybil(
    parsers=[
        myst.DocTestDirectiveParser(optionflags=ELLIPSIS),
        myst.PythonCodeBlockParser(doctest_optionflags=ELLIPSIS),
        myst.SkipParser(),
    ],
    patterns=["*.md"],
)

rest_examples = Sybil(
    parsers=[
        rest.DocTestParser(optionflags=ELLIPSIS),
        rest.PythonCodeBlockParser(),
    ],
    patterns=["*.py"],
)

pytest_collect_file = (markdown_examples + rest_examples).pytest()

collect_ignore = []
try:
    import sphinx  # noqa: F401
except ImportError:
    collect_ignore.extend(["docs"])


@pytest.fixture(name="close_me")
def _close_me():
    return CloseMe()
