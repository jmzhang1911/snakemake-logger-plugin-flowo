![Stars](https://static.pepy.tech/personalized-badge/snakemake-logger-plugin-flowo?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)
![Stars](https://img.shields.io/pypi/v/snakemake-logger-plugin-flowo.svg)

# Snakemake Logger Plugin - Flowo

A Snakemake logger plugin designed to be used with **[FlowO](https://github.com/zhanghaomiao/flowo)** for real-time task monitoring, making workflow management simple, interactive, and fun! 🎉

**Demo page: [flowo online](https://zhanghaomiao.github.io/flowo)**

**Important:** This plugin is designed to be used together with FlowO and requires FlowO to function correctly. It is not a standalone monitoring tool.

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
- `POSTGRES_PORT`: PostgreSQL port (default: 5432)
- `FLOWO_USER`: User displayed in Flowo
- `FLOWO_WORKING_PATH`: Snakemake execution project path

**Note:** The PostgreSQL database used by this plugin is configured in FlowO. Ensure FlowO is properly set up before using this logger plugin.

````

## 🚀 Usage
Basic usage
```bash
snakemake --logger flowo
````

Optional args: `logger-flowo-name` or `logger-flowo-tags`

```
snakemake \
    --logger flowo \
    --logger-flowo-name=your_project_name \
    --logger-flowo-tags="tagA,tagB,tagC"
```

## 🙏 Acknowledgement

This project is developed based on the excellent work of [cademirch/snakemake-logger-plugin-snkmt](https://github.com/cademirch/snakemake-logger-plugin-snkmt).
Special thanks to the original author for providing a solid foundation under the MIT License.
