# quteconf\_utils

## Overview

This is a helper library for configuring
[qutebrowser](https://www.qutebrowser.org/). Currently, it only provides
facilities for loading YAML data. It's also probably slow as shit.

## Installation

You can either

* initialize this repo as a submodule (if it's controlled by git already).
* clone it.

Not very elegant, I know, but it gets the job done. This is way too niche to upload to PyPI.

## Usage

In your `config.py` file:

```python
import quteconf_utils as qc
qc.init(c, config)

qc.load_from_yaml('<your .yaml file>')

# Repeat for all your YAML files.
```

This will set values in `config` according to the YAML file provided.

## Features

You may use `+X(<color>)` as a YAML value. This will load a color from `xrdb`.
You may also use `$<config value>`. This will substitute a config value.

## Other notes

idk
