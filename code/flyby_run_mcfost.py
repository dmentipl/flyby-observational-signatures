#!/usr/bin/env python
"""
Run MCFOST on flyby models.

Daniel Mentiplay, 2018-2019.
"""

import glob
import pathlib
import shutil
import subprocess

# ---------------------------------------------------------------------------- #

SETUP = True
RUN = True

CONFIG_DIR = pathlib.Path('~/repos/flyby/config').expanduser()
MCFOST_DIR = pathlib.Path('~/repos/mcfost').expanduser()
DUMP_DIR = pathlib.Path('~/runs/flyby').expanduser()

OUTPUT_DIR = DUMP_DIR / 'some_output_dir_name'

LIMITS = CONFIG_DIR / 'flyby-limits'
MCFOST = MCFOST_DIR / 'src' / 'mcfost'

BETA = ['45', '135']
TIME = ['100', '110', '120', '150']
INCLINATION = ['00', '45', '90']
WAVELENGTH = ['1.6', '850', '2100']
MOLECULE = ['CO']

# ---------------------------------------------------------------------------- #

if SETUP:

    OUTPUT_DIR.mkdir()
    LOG_DIR = (OUTPUT_DIR / 'logs').mkdir()

    for beta in BETA:
        for time in TIME:
            for inclination in INCLINATION:
                directory = (
                    OUTPUT_DIR / ('b' + beta) / ('t' + time) / ('i' + inclination)
                )
                directory.mkdir(parents=True)

# ---------------------------------------------------------------------------- #

if RUN:

    if not MCFOST.exists():
        raise FileNotFoundError

    for beta in BETA:
        for time in TIME:

            BETA_TIME_DIR = OUTPUT_DIR / ('b' + beta) / ('t' + time)
            CWD = BETA_TIME_DIR

            DUMP_FILE = 'b' + beta + '-' + time + '_'
            DUMP_PATH = DUMP_DIR / DUMP_FILE

            print(3 * '\n')
            print('+' + 20 * '=' + '+', flush=True)
            print('|' + 20 * ' ' + '|', flush=True)
            print(f'|  DUMP = {DUMP_FILE:9}  |', flush=True)
            print('|' + 20 * ' ' + '|', flush=True)
            print('|' + 20 * ' ' + '|', flush=True)
            print('+' + 20 * '=' + '+', flush=True)
            print(3 * '\n')

            # --- temperature --- #

            PARA_FILE = 'flyby-temperature.para'
            PARA_PATH = CONFIG_DIR / PARA_FILE

            message = 'Calculating temperature'
            print(3 * '\n' + '---- ' + message + ' ----' + 3 * '\n', flush=True)

            LOG_FILE = DUMP_FILE + 'th.log'
            LOG_PATH = LOG_DIR / LOG_FILE

            MCFOST_COMMAND = [
                MCFOST,
                PARA_PATH,
                '-phantom',
                DUMP_PATH,
                '-limits',
                LIMITS,
            ]

            subprocess.run(MCFOST_COMMAND, cwd=CWD, stdout=LOG_PATH, stderr=LOG_PATH)

            # --- thermal emission / scattered light --- #

            for inclination in INCLINATION:

                message = 'Inclination is ' + inclination + ' degrees'
                print(3 * '\n' + '---- ' + message + ' ----' + 3 * '\n', flush=True)

                BETA_TIME_INC_DIR = BETA_TIME_DIR / ('i' + inclination)
                CWD = BETA_TIME_INC_DIR

                for wavelength in WAVELENGTH:

                    message = 'Calculating image at ' + wavelength + ' µm'
                    print(3 * '\n' + '---- ' + message + ' ----' + 3 * '\n', flush=True)

                    LOG_FILE = DUMP_FILE + 'i' + inclination + '_' + wavelength + '.log'
                    LOG_PATH = LOG_DIR / LOG_FILE

                    if float(wavelength) < 10.0:
                        PARA = 'flyby-scat-i' + inclination + '.para'
                        CASA = ''
                        IGNORE_DUST = '-ignore_dust'
                    else:
                        PARA = 'flyby-scat-i' + inclination + '.para'
                        CASA = '-casa'
                        IGNORE_DUST = ''

                    MCFOST_COMMAND = [
                        MCFOST,
                        PARA_PATH,
                        '-phantom',
                        DUMP_PATH,
                        '-limits',
                        LIMITS,
                        '-img',
                        wavelength,
                        CASA,
                        IGNORE_DUST,
                    ]

                    subprocess.run(
                        MCFOST_COMMAND, cwd=CWD, stdout=LOG_PATH, stderr=LOG_PATH
                    )

            # --- molecular emission --- #

            for inclination in INCLINATION:

                message = 'Inclination is ' + inclination + ' degrees'
                print(3 * '\n' + '---- ' + message + ' ----' + 3 * '\n', flush=True)

                BETA_TIME_INC_DIR = BETA_TIME_DIR / ('i' + inclination)
                CWD = BETA_TIME_INC_DIR

                for molecule in MOLECULE:

                    message = 'Calculating ' + molecule + ' emission'
                    print(3 * '\n' + '---- ' + message + ' ----' + 3 * '\n', flush=True)

                    LOG_FILE = DUMP_FILE + 'i' + inclination + '_' + molecule + '.log'
                    LOG_PATH = LOG_DIR / LOG_FILE

                    PARA = 'flyby-alma-i' + inclination + '.para'
                    CASA = '-casa'
                    IGNORE_DUST = '-ignore_dust'

                    MCFOST_COMMAND = [
                        MCFOST,
                        PARA_PATH,
                        '-phantom',
                        DUMP_PATH,
                        '-limits',
                        LIMITS,
                        '-mol',
                        CASA,
                        IGNORE_DUST,
                    ]

                    subprocess.run(
                        MCFOST_COMMAND, cwd=CWD, stdout=LOG_PATH, stderr=LOG_PATH
                    )

                    for file in glob.glob(r'*.tmp'):
                        shutil.move(file, BETA_TIME_INC_DIR + '/data_th_' + molecule)
