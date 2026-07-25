# API reference

## Application life cycle

```{eval-rst}
.. module:: svcs_pyramid

.. autofunction:: init
.. autofunction:: close_registry

.. autofunction:: svcs_from
.. autofunction:: get_registry

.. autoclass:: PyramidRegistryHaver()
```


## Registering services

```{eval-rst}
.. autofunction:: register_factory
.. autofunction:: register_value
```


## Service acquisition

```{eval-rst}
.. function:: get(request, *svc_types)

   Same as :meth:`svcs.Container.get()`, but uses the container from *request*.

.. autofunction:: get_abstract
.. autofunction:: get_pings
```
