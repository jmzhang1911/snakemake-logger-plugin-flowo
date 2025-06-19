import argparse
from pathlib import Path


def generate_config():
    config_dir = Path.home() / ".config/flowo"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / ".env"
    template = """
### Postgres setting
POSTGRES_USER=snakemake
POSTGRES_PASSWORD=snakemake_password
POSTGRES_DB=snakemake_logs
POSTGRES_HOST=172.16.3.223
POSTGRES_PORT=6666

### APP setting
FLOWO_USER=FlowO
# FLOWO_WORKING_PATH=
"""
    with open(config_path, "w") as f:
        f.write(template)
    print(f"Default config generated at {config_path}")


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
