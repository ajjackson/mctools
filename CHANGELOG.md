# Change Log

Notable changes are logged here by release. This project is not
expected to be especially active and follows a simplified Semantic Versioning:

- Version numbers take the format X.Y
- X is associated with major API breakage / changes in algorithm and results.
- Y is associated with minor updates and improvements
- Small amounts of code tidying, refactoring and documentation do not
  lead to a new release, and simply sit on the Development branch of
  the Git repository.

The changelog format is inspired by [keep-a-changelog](https://github.com/olivierlacan/keep-a-changelog).

## [1.1] - 2024-04-19
Slap a version number on "unreleased" stuff before API-breaking v2

- "sendto" now looks for a config file in home directory
- "sendto" options to skip large VASP files
- New CPLAP plotter
- Add "get-minimum" for quick extraction of low-energy structure from trajectory

## [1.0] - 2017-04-25

- Add "get-volume" for quick read of volume
- Add "get-energy" for quick read of energy
- Update all "get" tools for Python3 compatibility and simpler interface
  - Input file is now consistently the first positional argument so no
    need to remember which optional flag is needed.

## [0.2] - 2016-03-01

- Fix broken get-spacegroup interface
- Add reader/converter for ATAT SQS files

## 0.1 - 2016-11-04

- Begin proper organisation of repository and packaging
- Tools collected from various projects
  - Reasonably functional components
    - ase-convert
    - get-primitive
    - get-spacegroup
    - vectors
  - Primitive / work-in-progress
    - get-vbm
    - vasp-charge
  - Possibly too "personal"
    - sendto
- Packaging with pip
- GPL license

[Unreleased]: https://github.com/ajjackson/mctools/compare/v1.0...HEAD
[1.0]: https://github.com/ajjackson/mctools/compare/v0.2...v1.0
[0.2]: https://github.com/ajjackson/mctools/compare/v0.1...v0.2


