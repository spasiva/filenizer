#!/usr/bin/python
#
# Copyright (C) 2017 Łukasz Kopacz
#
# This file is part of Filenizer.
#
# Filenizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Filenizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Filenizer. If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.1"

import shutil
import os
import argparse
import re


def add_zero(num):
    if num < 10:
        return "0" + str(num)
    return str(num)


def sim_name(fn, title):

    fn_re = re.compile(r'\d+')
    numbers = fn_re.findall(fn)

    if len(numbers) > 1:
        new_file_name = ("{} - S{}E{}{}".format(
            title,
            add_zero(int(numbers[0])),
            add_zero(int(numbers[1])),
            os.path.splitext(fn)[1]))  # file extension

        return new_file_name

    return fn


def parsenizer():
    # Command line options
    parser = argparse.ArgumentParser(description='This program helps organise your files.')
    #parser.add_argument('-t', '--title', required=True, help='Title of new file.')
    parser.add_argument('-t', '--title', help='Title of new file.')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursive output. Keeps original structure of folders.')
    parser.add_argument('-o', '--output', help='Location of output.')
    parser.add_argument('-i', '--input', help='Location of input.')
    parser.add_argument('--ignore', help='Ignored folders. Use comma to add multiple folders.')
    parser.add_argument('--ignore-file', help='Ignored files. Use comma to add multiple files.')
    args = parser.parse_args()
    parameters = vars(args)

    return parameters


def modifynizer(parameters):
    print(parameters)
    '''
    if not os.path.isdir(self.tv_input.get()):
        print(self.tv_input.get())
        self.label_info['text'] = 'Wrong input directory.'
    elif not os.path.isdir(self.tv_output.get()):
        print(self.tv_output.get())
        self.label_info['text'] = 'Wrong output directory.'
    else:
        print('ok')
    '''
    # Creates input folder
    if parameters['input']:
        input_dir = os.path.abspath(parameters['input'])
    else:
        input_dir = os.path.abspath('.')
    if not os.path.isdir(input_dir):
        return "Wrong input directory."

    # Creates output folder
    if parameters['output']:
        output_dir = parameters['output']
    else:
        output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Ignore folders
    exclude = {os.path.abspath(output_dir), os.path.abspath('.idea')}
    if parameters['ignore']:
        for ign_fol in parameters['ignore']:
            exclude.add(os.path.abspath(ign_fol))

    # Start walking
    for folder_name, subfolders, filenames in os.walk(input_dir, topdown=True):
        folder_name = os.path.abspath(folder_name)
        subfolders[:] = [d for d in subfolders if os.path.abspath(d) not in exclude]

        # Creates recursive folders
        print('Folder: "{}"'.format(folder_name))
        #if parameters['recursive']:
        #    os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)

        for filename in filenames:
            # Ignore '.py' files
            if filename.endswith('.py'):
                continue

            if filename in parameters['ignore_file']:
                continue

            # Source path
            src_path = os.path.join(folder_name, filename)

            # Edit file name
            if parameters['title']:
                filename = sim_name(filename, parameters['title'])

            # Destination path
            if parameters['recursive']:
                dst_path = os.path.join(output_dir, folder_name[len(input_dir)+1:])
                os.makedirs(dst_path, exist_ok=True)
                dst_path = os.path.join(dst_path, filename)
            else:
                dst_path = os.path.join(output_dir, filename)

            # Checking for duplicates & changing name of duplicates
            if os.path.isfile(dst_path):
                base, extension = os.path.splitext(dst_path)
                file_num = 2
                while os.path.isfile('{}_{}{}'.format(base, file_num, extension)):
                    file_num += 1
                dst_path = '{}_{}{}'.format(base, file_num, extension)

            # Copying
            print('    Copying "{}" to "{}"'.format(src_path, dst_path))
            shutil.copy(src_path, dst_path)
    return "Done."


if __name__ == "__main__":
    print(modifynizer(parsenizer()))
