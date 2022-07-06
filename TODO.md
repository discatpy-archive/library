# TODO List for DisCatPy API rewrite

- finish the core module

  - add a low level file object
  - client, incorportates everything from core into something devs can work with (migrate the current client, remove models related stuff)
  - built-in event handler

- start the models module

  - migrate all model related files
  - rewrite the model system to incorporate TypedDicts more
  - rewrite the model system around the new core module
  - rewrite the model system to be immutable
  - bot, inherited from client and has support for models
  - extended built-in event handler (handles cache, this will require monkeypatching)

- start working on extensions

  - commands core: the base extension for prefixed commands and application commnads
  - interactions: a high level wrapper for Discord interactions (application commands/ui components)
  - prefixed/text commands: a high level wrapper for prefixed commands, which use messages (requires message content intent)
