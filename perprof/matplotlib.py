"""
This handle the plot using matplotlib.
"""

import os.path
import gettext
import matplotlib.pyplot as plt
from . import prof

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation('perprof',
        os.path.join(THIS_DIR, 'locale'))
_ = THIS_TRANSLATION.gettext

class Profiler(prof.Pdata):
    def __init__(self, setup):
        if setup.get_output() is None:
            self.output = 'performance-profile.png'
        else:
            self.output = '{}.{}'.format(setup.get_output(),
                    setup.get_output_format())
        self.output_format = setup.get_output_format()

        # Language for the axis label
        translation = gettext.translation('perprof',
                os.path.join(THIS_DIR, 'locale'), [setup.lang])
        self.axis_lang = translation.gettext

        prof.Pdata.__init__(self, setup)

    def plot(self):
        if not self.force:
            try:
                file_ = open(self.output, 'r')
                file_.close()
                raise ValueError(_('ERROR: File {} exists.\nUse `-f` to overwrite').format(self.output))
            except FileNotFoundError:
                pass

        if not self.already_scaled:
            self.scale()

        try:
            self.ppsbt
        except AttributeError:
            self.set_percent_problems_solved_by_time()

        # Hack need to background color
        figure_ = plt.figure()
        plot_ = figure_.add_subplot(111)

        # Set configurations handle when saving the plot
        save_configs = {}
        save_configs['format'] = self.output_format

        if self.background:
            plot_.set_axis_bgcolor((self.background[0] / 255,
                    self.background[1] / 255,
                    self.background[2] / 255))
        if self.page_background:
            # RGB tuples must be in the range [0,1]
            save_configs['facecolor'] = (self.page_background[0] / 255,
                    self.page_background[1] / 255,
                    self.page_background[2] / 255)
        if not self.background and not self.page_background:
            save_configs['transparent'] = True
            save_configs['frameon'] = False

        # We need to hold the plots
        plot_.hold(True)
        # Generate the plot for each solver
        for solver in self.solvers:
            plot_.plot(self.times, self.ppsbt[solver], label=solver)

        # Change the xscale to log scale
        if self.semilog:
            plt.gca().set_xscale('log')

        # Axis
        try:
            maxt = min(max(self.times), self.tau)
        except (AttributeError, TypeError):
            maxt = max(self.times)
        plt.gca().set_xlim(1, maxt)
        plt.gca().set_xlabel(self.axis_lang('Performance Ratio'))
        plt.gca().set_ylim(0, 1)
        plt.gca().set_ylabel(self.axis_lang('Problems solved'))

        # Legend
        plt.gca().legend(loc=4)

        # Help lines
        plt.gca().grid(axis='y', color='0.5', linestyle='-')

        # Save the plot
        plt.savefig(self.output, bbox_inches='tight', pad_inches=0.05,
                **save_configs)
