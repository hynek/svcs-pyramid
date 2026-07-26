# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Calendar Versioning](https://calver.org/).

The **first number** of the version is the year.
The **second number** is incremented with each release, starting at 1 for each year.
The **third number** is for emergencies when we need to start branches for older releases.

You can find our backwards-compatibility policy [here](https://github.com/hynek/svcs-pyramid/blob/main/.github/SECURITY.md).

<!-- changelog follows -->


## [26.1.0](https://github.com/hynek/svcs-pyramid/compare/26.1.0...26.1.0) - 2026-07-26

### Deprecated

- `svcs_pyramid.get_abstract()` is carried over from `svcs.pyramid` so that the rename is the only change you have to make, but it's deprecated.
  Thanks to [PEP 747], `svcs_pyramid.get()` does the same thing.
  There are no deprecation warnings or plans to remove it for now.

[PEP 747]: https://peps.python.org/pep-0747/


### Added

- Initial release.
  *svcs-pyramid* is the extraction of *svcs*'s `svcs.pyramid` module into its own package.


### Changed

- The import name is `svcs_pyramid` instead of `svcs.pyramid`.
  Nothing else changed, so migrating is a pure rename:

  ```
  import svcs           →  import svcs_pyramid
  svcs.pyramid.init(…)  →  svcs_pyramid.init(…)
  ```

  The registry and the container are still stored under the `svcs_registry` and `svcs_container` keys, so `svcs_pyramid` is a drop-in replacement for `svcs.pyramid`.
