# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [v12.1.0] - 2026-01-02

### Added
- Python 3.14 compatibility
- Session file locking
- Improved test coverage

### Changed
- Switched CI to uv tooling
- Various housekeeping improvements

## [v12.0.0] - 2024-06-02

### Added
- Smart Home functionality for switch states, energy consumption and power values
- Unit tests for smart home plugin
- FritzBox 7530 AX as supported model
- Improved debug information

### Changed
- Python 3.9 compatibility

## [v11.1.0] - 2023-09-29

### Added
- 60 seconds timeout for requests
- GitHub Actions now run with multiple Python versions
- Requirements files for dev environment

### Changed
- Improved unit tests to patch `requests` package
- Code refactorings
- Raised minimum `pylint` level to 9
- Replaced deprecated `fritzconnection.uptime`

## [v11.0.0] - 2023-09-28

### Added
- Unit tests
- Support for latest FritzOS 7.57

## [v10.1.0] - 2021-10-06

### Changed
- Add missing user from configuration for plugins
- Support pbkdf2 login available since FritzOS 7.24

## [v10.0.0] - 2020-11-17

First version after refactoring as a fork of [fritzbox-munin](https://github.com/Tafkas/fritzbox-munin).

### Added
- Graphs for smart home temperatures
- Configuration environment variable for TLS and certificates
- Public IP address in description of uptime graph

### Changed
- Various code refactorings
- Compatibility with Python 3
- Compatibility with FritzOS 7.20
- Updated fritzconnection dependency
- Proper error handling

[v12.1.0]: https://github.com/ma4nn/fritzbox-munin-fast/compare/v12.0.0...v12.1.0
[v12.0.0]: https://github.com/ma4nn/fritzbox-munin-fast/compare/v11.1.0...v12.0.0
[v11.1.0]: https://github.com/ma4nn/fritzbox-munin-fast/compare/v11.0.0...v11.1.0
[v11.0.0]: https://github.com/ma4nn/fritzbox-munin-fast/compare/v10.1.0...v11.0.0
[v10.1.0]: https://github.com/ma4nn/fritzbox-munin-fast/compare/v10.0.0...v10.1.0
[v10.0.0]: https://github.com/ma4nn/fritzbox-munin-fast/releases/tag/v10.0.0
