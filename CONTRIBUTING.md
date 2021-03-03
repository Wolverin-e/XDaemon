# Contributing to XDaemon

<img src='.readme/favicon/android-chrome-512x512.png' height="100px">
XDaemon is an automation tool.

## Settingup Development environment

Start by Forking [https://github.com/Wolverin-e/XDaemon](https://github.com/Wolverin-e/XDaemon) to yourusername.

```sh
# Clone your forked repository locally
$ git clone git@github.com:<yourusername>/XDaemon.git

# Enter the local directory
$ cd XDaemon

# Add Upstream
$ git remote add upstream https://github.com/Wolverin-e/XDaemon.git

# Create a Virtual env: venv
$ python3 -m venv ./venv

# Activate venv
$ source venv/bin/activate

# Install The Project
$ pip install -e '.[dev]'

# Test the installation by
$ xd
```

## Proposing new changes

```sh
# Update the local master
$ git checkout master
$ git fetch upstream
$ git rebase upstream/master

# Shift onto a new branch from the Master
$ git checkout -b <new-branch-name>


#########################
###   Do.Your.Magic   ###
#########################


# Before Commiting your code
# For Checking PEP8 Violations:
$ flake8 .
# If any violations -> For auto-linting:
$ autopep8 -i <file-to-lint>

# Commit Your Code
$ git add .
$ git commit -m '<good-commit-message>'

# Push your changes from the current branch to create a new branch with the same name
$ git push origin <new-branch-name>

# Create a Pull Request(PR): <your-remote>:<new-branch-name> → Wolverin-e:master
```
