# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2020, Lars Asplund lars.anders.asplund@gmail.com

"""
Helper functions to get/generate sources for the documentation
"""

import sys
import json
import inspect
from pathlib import Path
from os import listdir, remove
from subprocess import check_call
from shutil import copyfile
from urllib.request import urlretrieve

ROOT = Path(__file__).parent.parent / "docs"


def get_btdpy(location):
    btdpy = Path(location) / "btd.py"
    if not btdpy.is_file():
        urlretrieve("https://github.com/buildthedocs/btd/raw/py/btd.py", str(btdpy))


def copy_common():
    """
    Copy RST sources used outside 'docs' into 'docs' and fix paths accordingly
    """
    with (Path(ROOT) / ".." / "README.rst").open("r") as fptr:
        data = fptr.readlines()
        rm = []
        for i, s in enumerate(data):
            if "<!-- GHONLY -->" in s:
                rm += [i - 1]
            elif "<!-- /GHONLY -->" in s:
                rm += [i + 1]
        for x in range(int(len(rm) / 2)):
            del data[rm[2 * x] : rm[2 * x + 1]]
        with (Path(ROOT) / "readme.rst").open("w") as fptr:
            fptr.writelines(data)
    check_call(
        [
            "sed",
            "-i",
            "s#\./docs/_static/img/#_static/img/#g",
            str(Path(ROOT) / "readme.rst"),
        ]
    )
    copyfile(str(Path(ROOT) / ".." / "LICENSE.rst"), str(Path(ROOT) / "license.rst"))


def examples():
    """
    Traverses the examples directory and generates examples.rst with the docstrings
    """
    eg_path = ROOT.parent / "examples"
    egs_fptr = (ROOT / "examples.rst").open("w+")
    egs_fptr.write("\n".join([".. _examples:\n", "Examples", "========", "\n"]))
    for language, subdir in {"VHDL": "vhdl", "SystemVerilog": "verilog"}.items():
        egs_fptr.write("\n".join([language, "~~~~~~~~~~~~~~~~~~~~~~~", "\n"]))
        for item in listdir(str(eg_path / subdir)):
            loc = eg_path / subdir / item
            if loc.is_dir():
                _data = _get_eg_doc(
                    loc,
                    "https://github.com/VUnit/vunit/tree/master/examples/%s/%s"
                    % (subdir, item),
                )
                if _data:
                    egs_fptr.write(_data)


def _get_eg_doc(location: Path, ref):
    """
    Reads the docstring from a run.py file and rewrites the title to make it a ref
    """
    nstr = str(location.name)

    if not (location / "run.py").is_file():
        print(
            "WARNING: Example subdir '"
            + nstr
            + "' does not contain a 'run.py' file. Skipping..."
        )
        return None

    print("Generating '_main.py' from 'run.py' in '" + nstr + "'...")
    with (location / "run.py").open("r") as ifile:
        with (location / "_main.py").open("w") as ofile:
            ofile.writelines(["def _main():\n"])
            ofile.writelines(["".join(["    ", x]) for x in ifile])

    print("Extracting docs from '" + nstr + "'...")
    sys.path.append(str(location))
    from _main import _main  # pylint: disable=import-error,import-outside-toplevel

    eg_doc = inspect.getdoc(_main)
    del sys.modules["_main"]
    sys.path.remove(str(location))
    remove(str(location / "_main.py"))

    if not eg_doc:
        print(
            "WARNING: 'run.py' file in example subdir '"
            + nstr
            + "' does not contain a docstring. Skipping..."
        )
        return ""

    title = "`%s <%s/>`_" % (eg_doc.split("---", 1)[0][0:-1], ref)
    return "\n".join([title, "-" * len(title), eg_doc.split("---\n", 1)[1], "\n"])
