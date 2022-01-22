# What

A shell for mi1 engineers to iterate on frontend concepts. Minimal decisions
made.

I've chosen snowpack for a bundler since it uses `esbuild` under the hood and
gives us the niceties of using something more unwieldy like `webpack`.

# Set up
1. [ Install nvm ](https://github.com/nvm-sh/nvm#installing-and-updating) to
   manage javascript versions (like `pyenv` for having virtualenvs with
   multiple python versions, kinda).
1. Use latest node long term support release
```
nvm i --lts
nvm use --lts
```
1. Install javascript modules `npm i` (short for `npm install`).
1. Run the frontend locally:
```
npm start
```

# What it does

It's a blank [codemirror](https://codemirror.net/6/) editor instance. Building
out support for the order language and syncing to the backend are totally
ignored so far.


