import argparse

import yaml
from rich.console import Console

from src.build_dataset import Downloader
from src.export import Exporter
from src.find_breakouts import find_breakouts
from src.messages import BANNER


def main():
    console = Console()
    console.print(BANNER, style="white")

    # Setup
    parser = argparse.ArgumentParser(
        description="BreakoutFinder is an educational tool for finding stock breakouts. Its "
                    "results won't be entirely perfect, but can be used for studying.")
    parser.add_argument('--config', type=str, default="config.yaml", help='Path to configuration file. Default: '
                                                                          '"config.yaml" (in directory of executable)')
    args = parser.parse_args()
    config_file = open(args.config, "r")
    config = yaml.safe_load(config_file)
    exporter = Exporter(config)

    # Download stock data, defaults to ZIP files from Google Drive
    downloader = Downloader(config.get("exchanges"), config)
    if config.get("data_download") == "yahoo":
        with console.status("[bold green]Downloading data from Yahoo Finance...") as status:
            downloader.download_data(config['exchanges'])
    else:
        with console.status("[bold green]Downloading and unzipping data...") as status:
            downloader.download_zips(config['exchanges'])

    # Setup how to export found breakouts
    export_callbacks = []
    for exp in config['exports']:
        if exp == "img":
            export_callbacks.append(exporter.export_static_chart)
        elif exp == "interactive":
            export_callbacks.append(exporter.export_interactive)
        elif exp == "csv":
            export_callbacks.append(exporter.export_csv)

    # Start finding breakouts
    find_breakouts(
        console,
        config['exchanges'],
        config,
        export_callbacks
    )


if __name__ == '__main__':
    main()
