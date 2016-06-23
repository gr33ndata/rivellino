import sys
import time

from argparse import ArgumentParser

from ruleset import RulesEngine

class ETL:

    def __init__(self):

        self.re = RulesEngine()

    def list(self):
        print ''
        print 'There are {0} existing rules:'.format(len(self.re))
        for rule in self.re:
            print '> {0}\n  {1} [{2} rule]'.format(
                rule['rule_name'],
                rule['rule_description'],
                rule['rule_type']
            )
        print ''

    def run(self, rule_name=''):
        if rule_name:
            self.re.apply_rule_by_name(rule_name)
        else:
            self.re.apply_rules()


def parse_cli():

    parser = ArgumentParser(description='BidX ETL Tool')
    parser.add_argument(
        '-p', '--profiling', 
        action='store_true', 
        help='Print stats about ETL performance'
    )
    parser.add_argument(
        '-l', '--list', 
        action='store_true', 
        help='List all existing rules'
    )
    parser.add_argument(
        '-r', '--run', 
        nargs='?', default=False, const='all', 
        metavar='rule_name.yml',
        help='Run all rules, or a specific rule by name'
    )

    return parser.parse_args()

def main(args):

    #print args
    if args.list:
        e = ETL()
        e.list()
    elif args.run:
        e = ETL()
        rule_name = '' if args.run == 'all' else args.run
        e.run(rule_name)
    else:
        parser.print_help()
        sys.exit('\n')

def main_profiled(args):
    time_start = time.time()
    main(args)
    time_delta = time.time() - time_start
    print("--- %s seconds to finish ---" % round(time_delta, 2)) 

if __name__ == '__main__':

    try:
        args = parse_cli()
        if args.profiling:
            main_profiled(args)
        else:
            main(args)
    except Exception, e:
        print "Failed to run!"
        raise



