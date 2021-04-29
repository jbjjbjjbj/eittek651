#!/usr/bin/env python
# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
import doctest
import pkgutil
import unittest

import antenna_diversity
from mypy import api


def load_tests(loader, tests, pattern):
    path = antenna_diversity.__path__
    name = antenna_diversity.__name__ + '.'
    walker = pkgutil.walk_packages(path, name)

    tests.addTests(loader.discover('test'))

    for importer, name, ispkg in walker:
        tests.addTests(doctest.DocTestSuite(name))
        pass
    return tests


if __name__ == "__main__":
    print("Running mypy")
    print(api.run(["antenna_diversity", "examples"])[0])

    print("Running unittest")
    unittest.main()

