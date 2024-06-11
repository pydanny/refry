# refry

> You know what's better than fries? Fries cooked twice.
>
> What's even better than twice cooked fries is triple cooked fries!

Refry is a modern, maintained, typed easy-to-use retry decorator.

## Installation

```bash
pip install refry
```

## Usage

### Basic usage

```python
import refry

@refry.retry
def function_with_problem():
    raise Exception('Something bad happens here')


# This will be attempted 5 times, each time with a delay increasing
# by 5 seconds.
function_with_problem()
```

### Retry with custom Exception

```python
@refry.retry(rate_limit_exception=ZeroDivisionError)
def function_with_bad_division():
    1 / 0

function_with_bad_division()
```

### Advanced usage: custom backoff and retry count

```python
@refry.retry(backoff_increment=10, retries=3)
def function_with_custom_backoff():
    raise Exception('Something bad happens here')

# This will be attempted 3 times, with a delay increasing by 10 seconds each time.
function_with_custom_backoff()
```

### Asynchronous function support

```python
import asyncio
import refry

@refry.retry
async def async_function_with_problem():
    raise Exception('Something bad happens here')

# This will be attempted 5 times, each time with a delay increasing by 5 seconds.
await async_function_with_problem()
```

### Retry with custom logic

```python
import refry

def custom_logic(exception):
    # Custom logic to determine if a retry should occur
    return isinstance(exception, ZeroDivisionError)

@refry.retry(rate_limit_exception=ZeroDivisionError, retries=3)
def function_with_custom_logic():
    1 / 0

function_with_custom_logic()
```

### Arguments for `refry.retry()`

* `rate_limit_exception`: Types of exception to trigger a retry. Default value is [`Exception`].
* `backoff_increment`: The delay increment in seconds between retries. Default value is `5` seconds.
* `retries`: The number of retry attempts. Default value is `5`.

---

## Comparison with Previous Implementations

Refry is designed to be a modern, maintained, and typed easy-to-use retry decorator.
Here are some comparisons with other popular retry libraries:

* **Tenacity**: [Tenacity](https://pypi.org/project/tenacity/) is a highly configurable retry library for Python. It provides extensive options for backoff strategies, custom retry conditions, and logging. However, Tenacity's flexibility can make it more complex to use for simple retry needs.
* **Retrying**: [Retrying](https://pypi.org/project/retrying/) is another popular retry library that offers simplicity and ease of use. However, it is no longer actively maintained, which can be a concern for projects requiring long-term support.
* **Built-in Solutions**: Frameworks like Django and Flask provide built-in retry mechanisms for certain operations (e.g., database retries). These are often tightly coupled with the framework and may not be suitable for general-purpose retry needs outside of the framework's context.

---

## Development Setup

For development, this project uses [rye](https://rye.astral.sh/) to manage dependencies, environment, and publishing to pypi. 

Once you've [installed the tool](https://rye.astral.sh/guide/installation/), clone the project and follow these instructions.

```bash
cd refry/
rye sync
```

The `rye sync` will set up the local `.venv` folder. 

Running tests:

```bash
rye run tests
```

Formatting the code:

```bash
rye run format
```

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write tests to cover your changes.
4. Run all tests to ensure no regressions.
5. Open a pull request with a detailed description of your changes.


## Contributors 

<table>
<tr>
    <td align="center">
        <a href="https://github.com/pydanny">
            <img src="https://avatars.githubusercontent.com/u/62857?v=4" width="100;" alt="pydanny"/>
            <br />
            <sub><b>Daniel Roy Greenfeld</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/rjvitorino">
            <img src="https://avatars.githubusercontent.com/u/2514072?v=4" width="100;" alt="rjvitorino"/>
            <br />
            <sub><b>Ricardo Vitorino</b></sub>
        </a>
    </td></tr>
</table>

