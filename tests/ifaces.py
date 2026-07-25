# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

"""
Interfaces used throughout the tests. They're dataclasses so they have a
predictable repr.
"""

import dataclasses


@dataclasses.dataclass
class Service:
    pass


@dataclasses.dataclass
class AnotherService:
    pass
