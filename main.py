#!/usr/bin/env python

"""TCEQ rich data downloader"""

__author__      = "Abe Hmiel"
__copyright__   = "Copyright 2020"

import os
import logging
from typing import List
from time import sleep
from tempfile import NamedTemporaryFile
from pathlib import Path
import pandas as pd
import requests
import click

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
# a little hack to not have to scrape pages:
# all the excel download links have this pattern, where
# appending any incident number to the following string
# will start a database download
BASE_URL = "https://www2.tceq.texas.gov/oce/eer/index.cfm?fuseaction=main.emissiondwnld&target="

def load_input_data(filename: Path) -> pd.DataFrame:
    """
    Safely loads an xls file into a dataframe
    :param: filename - Path
    :returns: pd.DataFrame
    """
    if Path(filename).exists():
        return pd.read_excel(filename,
                             dtype={"INCIDENT NO.": str})
    else:
        raise ValueError("Input file could not be found")


def link_factory(df: pd.DataFrame) -> List[str]:
    """
    Transforms an input dataframe of tceq incidents to a
    list of urls to visit to download complete incident data
    :param: df - pd.DataFrame input xls file as df
    :returns: list of str
    """
    try:
        incidents = df["INCIDENT NO."].unique()
        links = [BASE_URL + i for i in incidents]
        logger.info(f"Found {len(links)} links in data")
    except:
        links = []
        logger.warning("Could not extract links from data")
    finally:
        return links


def visit_link_and_load_df(url: str) -> pd.DataFrame:
    """
    Transform a bytes object from  a url visit
    into a pandas dataframe
    :param: url - str
    :returns: df - pd.DataFame
    """
    # visit page
    r = requests.get(url)
    # save as named temporary file
    temp_xls = None
    try:
        # Windows suckage - needs xls and to stay on disk after open context
        with open('temp.xls', 'wb') as temp_xls:
            # write excel binary
            # you can't read excel from memory, apparently
            temp_xls.write(r.content)
        # load named file and append to dfs
        df = pd.read_excel("temp.xls")
    except:
        logger.warning(f"could not handle temporary file for {url}")
        df = pd.DataFrame()
    finally:
        if temp_xls is not None:
            os.remove("temp.xls")
        return df


def df_factory(links: List[str], sleep_time: int=5) -> pd.DataFrame:
    """
    iterate over all the links, grab their data and
    accumulate into a dataframe
    """
    dfs = []
    # iterate over links
    for i, url in enumerate(links):
        dfs.append(visit_link_and_load_df(url))
        # wait <5> (or sleep_time) seconds so you don't get borked
        sleep(sleep_time)
        # verbose output
        if i % 10 == 0:
            logger.info(f"Progress: {i+1} of {len(links)}")
    df = pd.concat(dfs, sort=False).reset_index(drop=True)
    return df


@click.command()
@click.option('--input-filename', default="sample.xls",
              help='the input filename from original TCEQ query')
@click.option('--output-filename', default="output.csv",
              help='the output csv filename')
@click.option('--sleep-time', default=5,
              help='how long to wait between requests')
def main(input_filename: str, output_filename: str, sleep_time: int):
    input_df = load_input_data(Path(input_filename))
    links = link_factory(input_df)
    df = df_factory(links, sleep_time)
    df.to_csv(Path(output_filename))
    logger.info(f"wrote combined DataFrame to {output_filename}")


if __name__ == "__main__":
    main()
