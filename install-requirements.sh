#!/bin/bash

test -e parsi_io || git clone https://github.com/language-ml/parsi.io.git parsi_io
cd parsi_io
git pull
touch __init__.py
cd ..
