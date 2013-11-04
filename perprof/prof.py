"""
The functions related with the perform (not the output).
"""

from . import parse

def load_data(setup):
    """
    Load the data.

    :param setup: the setup configurations
    :type setup: main.PerProfSetup
    """
    data = {}
    for f in setup.get_files():
        data[f] = parse.parse_file(f)
    return data

class Pdata:
    def __init__(self, setup):
        self.data = load_data(setup)

    def __repr__(self):
        try:
            self.solvers
        except:
            self.get_set_solvers()
        try:
            self.problems
        except:
            self.get_set_problems()

        for s in self.solvers:
            print('{:>8}'.format(s), end='  ')
        print()

        for p in self.problems:
            print('{:>8}'.format(p), end='  ')
            for s in self.solvers:
                print('{:8.4}'.format(self.data[s][p][1]), end='  ')
            print()

        return ''

    def get_set_solvers(self):
        try:
            self.solvers
        except:
            self.solvers = self.data.keys()
        return self.solvers

    def get_set_problems(self):
        try:
            self.problems
        except:
            p = set()
            for i in self.data.keys():
                for j in self.data[i].keys():
                    p.add(j)
            self.problems = p
        return self.problems

    def scale(self):
        """
        Scale time.
        """
        try:
            self.solvers
        except:
            self.get_set_solvers()
        try:
            self.problems
        except:
            self.get_set_problems()

        for p in self.problems:
            min_time = float('inf')
            for s in self.solvers:
                if self.data[s][p][1] < min_time:
                    min_time = self.data[s][p][1]
            for s in self.solvers:
                self.data[s][p][1] = self.data[s][p][1] / min_time