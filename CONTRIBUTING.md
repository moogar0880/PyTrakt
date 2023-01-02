# Contributing to python-pytrakt

## Git: setup pre-commit

For convenience this project uses [pre-commit] hooks:

```
brew install pre-commit
pre-commit install
```

It's usually a good idea to run the hooks against all of the files when adding
new hooks (usually pre-commit will only run on the changed files during git
hooks):

```
pre-commit run --all-files
```

You can update your hooks to the latest version automatically by running
`pre-commit autoupdate`. By default, this will bring the hooks to the latest
tag on the default branch.

[pre-commit]: https://pre-commit.com/
