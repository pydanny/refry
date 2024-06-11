# refry

> You know what's better than fries? Fries cooked twice.
>
> What's even better than twice cooked fries is triple cooked fries!

Refry is a modern, maintained, typed easy-to-use retry decorator.

## Installation

```
pip install refry
```

## Usage

Basic usage

```python
import refry

@refry.retry
def function_with_problem():
    raise Exception('Something bad happens here')


# This will be attempted 5 times, each time with a delay increasing
# by 5 seconds.
function_with_problem()
```

With custom exception:

```python
@refry.retry(ZeroDivisionError)
def function_with_bad_division():
    1 / 0


function_with_bad_division()
```

## Development

For development this project uses [rye](https://rye.astral.sh/) to manage dependencies, environment, and publishing to pypi. Once you've [installed the tool](https://rye.astral.sh/guide/installation/), clone the project and follow these instructions.

```
cd refry/
rye sync
```

The `rye sync` will set up the local `.venv` folder. 

Running tests:

```
rye run tests
```

Formatting the code:

```
rye run format
```


## Contributors 

<!-- readme: contributors -start -->
<!-- readme: contributors -end -->