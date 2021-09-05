#!/usr/bin/env python

from collections import Counter
from math import log
from random import random as rng
import random
from datetime import datetime

import click

# From the sum of the populations in the Ascendant RPG book.
ASCENDANT_FRACTION = 8.81e-05

# Magic numbers to get to the distribution to match the book.
LAMBDA = 0.8047189572  # https://en.wikipedia.org/wiki/Inverse_transform_sampling
MINIMUM_PL = 15

# https://en.wikipedia.org/wiki/Binomial_distribution#Normal_approximation
BINOMIAL_APPROXIMATION = 9 * (1 - ASCENDANT_FRACTION) / ASCENDANT_FRACTION


def generate_pl():
    return int(-log(1 - rng()) / LAMBDA) + MINIMUM_PL


@click.command()
@click.option(
    "-p",
    "--population",
    default=1000000,
    type=int,
    help="Population to draw from (default 1,000,000)",
)
@click.option(
    "--expected_pop",
    is_flag=True,
    help="Don't randomize the total number of Ascendants.",
)
@click.option(
    "-a",
    "--ascendants",
    default=None,
    type=int,
    help="Genrate a number of Ascendants instead of a population.",
)
@click.option("--seed", default=None, help="Override the RNG seed.")
def generate(population, expected_pop, ascendants, seed):
    if seed is None:
        time = datetime.now()
        seed = time.hour * 10000 + time.minute * 100 + time.second
    random.seed(seed)

    if ascendants is None:
        ascendants = round(ASCENDANT_FRACTION * population)
        click.echo(
            f"There are {ascendants:,} expected Ascendants in a population of {population:,}."
        )
        if expected_pop:
            click.echo("Using the expected population.")
        elif population < BINOMIAL_APPROXIMATION:
            click.echo("Rolling for each person to get number of Ascendants.")
            ascendants = sum(1 for _ in range(population) if rng() <= ASCENDANT_FRACTION)
        else:
            click.echo(
                "Using the approximate binomial distribution to get number of Ascendants."
            )
            np = population * ASCENDANT_FRACTION
            sigma = (np * (1 - ASCENDANT_FRACTION)) ** 0.5
            ascendants = round(random.normalvariate(np, sigma))
    else:
        click.echo(f"Generating exactly {ascendants} Ascendants.")

    results = Counter(generate_pl() for _ in range(ascendants))
    keys = sorted(list(results))

    click.echo("\nPL     Count")
    for key in keys:
        click.echo(f"{key}     {results[key]:,}")
    click.echo(f"Total  {sum(results.values()):,}")

    click.echo(f"\nSeed   {seed}")


if __name__ == "__main__":
    generate()
