import argparse
from pathlib import Path
from .config import logger


def generate_config():
    config_dir = Path.home() / ".config/flowo"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / ".env"
    template = """
### Postgres setting
POSTGRES_USER=flowo
POSTGRES_PASSWORD=flowo_password
POSTGRES_DB=flowo_logs
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

### APP setting
FLOWO_USER=FlowO
# FLOWO_WORKING_PATH
"""
    with open(config_path, "w") as f:
        f.write(template)
    logger.info(f"Default config generated at {config_path}")


def main():
    parser = argparse.ArgumentParser(description="Flowo Logger Plugin Utility")
    parser.add_argument(
        "--generate-config",
        action="store_true",
        help="Generate default config at ~/.config/flowo/.env",
    )

    args = parser.parse_args()
    if args.generate_config:
        generate_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
