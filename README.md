## Ascendant Tools

Ascendant is a superpowered role-playing game of infinite possibilities.

### `demographics.py`

In the book, there is a distribution of Power Levels that Ascendants follow, where progressively more
powerful heroes are exponentially less likely to appear.  This script uses [Inverse transform
sampling](https://en.wikipedia.org/wiki/Inverse_transform_sampling) to randomly determine how many
Ascendants at each Power Level appear in a given population.

#### Usage

```
$ ./demographics.py --help
Usage: demographics.py [OPTIONS]

Options:
  -p, --population INTEGER  Population to draw from (default 1,000,000)
  --expected_pop            Don't randomize the total number of Ascendants.
  --seed TEXT               Override the RNG seed.
  --help                    Show this message and exit.

$ ./demographics.py
There are 88 expected Ascendants in a population of 1,000,000.
Using the approximate binomial distribution to get number of Ascendants.

PL     Count
15     53
16     18
17     13
18     8
19     1
20     3
Total  96

Seed   133322
```

#### Requirements

Python 3 and [click](https://pypi.org/project/click).  I tested click versions '7.1.2' and '8.0.1', but it's likely to work with many other versions.

### Copyright information

Ascendant is Copyright Autarch LLC.
