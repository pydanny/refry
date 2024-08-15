# refry

> You know what's better than fries? Fries cooked twice.
>
> What's even better than twice cooked fries is triple cooked fries!

![Refry basic usage example](https://github.com/pydanny/refry/assets/2514072/939ecaf7-c1de-4864-b1c8-24907197bb73)

Refry is a modern, maintained, typed easy-to-use retry decorator.

---

## Installation

```bash
pip install refry
```

---

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

### Retry Decorator with Backoff and Jitter

The `@retry` decorator allows you to automatically retry a function if it raises specific exceptions.
It supports **different backoff strategies** (sequential, logarithmic, exponential) and **optional jitter** to handle the [thundering herd problem](http://www.catb.org/jargon/html/T/thundering-herd-problem.html).


```python
import refry

@refry.retry(rate_limit_exception=Exception, backoff_increment=2, retries=5, backoff_type="sequential", jitter=True)
def function_with_problem():
    raise Exception('Something bad happens here')

# Call the function to see the retry mechanism in action
function_with_problem()
```


### Arguments for `refry.retry()`

* `rate_limit_exception`: Types of exception to trigger a retry. Default value is [`Exception`].
* `backoff_increment`: The delay increment in seconds between retries. Default value is `5` seconds.
* `retries`: The number of retry attempts. Default value is `5`.
* `backoff_type`: The backoff strategy to use. Can be one of `"sequential"`, `"logarithmic"`, or `"exponential"`. Defaults to `"sequential"`.
* `jitter`: If `True`, adds a random amount of time to each backoff interval to prevent thundering herd problem. Defaults to `False`.

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

---

## Contribution Guidelines

### Code of Conduct

This project and everyone participating in it is governed by refry's [Code of Conduct](CODE_OF_CONDUCT.md). 

By participating, you are expected to uphold this code. Please report unacceptable behavior to [@pydanny](https://github.com/pydanny).

### How to contribute

Thank you for considering contributing to refry! We welcome contributions from everyone.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute to this project, including how to report bugs, suggest enhancements, and submit pull requests. 

1. **Fork the repository.**
2. **Create a new branch** from the `main` branch.
3. **Commit your changes** to your branch.
4. **Push your changes** to your fork.
5. **Submit a pull request** from your fork to the `main` branch of the original repository.

---

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

