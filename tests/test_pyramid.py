# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock

import httpx2
import pytest
import svcs

from pyramid.config import Configurator
from pyramid.view import view_config

import svcs_pyramid

from tests.helpers import nop
from tests.ifaces import AnotherService, Service


@pytest.fixture(name="config")
def _config():
    config = Configurator(settings={})
    svcs_pyramid.init(config)

    config.add_route("tl_view", "/tl")
    config.add_route("health_view", "/health")

    config.scan(".test_pyramid")

    return config


@pytest.fixture(name="app")
def _app(config):
    return config.make_wsgi_app()


@pytest.fixture(name="client")
def _client(app):
    return httpx2.Client(
        transport=httpx2.WSGITransport(app=app), base_url="http://example.com/"
    )


@pytest.fixture(name="rh", params=(0, 1))
def _rh(request, config, app):
    """
    A RegistryHaver fixture -- usually that's configs and apps.
    """
    return (config, app)[request.param]


def test_close_nop(rh):
    """
    Closing a config/app that has no svcs_registry does nothing.
    """
    svcs_pyramid.close_registry(Mock(registry={}))


def test_close(rh):
    """
    Closing a config/app with svcs_registry calls the on_registry_close
    callbacks of the registered services.
    """
    orc = Mock()

    svcs_pyramid.register_factory(rh, int, int, on_registry_close=orc)

    svcs_pyramid.close_registry(rh)

    assert orc.called


def test_init_custom_registry():
    """
    A registry that is passed to init() is used instead of a fresh one.
    """
    registry = svcs.Registry()
    config = Configurator(settings={})

    svcs_pyramid.init(config, registry=registry)

    assert registry is svcs_pyramid.get_registry(config)


@view_config(route_name="tl_view", renderer="json")
def tl_view(request):
    """
    Thread locals return the same objects as the direct way.
    """
    svc = svcs_pyramid.get(request, Service)
    svcs_pyramid.get(request, float)

    assert (
        svc
        is svcs_pyramid.get(request, Service)
        is svcs_pyramid.svcs_from(request).get(Service)
        is svcs_pyramid.get_abstract(request, Service)
    )
    assert (
        request.registry["svcs_registry"]
        is svcs_pyramid.get_registry()
        is svcs_pyramid.get_registry(request)
    )
    assert (
        request.svcs_container
        is svcs_pyramid.svcs_from()
        is svcs_pyramid.svcs_from(request)
    )

    return {"svc": svc}


@view_config(route_name="health_view", renderer="json")
def health_view(request):
    pings = svcs_pyramid.get_pings(request)

    assert pings == svcs_pyramid.svcs_from(request).get_pings()

    for ping in pings:
        ping.ping()

    return {"num": len(pings)}


class TestIntegration:
    def test_get(self, app, client, close_me):
        """
        Service acquisition via svcs_get and thread locals works.
        """

        def closing_factory():
            yield 1.0

            close_me.close()

        svcs_pyramid.get_registry(app).register_value(Service, 42)
        svcs_pyramid.register_value(app, AnotherService, 23)
        svcs_pyramid.register_factory(app, float, closing_factory)

        assert {"svc": 42} == client.get("/tl").json()
        assert close_me.is_closed

    def test_get_pings(self, app, client):
        """
        get_pings() returns service pings with and without passing a request.
        """
        svcs_pyramid.get_registry(app).register_value(Service, 42, ping=nop)

        assert {"num": 1} == client.get("/health").json()
