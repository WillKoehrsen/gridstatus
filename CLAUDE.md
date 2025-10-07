# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Testing
- `uv run pytest -s -vv -n auto --reruns 5 --reruns-delay 3 --durations=25` - Run tests with retries and timing
- `make test-unit` - Run unit tests only (excluding integration tests)
- `make test-slow` - Run slow tests marked with @pytest.mark.slow
- `make test-cov` - Run tests with coverage report
- `make test-one-off market=MARKET test=TEST_NAME` - Run single test (e.g., `make test-one-off market=caiso test=test_get_load_latest`)

### Testing by ISO
- `make test-aeso` - Test AESO (Alberta Electric System Operator)
- `make test-caiso` - Test CAISO (California Independent System Operator)
- `make test-ercot` - Test ERCOT (Electric Reliability Council of Texas)
- `make test-isone` - Test ISO New England
- `make test-miso` - Test MISO (Midcontinent Independent System Operator)
- `make test-nyiso` - Test NYISO (New York Independent System Operator)
- `make test-pjm` - Test PJM Interconnection
- `make test-spp` - Test SPP (Southwest Power Pool)
- `make test-eia` - Test EIA (Energy Information Administration)
- `make test-ieso` - Test IESO (Independent Electricity System Operator)

### Linting and Code Quality
- `make lint` - Check code style with ruff
- `make lint-fix` - Fix linting issues automatically
- `uv run ruff check gridstatus/` - Check code style directly
- `uv run ruff format gridstatus/` - Format code
- `make mypy-coverage` - Generate mypy type checking report

### Environment Setup
- `uv venv .venv` - Create virtual environment
- `source .venv/bin/activate` - Activate virtual environment (Linux/macOS)
- `uv sync` - Install dependencies
- `make installdeps-dev` - Install dev dependencies and setup pre-commit hooks
- `make installdeps-test` - Install test dependencies
- `uv pip install vcrpy` - Install VCR.py for test fixtures (needed for unit tests)

### Documentation
- `make docs` - Build documentation using Sphinx
- Documentation is built using Sphinx and hosted on Read the Docs

### Build and Package
- `make package` - Build package for distribution
- `uv build` - Build package directly

## Architecture

### Core Structure
This is a Python library providing a uniform API for accessing electricity market data from major Independent System Operators (ISOs) in North America.

### Main Components
- **Base Class**: `ISOBase` in `gridstatus/base.py` - Common interface for all ISO implementations
- **ISO Implementations**: Each ISO has its own module (e.g., `caiso.py`, `ercot.py`, `nyiso.py`, etc.)
- **Markets Enum**: `Markets` class defines different market types (REAL_TIME_5_MIN, DAY_AHEAD_HOURLY, etc.)
- **Utilities**: `utils.py` contains shared functions like `get_iso()` and `list_isos()`
- **Visualization**: `viz.py` provides plotting capabilities using plotly

### ISO Classes
All ISO classes inherit from `ISOBase` and implement methods like:
- `get_load()` - Get load data
- `get_fuel_mix()` - Get generation fuel mix
- `get_lmp()` - Get Locational Marginal Prices
- `get_status()` - Get system status

### Supported ISOs
- **AESO** - Alberta Electric System Operator
- **CAISO** - California Independent System Operator  
- **ERCOT** - Electric Reliability Council of Texas
- **IESO** - Independent Electricity System Operator (Ontario)
- **ISONE** - ISO New England
- **MISO** - Midcontinent Independent System Operator
- **NYISO** - New York Independent System Operator
- **PJM** - PJM Interconnection
- **SPP** - Southwest Power Pool
- **EIA** - Energy Information Administration

### Testing Framework
- Uses pytest with VCR.py for API response recording/playback
- Test fixtures stored in `gridstatus/tests/fixtures/` organized by ISO
- Markers: `@pytest.mark.slow` for slow tests, `@pytest.mark.integration` for API tests
- Run tests with `make test-unit` to exclude integration tests

### Environment Variables
Some ISOs require API keys set via environment variables:
- EIA API requires `EIA_API_KEY`
- ERCOT API requires `ERCOT_API_USERNAME`, `ERCOT_API_PASSWORD`, `ERCOT_PUBLIC_API_SUBSCRIPTION_KEY`, `ERCOT_ESR_API_SUBSCRIPTION_KEY`
- PJM API requires `PJM_API_KEY`
- MISO API requires `MISO_API_PRICING_SUBSCRIPTION_KEY` and `MISO_API_LOAD_GENERATION_AND_INTERCHANGE_SUBSCRIPTION_KEY`
- AESO API requires `AESO_API_KEY`
- Copy `.env.template` to `.env` and fill in required values
- Export `UV_ENV_FILE=path/to/.env` to make .env accessible to uv runtime

### Key Files
- `gridstatus/__init__.py` - Main package imports and ISO class registry
- `gridstatus/base.py` - Base classes and common functionality
- `pyproject.toml` - Python project configuration with dependencies and tool settings
- `Makefile` - Build and test commands
- `CONTRIBUTING.md` - Development setup and contribution guidelines