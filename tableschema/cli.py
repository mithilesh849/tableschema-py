# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import io
import sys
import json
import click
import tableschema
from . import config


# Module API

@click.group(help='')
def cli():
    """Command-line interface

    ```
    Usage: tableschema [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      infer     Infer a schema from data.
      info      Return info on this version of Table Schema
      validate  Validate that a supposed schema is in fact a Table Schema.
    ```

    """
    pass


@cli.command()
def info():
    """Return info on this version of Table Schema"""
    click.echo(json.dumps({'version': config.VERSION}, ensure_ascii=False, indent=4))


@cli.command()
@click.argument('data')
@click.option('--row_limit', default=100, type=int)
@click.option('--confidence', default=0.75, type=float)
@click.option('--encoding', default='utf-8')
@click.option('--to_file')
def infer(data, row_limit, confidence, encoding, to_file):
    """Infer a schema from data.

    - data must be a local filepath
    - data must be CSV
    - the file encoding is assumed to be UTF-8 unless an encoding is passed
      with --encoding
    - the first line of data must be headers
    - these constraints are just for the CLI

    """
    descriptor = tableschema.infer(data,
                                   encoding=encoding,
                                   limit=row_limit,
                                   confidence=confidence)
    if to_file:
        with io.open(to_file, mode='w+t', encoding='utf-8') as dest:
            dest.write(json.dumps(descriptor, ensure_ascii=False, indent=4))
    click.echo(descriptor)


@cli.command()
@click.argument('schema')
def validate(schema):
    """Validate that a supposed schema is in fact a Table Schema."""
    try:
        tableschema.validate(schema)
        click.echo("Schema is valid")
        sys.exit(0)
    except tableschema.exceptions.ValidationError as exception:
        click.echo("Schema is not valid")
        click.echo(exception.errors)
        sys.exit(1)
