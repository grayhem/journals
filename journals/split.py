"""
it will overwrite the output directory.
usage:
    python3 split.py whatever_file /path/to/output
"""

import sys

from pathlib import Path


SPLIT_ON = "--------\n"


def date_to_filename(base_path, raw_date_string):
    """
    given some date like MONTH/DAY/YEAR, make a filename like base_path/YEAR/MONTH/DAY.md
    """
    raw_date_string = raw_date_string[:-1]
    month, day, year = raw_date_string.split("/")
    relative_path = "{}/{}/{}.md".format(year, month, day)
    return base_path / relative_path



def main(target, output_dir):
    """

    """

    # make the top level output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # load the file
    with open(target, 'r') as the_file:
        lines = [l for l in the_file.readlines()]
    print(len(lines))
    # read lines into files
    last_line = lines[0]
    output_file = None
    for this_line in lines[1:]:
        if this_line == SPLIT_ON:
            if output_file is not None:
                output_file.close()
            date = last_line
            filename = date_to_filename(output_path, date)
            print(filename)
            # make the path up to here if necessary
            parent_dir = filename.parent
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True)
            # make this the file we write to now
            output_file = filename.open('w')
        else:
            if output_file is not None:
                output_file.write(last_line)
        last_line = this_line
    output_file.write(last_line)
    output_file.close()

if __name__ == '__main__':
    target = sys.argv[1]
    output_dir = sys.argv[2]
    main(target, output_dir)
