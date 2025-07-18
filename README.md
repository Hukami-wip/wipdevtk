# wipdevtk

A minimal Python development toolkit for database connections and utilities.

## Installation

```bash
pip install -e .
```

## Usage

```python
from wipdevtk.interfaces.connectors.sql_connector import SQLConnector
from wipdevtk.sql.utils import _session

# Initialize database connector
connector = SQLConnector(connection_url="your_database_url")

# Use _session decorator
@_session
def my_function(session):
    # Your database operations here
    pass
```

## Features

-   SQLConnector for database connections
-   Session management with \_session decorator
-   Logging utilities
-   Development mode support

## License

MIT License
