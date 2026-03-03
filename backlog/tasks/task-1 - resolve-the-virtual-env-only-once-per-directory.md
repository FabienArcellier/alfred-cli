## Description
Cache the resolved virtual environment path per directory to avoid redundant venv detection operations during a single alfred session. The `venv_lookup()` function in `interpreter.py` is called multiple times (e.g., from `ctx.py` in `invoke_through_external_venv()` and `should_use_external_venv()`), causing repeated filesystem operations for the same project directory.

### Benefits

- **Performance improvement**: Eliminates redundant venv detection operations by caching results
- **Reduced filesystem I/O**: Fewer stat calls and directory traversals per command execution
- **Consistency**: Ensures the same venv is used throughout a session for a given directory
- **Better user experience**: Faster command execution, especially in projects with nested commands
- **Simple implementation**: Uses Python's built-in `functools.lru_cache` decorator (already used in `commands.py`)

### Risks

- **Stale cache**: If the venv is moved or deleted during a session, the cache may point to an invalid location (mitigation: cache is per-process, cleared on restart)
- **Testing complexity**: Tests may need to clear cache between assertions to avoid interference
- **Cache invalidation**: Need to ensure cache is cleared appropriately when switching contexts in tests

## Implementation Plan

### Todo

- [x] Add LRU cache to venv_lookup function

Import `functools.lru_cache` and apply the `@lru_cache(maxsize=None)` decorator to the `venv_lookup()` function in `src/alfred/interpreter.py`. This will cache results based on the `project_dir` parameter.

- [x] Add cache_clear function for testing

Create a `venv_lookup_cache_clear()` function in `src/alfred/interpreter.py` that calls `venv_lookup.cache_clear()` to allow tests to reset the cache between test cases.

- [x] Update integration tests to clear cache

Modify `tests/integrations/test_interpreter.py` to clear the venv lookup cache before or after each test to prevent test interference.

### Files

- src/alfred/interpreter.py
- tests/integrations/test_interpreter.py
- tests/units/test_interpreter.py

## Temporary updates to merge

