# Some Guy's Opinions on Technical Direction

System Components:

- ETL system for updating Semantic Graph Database from information sources
- Semantic Graph Database
- Frontend semantic editor
- application server mediating access to graph database

Frontend system diagram:

![frontend system](./fig_01.svg)

Candidate open-source components:

- Event Log: React/Redux
This is one of the standard open-source stacks for building this sort of
application--where there are multiple interacting components and complex real-
time sync requirements for the backend integration.
- Note (code) Editor: CodeMirror
CodeMirror is a popular open source library for building text editors in the
browser. It has hooks for doing autocomplete and real-time parsing. If we use
react-redux, we will need to define the boundary between CodeMirror and the
application, and build a react wrapper.
Example: Should codemirror be publishing onChange events to the full application,
or should we capture these inside a react component and forward those events to
redux? This would be the main responsibility of a codemirror
wrapper--explicitly defining the boundary between the editor/parser and the
rest of the application.
- Parser library: [lezer](https://lezer.codemirror.net/)
Lezer is a system for building incremental parsers (for building code
intelligence into IDE projects). It is designed to work with codemirror. It
could be used to parse the notes-language. Using Lezer at this stage is a bit
of a heavy hammer approach, but it will also provide stable patterns for the
integration with codemirror.
- Semantics Tab
The semantics tab needs to communicate with the backend to populate e.g. the
experts view. Some of the API calls for the semantics tab e.g. (likely
conditions) will also be useful for doing autocomplete in the text editor. This
is one of the reasons for using an explicit central event-log state store--to
share in-memory state across multiple components in a disciplined way.


Backend system diagram:
![backend system](./fig_02.svg)


