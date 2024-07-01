# Contributing to refry

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to refry. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How can I contribute?](#how-can-i-contribute)
  - [Reporting bugs](#reporting-bugs)
  - [Suggesting enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)

## Code of Conduct

This project and everyone participating in it is governed by refry's [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [@pydanny](https://github.com/pydanny).

## How can I contribute?

### Reporting bugs

This section guides you through submitting a bug report for refry. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

Before creating a bug report, please check if an issue already exists and has been addressed.

#### How do I submit a (good) bug report?

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible.
- **Provide specific examples** to demonstrate the steps.
- **Describe the behavior you observed** after following the steps and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see** instead and why.
- **Include screenshots** which might help to illustrate the problem.
- **If the problem is related to performance or memory**, include a [profile log](https://docs.python.org/3/library/profile.html) with your report.

### Suggesting enhancements

This section guides you through submitting an enhancement suggestion for refry, including completely new features and minor improvements to existing functionalities. 

#### How do I submit a (good) enhancement suggestion?

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Provide specific examples to demonstrate** the steps.
- **Describe the current behavior and explain which behavior you expected to see** instead and why.
- **Include screenshots or code snippets** which might help to illustrate the suggestion.

### Pull Requests

The process described here will help you to get your contributions accepted more easily.

#### Before Submitting a Pull Request

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the [README.md](README.md) with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Ensure your feature or fix passes all tests.
- Make sure your commit messages are clear and appropriate.

#### Submitting a Pull Request

1. **Fork the repository.**
2. **Create a new branch** from the `main` branch.
3. **Commit your changes** to your branch.
4. **Push your changes** to your fork.
5. **Submit a pull request** from your fork to the `main` branch of the original repository.

## Style Guides

### Git Commit Messages

- Follow [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) best practices:
  - Use `feature/`, `bugfix/`, `docs/`, `release/`, `hotfix/`, and `support/` prefixes for branch names.
  - Regularly rebase your feature branch with the `main` branch to keep up to date.
  - Merge your feature branch into `main` once it is complete.
- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally after the first line.
- Optionally consider starting the commit message with an applicable emoji:
  - :bug: `:bug:` for a bug fix.
  - :sparkles: `:sparkles:` for a new feature.
  - :memo: `:memo:` for documentation.
  - :rocket: `:rocket:` for performance improvements.
  - :lipstick: `:lipstick:` for UI improvements.

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- Use [Black](https://github.com/psf/black) for code formatting.
- Write [docstrings](https://www.python.org/dev/peps/pep-0257/).
- Use type hints where possible.
- Follow [Ruff](https://github.com/charliermarsh/ruff) rules for linting:
  - Install Ruff with `pip install ruff` in your development environment or with `rye` as [documented](README.md#development-setup).
  - Run Ruff with `ruff check .` to check for linting issues.
  - Use `ruff --fix` to automatically fix issues where possible.

---

Thank you for considering contributing to refry!

We look forward to your contributions.
