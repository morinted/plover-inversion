#!/usr/bin/env python
"""
Python 3 script to create a .json dictionary of inverted numbers for
stenography / Plover's number bar.
"""


def make_sequences(char_list):
    # Final result of all possible combos of numbers
    result = []

    # The numbers that have been iterated over
    singles = []

    for number in char_list:
        new_entries = []
        for article in result + singles:
            new_entries.append(article + number)
        result.extend(new_entries)
        singles.append(number)
    return result


def get_stroke_output_pairs(left_hand, right_hand,
                            left_hand_seq, right_hand_seq,
                            inversion):
    # Note: String[::-1] reverses the string

    # All left hand reverses
    reverse_left = {(entry + inversion): entry[::-1]
                    for entry in left_hand_seq}

    # All right hand reverses
    reverse_right = {inversion + entry: entry[::-1]
                     for entry in right_hand_seq}

    # Both hands
    reverse_both = dict()
    for stroke, left in reverse_left.items():
        for right in right_hand_seq:
            # stroke is format 123450EU
            # left is format 054321
            # right is format 6789
            # Append right to stroke, prefix reverse right to left
            new_stroke = stroke + right
            new_entry = right[::-1] + left
            reverse_both.update({new_stroke: new_entry})

    # Handle singles
    single_combos = dict()
    for l_char in left_hand:
        for r_stroke, r_entry in reverse_right.items():
            single_combos.update({l_char + r_stroke: r_entry + l_char})
    for r_char in right_hand:
        for l_stroke, l_entry in reverse_left.items():
            single_combos.update({l_stroke + r_char: r_char + l_entry})

    # Jumble them all together, return to mama.
    return dict(reverse_left.items() |
                reverse_right.items() |
                reverse_both.items() |
                single_combos.items())


def json_format_strokes(strokes):
    result = ""
    for stroke, entry in sorted(strokes.items()):
        result = result + json_format_stroke(stroke, entry)
    return wrap_json(result[:-2])


def json_format_stroke(stroke, entry):
    return '  "' + stroke + '": "' + entry + '",\n'


def wrap_json(to_wrap):
    return '{\n' + to_wrap + '\n}'


def write_to_file(to_write, filename):
    f = open(filename, 'w')
    f.write(to_write)


def main():
    left_hand = [
        '1', '2', '3', '4', '5', '0',
    ]
    right_hand = [
        '6', '7', '8', '9',
    ]
    inversion = "EU"
    filename = "inverted.json"
    left_hand_seq = make_sequences(left_hand)
    right_hand_seq = make_sequences(right_hand)
    strokes = get_stroke_output_pairs(left_hand, right_hand, left_hand_seq,
                                      right_hand_seq, inversion)
    write_to_file(json_format_strokes(strokes), filename)

    print("./{} written.".format(filename))


if __name__ == '__main__':
    main()
