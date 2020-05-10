#!/usr/bin/python3

# This file is managed by `git_helper`. Don't edit it directly

import platform
import rst2txt
import sys
from docutils.core import publish_file
from io import StringIO

from __pkginfo__ import (
	author, long_description, conda_description, extras_require, install_requires, modname, project_urls, repo_root, short_desc, VERSION,
	web,
	)

recipe_dir = repo_root / "conda"

if not recipe_dir.exists():
	recipe_dir.mkdir()

# TODO: entry_points, manifest

all_requirements = install_requires[:]

if isinstance(extras_require, dict):
	for requires in extras_require.values():
		all_requirements += requires

all_requirements = set(x.replace(" ", '') for x in set(all_requirements))
requirements_block = "\n".join(f"    - {req}" for req in all_requirements)

# txt_readme = publish_file(source=StringIO(long_description), writer=rst2txt.Writer())
# description_block = "\n".join([line.replace('"', '\\"') for line in txt_readme.split("\n")])
description_block = conda_description.replace('"', '\\"')

with open(recipe_dir / "meta.yaml", "w") as fp:
	fp.write(f"""{{% set name = "{modname}" %}}
{{% set version = "{VERSION}" %}}

package:
  name: "{{{{ name|lower }}}}"
  version: "{{{{ version }}}}"

source:
  url: "https://pypi.io/packages/source/{{{{ name[0] }}}}/{{{{ name }}}}/{{{{ name }}}}-{{{{ version }}}}.tar.gz"

build:
#  entry_points:
#    - {modname} = {modname}:main
#  skip_compile_pyc:
#    - "*/templates/*.py"          # These should not (and cannot) be compiled
  noarch: python
  script: "{{{{ PYTHON }}}} -m pip install . -vv"

requirements:
  build:
    - python
    - setuptools
    - wheel
  host:
    - pip
    - python
{requirements_block}
  run:
    - python
{requirements_block}

test:
  imports:
    - {modname}

about:
  home: "{web}"
  license: "GNU Lesser General Public v3 (LGPLv3)"
  license_family: LGPL
  # license_file: requirements.txt
  summary: "{short_desc}"
  description: "{description_block}"
  doc_url: {project_urls["Documentation"]}
  dev_url: {project_urls["Source Code"]}

extra:
  maintainers:
    - {author}
    - github.com/{{ username }}

""")

print(f"Wrote recipe to {recipe_dir / 'meta.yaml'}")
#
# plat = platform.system().lower()
# arch = platform.architecture()[0][:2]
#
# if plat == "linux":
# 	conda_arch = f"linux-{arch}"
# elif plat == "windows":
# 	conda_arch = f"win-{arch}"
# elif plat == "darwin":
# 	conda_arch = f"osx-{arch}"
# else:
# 	sys.exit(1)
#
# with open(recipe_dir / "conda_arch.sh", "w") as fp:
# 	fp.write(f'#!/bin/bash\necho "{conda_arch}"')
