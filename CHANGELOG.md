# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
From http://keepachangelog.com

## [Unreleased][unreleased]
### Added
### Changed
### Fixed
### Removed

## 3.1 - 2016-09-15
### Fixed
- wrong paramter to ifup, thanks dimagafurov


## 3.0 - 2016-08-15
### Changed
- Makes flake8 happy
- REMOVED compatibility with python 2.6


## 2.3 - 2016-08-07
### Changed
- Code is ready to be deployed to PyPi


## 2.2 - 2016-07-22
### Changed
- InterfacesWritter : uses ifup --no-act to check for /etc/network/interfaces validity
- adapter : it is possible to access its properties


## 2.1 - 2016-07-10
### Added
- a changelog...

### Changed
- toolutils : safe_subprocess : enforce shell command being an array
- interfacesWriter : uses 'ifup -a --no-act' to check the interfaces file just written.


## 2.0-beta - 2014-09-01
### Changed
- refactoring which breaks retrocompatibility


## 1.0 - 2012-12-15
### Added
- Read, writing, and editing supported.
- Specify file locations in constants.py
