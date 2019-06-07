# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2020, Lars Asplund lars.anders.asplund@gmail.com

"""
Command line utility to build documentation/website
"""

from subprocess import check_call
from pathlib import Path
import sys
from sys import argv
from shutil import copyfile
from create_release_notes import create_release_notes

import json
from docs_utils import (
    examples,
    copy_common,
    get_btdpy
)


DROOT = Path(__file__).parent.parent / 'docs'


def main():
    """
    Build documentation/website
    """
    docs = str(Path(__file__).parent / '..' / 'docs')
    get_btdpy(docs)
    sys.path.append(docs)
    import btd
    btd.get_theme()
    with str(Path(__file__).parent / '..' / 'docs' / 'context.json').open("w") as fptr:
        json.dump({
            'slug_user': 'VUnit',
            'slug_repo': 'vunit',
            'slug_path': 'master/docs/',
            'current_version': 'master',
        }, fptr)
    # btd.custom_last()
    del sys.modules["btd"]
    sys.path.remove(docs)

    copy_common()
    examples()
    copyfile(str(DROOT / '..' / 'LICENSE.rst'), str(DROOT / 'license.rst'))
    get_theme(
        DROOT,
        "https://codeload.github.com/buildthedocs/sphinx.theme/tar.gz/v0"
    )
    create_release_notes()
    check_call(
        [
            sys.executable,
            "-m",
            "sphinx"
        ] + ([] if len(argv) < 2 else argv[2:]) + [
            "-TEWanb",
            "html",
            Path(__file__).parent.parent / "docs",
            argv[1],
        ]
    )


if __name__ == "__main__":
    main()
