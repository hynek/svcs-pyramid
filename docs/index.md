---
hide-toc: true
---

# *svcs-pyramid*

Release **{sub-ref}`release`**  ([What's new?](https://github.com/hynek/svcs-pyramid/blob/main/CHANGELOG.md))


```{include} ../README.md
:start-after: "<!-- begin index -->"
:end-before: "<!-- end index -->"
```

<!-- skip: next -->

```python
import svcs_pyramid


@view_config(route_name="index")
def view(request):
    db, api, cache = svcs_pyramid.get(request, Database, WebAPIClient, Cache)

    ...
```

```{include} ../README.md
:start-after: "<!-- begin addendum -->"
:end-before: "<!-- end addendum -->"
```

Read on in *{doc}`usage`* – or in [*svcs*'s own documentation](https://svcs.hynek.me/) if you're new to *svcs* itself.

```{toctree}
:hidden:

usage
api
credits
```

```{toctree}
:hidden:
:caption: Meta

svcs <https://svcs.hynek.me/>
PyPI <https://pypi.org/project/svcs-pyramid/>
GitHub <https://github.com/hynek/svcs-pyramid/>
Changelog <https://github.com/hynek/svcs-pyramid/blob/main/CHANGELOG.md>
Contributing <https://github.com/hynek/svcs-pyramid/blob/main/.github/CONTRIBUTING.md>
Security Policy <https://github.com/hynek/svcs-pyramid/blob/main/.github/SECURITY.md>
Funding <https://hynek.me/say-thanks/>
```
