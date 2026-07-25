# Usage

*svcs-pyramid* uses Pyramid's {class}`pyramid.registry.Registry` to store its own {class}`svcs.Registry` (yes, unfortunate name clash) and a {term}`tween` that attaches a fresh {class}`svcs.Container` to every request and closes it afterwards.


## Installation

```console
$ uv pip install svcs-pyramid
```

::: {note}
*svcs-pyramid* used to be the `svcs.pyramid` module that shipped with *svcs* itself.
If you're migrating, the only change you have to make is the import:

```
import svcs           →  import svcs_pyramid
svcs.pyramid.init(…)  →  svcs_pyramid.init(…)
```

The names under which the registry and the container are stored are unchanged, so both packages are interchangeable.
:::


## Initialization

The most important API is {func}`svcs_pyramid.init()` that takes an {class}`pyramid.config.Configurator` and optionally the positions where to put its {term}`tween` using the *tween_under* and *tween_over* arguments.

You can use {func}`svcs_pyramid.register_factory()` and {func}`svcs_pyramid.register_value()` that work like their {class}`svcs.Registry` counterparts but take a {class}`pyramid.config.Configurator` as the first option (or any other object that has a `registry: dict` field, really).

So you application factory is going to look something like this:

```python
def make_app():
    ...

    with Configurator(settings=settings) as config:
        svcs_pyramid.init(config)
        svcs_pyramid.register_factory(config, Database, db_factory)

        ...

        return config.make_wsgi_app()
```


## Service acquisition

You can use {func}`svcs_pyramid.svcs_from()` to access a request-scoped {class}`svcs.Container` from a request object:

```python
from svcs_pyramid import svcs_from


def view(request):
    db = svcs_from(request).get(Database)
```

Or you can use {func}`svcs_pyramid.get()` to access a service from the current request directly:

```python
import svcs_pyramid


def view(request):
    db = svcs_pyramid.get(request, Database)
```


### Thread locals

Despite being [discouraged](<inv:#narr/threadlocals>), you can use Pyramid's thread locals to access the active container.

So this:

```python
def view(request):
    registry = svcs_pyramid.get_registry()
    container = svcs_pyramid.svcs_from()
```

is equivalent to this:

```python
def view(request):
    registry = svcs_pyramid.get_registry(request)
    container = svcs_pyramid.svcs_from(request)
```

::: {caution}
These functions only work from within **active** Pyramid requests.
:::


(health)=

## Health checks

You can use {func}`svcs_pyramid.get_pings` to get all registered health checks.

A health endpoint could look like this:

```{literalinclude} examples/health_check.py
```


## Testing

Assuming you have an application factory `your_app.make_app()`[^factory] that initializes and configures *svcs* using {func}`svcs_pyramid.init()`, you can use the following fixtures to get a [WebTest application](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/functional_testing.html) and its registry for overrides:

[^factory]: The one that returns {meth}`pyramid.config.Configurator.make_wsgi_app`.

% skip: next

```python
from your_app import make_app

import pytest
import svcs_pyramid
import webtest


@pytest.fixture
def app():
    app = make_app()

    with svcs_pyramid.get_registry(app):
        yield webtest.TestApp(app)


@pytest.fixture
def registry(app):
    return svcs_pyramid.get_registry(app)
```

Now you can write a test like this:

```python
from sqlalchemy import Engine


def test_broken_database(app, registry):
    boom = Mock(spec_set=Engine)
    boom.execute.side_effect = RuntimeError("Boom!")

    registry.register_value(Engine, boom)  # ← override the database

    resp = app.get("/some-url")

    assert 500 == resp.status_code
```

Since {func}`~svcs_pyramid.init()` takes a *registry* keyword argument, you can also go the other way around and pass a (potentially pre-configured) {class}`svcs.Registry` *into* your application factory.


## Cleanup

You can use {func}`svcs_pyramid.close_registry()` to close the registry that is attached to the {class}`pyramid.registry.Registry` of the config or app object that you pass as the only parameter.
