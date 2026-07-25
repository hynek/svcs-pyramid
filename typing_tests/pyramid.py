# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from collections.abc import Generator

import pyramid
import svcs

from pyramid.config import Configurator

import svcs_pyramid


def factory_with_cleanup() -> Generator[int, None, None]:
    yield 1


config = Configurator(settings={})

svcs_pyramid.init(config)

svcs_pyramid.register_value(config, int, 1)
svcs_pyramid.register_value(config, int, 1, ping=lambda: None)

svcs_pyramid.register_factory(config, str, str)
svcs_pyramid.register_factory(config, int, factory_with_cleanup)
svcs_pyramid.register_value(config, str, str, ping=lambda: None)

req = pyramid.request.Request()

o1: object = svcs_pyramid.get(req, object)
o2: int = svcs_pyramid.get_abstract(req, object)

a: int
b: str
c: bool
d: tuple
e: object
f: float
g: list
h: dict
i: set
j: bytes
a, b, c, d, e, f, g, h, i, j = svcs_pyramid.get(
    req, int, str, bool, tuple, object, float, list, dict, set, bytes
)

pings: list[svcs.ServicePing] = svcs_pyramid.get_pings(req)

reg: svcs.Registry = svcs_pyramid.get_registry(config)
reg = svcs_pyramid.get_registry()

con: svcs.Container = svcs_pyramid.svcs_from()
con = svcs_pyramid.svcs_from(req)

svcs_pyramid.close_registry(config)
