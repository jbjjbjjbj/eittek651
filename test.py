import doctest
import pkgutil
import unittest

import antenna_diversity


def load_tests(loader, tests, pattern):
    path = antenna_diversity.__path__
    name = antenna_diversity.__name__ + '.'
    walker = pkgutil.walk_packages(path, name)
    for importer, name, ispkg in walker:
        tests.addTests(doctest.DocTestSuite(name))
    return tests


if __name__ == "__main__":
    unittest.main()
