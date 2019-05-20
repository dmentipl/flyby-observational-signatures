#!/usr/bin/env python
'''
flyby-mcfost.py
D. Mentiplay, 2018.

Run mcfost on flyby models.
'''

import glob
import os
import shutil
import subprocess

# ---------------------------------------------------------------------------- #

SETUP = True
RUN = True

PWD = os.path.dirname(os.path.abspath('__file__'))
CONFIG_DIR = (
    os.path.expandvars('$HOME') + '/repos/phd/projects/dusty-discs/flyby'
)
MCFOST_DIR = os.path.expandvars('$MCFOST_DIR')
DUMP_DIR = os.path.expandvars('$HOME') + '/runs/dusty-discs/flyby'

LIMITS = PWD + '/flyby-limits'
MCFOST = PWD + '/mcfost'

BETA = ['45', '135']
TIME = ['100', '110', '120', '150']
INCLINATION = ['00', '45', '90']
WAVELENGTH = ['1.6', '850', '2100']
MOLECULE = ['CO']

# ---------------------------------------------------------------------------- #

if SETUP:

    shutil.copy2(CONFIG_DIR + '/flyby-limits', PWD)
    shutil.copy2(MCFOST_DIR + '/src/mcfost', PWD)

    for inclination in INCLINATION:
        paras = [
            CONFIG_DIR + '/flyby-temperature.para',
            CONFIG_DIR + '/flyby-alma-i' + inclination + '.para',
            CONFIG_DIR + '/flyby-scat-i' + inclination + '.para',
        ]
        for para in paras:
            shutil.copy2(para, PWD)

    for beta in BETA:
        for time in TIME:

            for inclination in INCLINATION:
                DIR = PWD + '/b' + beta + '/t' + time + '/i' + inclination
                os.makedirs(DIR)

            dump = DUMP_DIR + '/b' + beta + '-' + time + '_'
            shutil.copy2(dump, PWD)

# ---------------------------------------------------------------------------- #

if RUN:

    if not os.path.isfile(MCFOST):
        raise FileNotFoundError

    for beta in BETA:
        for time in TIME:

            DUMP_FILE = 'b' + beta + '-' + time + '_'
            DUMP = DUMP_DIR + '/' + DUMP_FILE

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
            PARA = PWD + '/' + PARA_FILE

            message = 'Calculating temperature'
            print(3 * '\n' + '---- ' + message + ' ----' + 3 * '\n', flush=True)

            LOG_FILE = DUMP_FILE + 'th.log'
            LOG = PWD + '/' + LOG_FILE
            ROOT_DIR = 'b' + beta + '/t' + time

            MCFOST_COMMAND = (
                MCFOST
                + ' '
                + PARA
                + ' -phantom '
                + DUMP
                + ' -limits '
                + LIMITS
                + ' | tee '
                + LOG
            )

            subprocess.run(MCFOST_COMMAND, shell=True)

            # --- thermal emission / scattered light --- #

            for inclination in INCLINATION:

                message = 'Inclination is ' + inclination + ' degrees'
                print(
                    3 * '\n' + '---- ' + message + ' ----' + 3 * '\n',
                    flush=True,
                )

                DIR_INC = ROOT_DIR + '/i' + inclination

                for wavelength in WAVELENGTH:

                    message = 'Calculating image at ' + wavelength + ' µm'
                    print(
                        3 * '\n' + '---- ' + message + ' ----' + 3 * '\n',
                        flush=True,
                    )

                    LOG_FILE = (
                        DUMP_FILE
                        + 'i'
                        + inclination
                        + '_'
                        + wavelength
                        + '.log'
                    )
                    LOG = PWD + '/' + LOG_FILE

                    if float(wavelength) < 10.0:
                        PARA = 'flyby-scat-i' + inclination + '.para'
                        CASA = ''
                        IGNORE_DUST = '-ignore_dust'
                    else:
                        PARA = 'flyby-scat-i' + inclination + '.para'
                        CASA = '-casa'
                        IGNORE_DUST = ''

                    MCFOST_COMMAND = (
                        MCFOST
                        + ' '
                        + PARA
                        + ' -phantom '
                        + DUMP
                        + ' -limits '
                        + LIMITS
                        + ' -img '
                        + wavelength
                        + ' '
                        + CASA
                        + ' '
                        + IGNORE_DUST
                        + ' | tee '
                        + LOG
                    )

                    subprocess.run(MCFOST_COMMAND, shell=True)

                    shutil.move('data_' + wavelength, DIR_INC)

            shutil.move('data_th', ROOT_DIR)

            # --- molecular emission --- #

            for inclination in INCLINATION:

                message = 'Inclination is ' + inclination + ' degrees'
                print(
                    3 * '\n' + '---- ' + message + ' ----' + 3 * '\n',
                    flush=True,
                )

                DIR_INC = ROOT_DIR + '/i' + inclination

                for molecule in MOLECULE:

                    message = 'Calculating ' + molecule + ' emission'
                    print(
                        3 * '\n' + '---- ' + message + ' ----' + 3 * '\n',
                        flush=True,
                    )

                    LOG_FILE = (
                        DUMP_FILE + 'i' + inclination + '_' + molecule + '.log'
                    )
                    LOG = PWD + '/' + LOG_FILE

                    PARA = 'flyby-alma-i' + inclination + '.para'
                    CASA = '-casa'
                    IGNORE_DUST = '-ignore_dust'

                    MCFOST_COMMAND = (
                        MCFOST
                        + ' '
                        + PARA
                        + ' -phantom '
                        + DUMP
                        + ' -limits '
                        + LIMITS
                        + ' -mol '
                        + CASA
                        + ' '
                        + IGNORE_DUST
                        + ' | tee '
                        + LOG
                    )

                    subprocess.run(MCFOST_COMMAND, shell=True)

                    shutil.move('data_' + molecule, DIR_INC)
                    shutil.move('data_th', DIR_INC + '/data_th_' + molecule)

                    for file in glob.glob(r'*.tmp'):
                        shutil.move(file, DIR_INC + '/data_th_' + molecule)
