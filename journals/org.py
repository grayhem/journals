"""
reorganize the journal file into a .org with headings representing year, month, day etc. 
"""

import sys
from pathlib import Path



SPLIT_ON = "--------\n"


def date_to_key_triple(raw_date_string):
    """
    return a 3-tuple of keys into the dictionary where the associated text should go
    """
    raw_date_string = raw_date_string[:-1]  
    month, day, year = raw_date_string.split("/")
    return year, month, day
 

def main(in_filename, out_filename):
    """
    etc
    """
    in_path = Path(in_filename)
    out_path = Path(out_filename)
    
    # load the file
    with in_path.open('r') as the_file:
        lines = [l for l in the_file.readlines()]

    the_dictionary = {}

    def insert(key_triple, value):
        """
        put the entry in there
        """
        # can't think of a less-cute way to exclude the date, sorry. the journal format i've been
        # using this whole time is weird.
        value[0] = ""
        value.append("\n")
        value = "\t".join(value)
        if key_triple[0] not in the_dictionary:
            the_dictionary[key_triple[0]] = {}
        if key_triple[1] not in the_dictionary[key_triple[0]]:
            the_dictionary[key_triple[0]][key_triple[1]] = {}
        the_dictionary[key_triple[0]][key_triple[1]][key_triple[2]] = value

    # read lines into the accumulator and dump into the dictionary
    last_line = lines[0]
    entry_accumulator = None
    this_key = None
    for this_line in lines[1:]:
        if this_line == SPLIT_ON:
            # dump the last entry into the dictionary
            if this_key is not None:
                insert(this_key, entry_accumulator)
            # update the date
            date = last_line
            this_key = date_to_key_triple(date)
            entry_accumulator = [] 
        else:
            if entry_accumulator is not None and last_line != "\n":
                entry_accumulator.append(last_line) 
            last_line = this_line
    insert(this_key, entry_accumulator)

    # crawl through the dictionary and write entries to the org file
    with out_path.open('w') as the_file:
        for this_year_number, this_year_entries in the_dictionary.items():
            the_file.write("* " + this_year_number + "\n")
            for this_month_number, this_month_entries in this_year_entries.items():
                the_file.write("** " + this_month_number + "\n")
                for this_day_number, this_day_entry in this_month_entries.items():
                    the_file.write("*** " + this_day_number + "\n")
                    the_file.write(this_day_entry)



if __name__ == '__main__':
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    main(in_filename, out_filename)












