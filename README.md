# Snakemake Logger Plugin - Flowo

A Snakemake logger plugin that stores workflow execution data in PostgreSQL, making your workflow management more efficient and fun! 🎉

## 🎈 Features

- Stores Snakemake workflow execution data in PostgreSQL database
- Tracks jobs, rules, files, and errors
- Provides comprehensive logging and monitoring capabilities
- Easy integration with existing Snakemake workflows

## 💻 Installation

```bash
pip install snakemake-logger-plugin-flowo
```
## 🔧 Configuration

```bash
# To generate the default configuration file, run the following command:
# This will create the default .env configuration file in your $HOME/.config/flowo/ directory.
flowo --generate-config

# After generating the .env file, open it with your preferred text editor to adjust the settings:
vim $HOME/.config/flowo/.env
```
The following environment variables are available for configuration in the `.env` file:

- `POSTGRES_USER`: PostgreSQL username (default: flowo)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: flowo_password)
- `POSTGRES_DB`: PostgreSQL database name (default: flowo_logs)
- `POSTGRES_HOST`: PostgreSQL host (default: localhost)
- `POSTGRES_PORT`: PostgreSQL port (default: localhost: 5432)
- `FLOWO_USER`: User displayed in Flowo
- `FLOWO_WORKING_PATH`: Snakemake execution project path

## 🚀 Usage
Basic usage
```bash
snakemake --logger flowo
```
config `flowo_project_name` or `flowo_tags`
```
snakemake \
    --config flowo_project_name=your_project_name flowo_tags="tagA,tagB,tagC" \
    --logger flowo
```
or config in --configfile
```
flowo_project_name: your_project_name
flowo_tags: "tagA,tagB,tagC"
```


## 📜 License

MIT License
