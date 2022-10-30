# anonymous anonymous 2020
# coral_pytorch
# Author: anonymous anonymous <sebastiananonymous.com>
#
# License: MIT
import argparse


def parse_cmdline_args(parser=None):

    if parser is None:
        parser = argparse.ArgumentParser()

    parser.add_argument('--outpath',
                        type=str,
                        required=True)

    parser.add_argument('--cuda',
                        type=int,
                        default=-1)

    parser.add_argument('--seed',
                        type=int,
                        default=0)

    parser.add_argument('--numworkers',
                        type=int,
                        default=3)

    parser.add_argument('--save_models',
                        type=str,
                        choices=['true', 'false'],
                        default='false')

    parser.add_argument('--learningrate',
                        type=float,
                        default=0.0005)

    parser.add_argument('--batchsize',
                        type=int,
                        default=64)

    parser.add_argument('--epochs',
                        type=int,
                        default=100)

    parser.add_argument('--optimizer',
                        type=str,
                        choices=['sgd', 'adam'],
                        default='adam')

    parser.add_argument('--scheduler',
                        type=str,
                        choices=['true', 'false'],
                        default='false')

    parser.add_argument('--dataset',
                        type=str,
                        choices=['mnist', 'morph2', 'morph2-balanced', 'aes', 'fireman'],
                        default='mnist')

    parser.add_argument('--skip_train_eval',
                        type=str,
                        choices=['true', 'false'],
                        default='true')

    parser.set_defaults(feature=True)
    args = parser.parse_args()

    d = {'true': True,
         'false': False}

    args.skip_train_eval = d[args.skip_train_eval]
    args.scheduler = d[args.scheduler]
    args.save_models = d[args.save_models]

    return args
