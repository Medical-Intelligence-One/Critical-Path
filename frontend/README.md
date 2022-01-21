# What

A shell for mi1 engineers to iterate on frontend concepts. Minimal decisions
made. This is deliberately incomplete. It makes no decisions about deployment.

The main thing this ignores is that we'll need something other than `js/app.js`
to serve the javascript bundle to the frontend. This can be worked out later,
we'll just have to change the html when we do so.

# Set up
1. [ Install nvm ](https://github.com/nvm-sh/nvm#installing-and-updating) to
   manage javascript versions (like `pyenv` for having virtualenvs with
   multiple python versions, kinda).
2. Use latest node long term support release
3. [Install `esbuild`](https://esbuild.github.io/getting-started/#install-esbuild) to
   bundle the javascript.
```
nvm i --lts
nvm use --lts
```
3. Run the frontend locally
```
npm start
```
