# Bookworm Solver

Bookworm is a flash game in which the player searches for words on a board, similarly to Boggle.
This package provides a CLI with which one can find the longest word by supplying the board tiles.
Unfortunately the wordlist used does not exactly match the one Bookworm uses. Should you change the [words](words) file, you need to rerun the [wordtree_maker.py](wordtree_maker) script.

## Getting Started

### Prerequisites

This package is written in Python 3. It has been tested under version 3.6.4.
Code for integration testing is written in bash, version 4.4.19.

### Installing

All files should be downloaded to a single folder. As all outputs from scripts are included, no additional commands need to be run.

## Running the tests

All directions from here on assume that your current working directory is the `Bookworm Solver` folder.
Simply run `bash inttests.sh` for the integration tests. Additional tests can be added to the `tests` folder with the filename in the form of `test[0-9]+`, with the matching expected output file `answer[0-9]+`. Please look at the provided answers to see what their formats should be. A success run of the integration tests will output nothing.
Unit tests can be run with the command `python3 unittests.py`.

## The CLI

The CLI can be accessed by running `python3 bookworm_solver.py`. This command will first take a few seconds to process the pickled tree file. Once prompted, you can fill in the board going column-wise, e.g.:

```
Please type the letters of the board column by column separated by spaces:
d y e o p o f
a s n o h u e i
o b d d r e r
i e e e r n n y
l t m q r b m
v n s a u f n i
e a e d n s i
```

Note that "Qu" tiles should be input as "q". The input can be terminated with either an empty line or `ctrl+d`. The corresponding output for the above example is:

```
8
esteemed
[1, 1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 1, 1, 1, 1]
[1, 1, 0, 1, 1, 1, 1]
[1, 0, 0, 0, 1, 1, 1, 1]
[1, 0, 0, 1, 1, 1, 1]
[1, 1, 0, 1, 1, 1, 1, 1]
[1, 1, 0, 1, 1, 1, 1]
```
where `8` is the word length, `esteemed` the word found, and the lists the tiles used. The `0`'s denote the letters that have been used.

## Authors

* **jongyoonl** - *Initial work*

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE.md](LICENSE.md) file for details
