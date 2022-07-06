# ![Banner for DisCatPy](./assets/banner.png)

A high level, asynchronous Discord API wrapper made completely from scratch.

[![Discord Server invite](https://img.shields.io/discord/947409224361738250?label=discord&style=for-the-badge&logo=discord&color=5865F2&logoColor=white)](https://discord.gg/v7r9hNqQJb)
[![PyPi Version](https://img.shields.io/pypi/v/discatpy.svg?style=for-the-badge&logo=pypi)](https://pypi.org/project/discatpy/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/discatpy?style=for-the-badge)](https://pypi.org/project/discatpy/)

## Warning

Before you use DisCatPy, please make sure you know that it is currently in **pre-alpha** status. Bugs are prone to happen and not all features are implemented yet.

If you do experience any issues with DisCatPy, you can go ahead and open up an issue. If you want to contribute, then feel free to. Contributions are always welcome!

## Features

DisCatPy currently supports:

- Modern async/await syntax
- Proper handling of Discord's REST API and Gateway
- Proper REST API ratelimiting

If you want to see what DisCatPy is planning to support, check out the project board for v1.0 in the Projects tab.

### API Design

DisCatPy has a unique API design structured into folders. Here are the main elements of the API:

- Core
  - The core contains the main, lower level elements of the API
  - This includes raw HTTP and Gateway handlers, as well as a client
  - The core can be used directly by users, but it's not recommended to as you'll have to handle the Discord models yourself
- Models
  - The model is named after Discord Models, and it contains the more high level elements of the API relating to Discord Models (hence the name)
  - This includes Discord Model wrappers, like for example a wrapper for a Message
  - These models are immutable, and modifying them with an `edit` function for example returns a new model
  - The model also contains a bot, which inherits from client and adds caching capabilities
  - The model is encouraged to be used by users, but you aren't forced to use it
- Extensions
  - Extensions modify the usage of DisCatPy by adding new features
  - Commands Base
    - The commands base is the base for extensions that add wrappers for commands
    - It adds a simple command, which has a callback, hooks, and other things
    - It also adds options and command groups
  - Interactions
    - The high level wrapper for interactions
    - Interactions can techincally be used without this extension, but it's more low level
    - The interactions extension implements Appliation Commands, which inherit from the Commands Base
    - The interactions extensions also implements UI Components
  - Prefixed Commands
    - The high level wrapper for prefixed commands/text based commands
    - This wrapper is like most other ones in other libraries

## Installing

Currently, the PyPi package does not have a pre-release version. Therefore, you'll have to install directly from the git repo.

Make sure you have `git` installed before doing this.

Run this command in a terminal:

```bash
# For Unix systems
python3 -m pip install git+https://github.com/EmreTech/DisCatPy
```

If you're using Windows, then you'll have to search up how to do this.

## Licensing

DisCatPy is licensed under the MIT License. Please read the [LICENSE](./LICENSE) file for more details.
