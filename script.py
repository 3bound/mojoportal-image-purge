"""Purge images and their directories from a MojoPortal image bank UNLESS they can be found in an SQL export."""

import re
import os
import shutil


# Path to MojoPortal SQL export
sql_path = '/path/to/export.sql'

# Path to MojoPortal image bank
image_bank_path = "/path/to/Image_Bank/"

regex = 'Data/Images/Image_Bank/[0-9]+'


def extract_image_ids(sql_path, regex):
    """Extract image IDs from the SQL export

    String -> List(String)
    """

    sql_file = open(sql_path, 'r')

    ids = [url.split('/').pop()
                   for line in sql_file.readlines()
                   for url in re.findall(regex, line)]
    sql_file.close()

    return ids


def purge(image_bank_path, image_ids):
    """Purge directories whose name does not match a list of image IDs

    String, List(String) -> Side Effect
    """
    directories = [image_bank_path + directory
                   for directory in os.listdir(image_bank_path)
                   if directory not in image_ids]

    for directory in directories:
        print("Deleting directory " + directory)
        shutil.rmtree(directory)

    return True


purge(image_bank_path, extract_image_ids(sql_path, regex))
