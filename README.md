# Snakemake Logger Plugin - Flowo

A Snakemake logger plugin that stores workflow execution data in PostgreSQL.

## Features

- Stores Snakemake workflow execution data in PostgreSQL database
- Tracks jobs, rules, files, and errors
- Provides comprehensive logging and monitoring capabilities
- Easy integration with existing Snakemake workflows

## Installation

```bash
pip install snakemake-logger-plugin-flowo
```

## Usage

### 1. Configure Database

Set up your PostgreSQL database and configure the connection:

```bash
export POSTGRES_USER=snakemake
export POSTGRES_PASSWORD=snakemake_password
export POSTGRES_DB=snakemake_logs
```

### 2. Use with Snakemake

Run your Snakemake workflow with the logger plugin:

```bash
snakemake --logger flowo
```

## Configuration

The plugin can be configured using environment variables:

- `POSTGRES_USER`: PostgreSQL username (default: snakemake)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: snakemake_password)
- `POSTGRES_DB`: PostgreSQL database name (default: snakemake_logs)
- `SQL_ECHO`: Enable SQL query logging (default: False)

## Development

### Setup

```bash
git clone <repository-url>
cd snakemake-logger-plugin-flowo
uv sync
```

### Build

```bash
uv build
```

## License

MIT License
