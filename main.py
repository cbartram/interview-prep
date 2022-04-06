import re
# compute_penalty("Y Y N Y", 0) should return 3
# compute_penalty("N Y N Y", 2) should return 2
# compute_penalty("Y Y N Y", 4) should return 1

## Examples ##

# get_best_closing_times("BEGIN Y Y END \nBEGIN N N END")
#   should return an array: [2, 0]

# get_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END")
#   should return an array: [2]

# get_best_closing_times("BEGIN N N END BEGIN Y Y\n END BEGIN N N END")
#   should return an array: [0, 2, 0]

# get_best_closing_times("BEGIN N N END BEGIN Y Y\n BEGIN BEGIN N N END")
#   should return an array: [0, 2]


def get_best_closing_times(aggregate_log: str) -> list:
    response = []
    valid_sequences = []
    for begin_split in aggregate_log.split("BEGIN"):
        begin_split = begin_split.replace(" ", "_") \
            .replace("\n", "")
        is_valid_sequence = "_END" in begin_split
        if ("_N_" in begin_split or "_Y_" in begin_split) and is_valid_sequence:
            first_end_occurrence = [m.start() for m in re.finditer("END", begin_split)][0]
            current_sequence = "".join(begin_split[0:first_end_occurrence])
            valid_sequences.append(current_sequence)

    print(valid_sequences)
    for sequence in valid_sequences:
        joined = "".join(sequence).replace("_", " ").strip()
        response.append(find_best_closing_time(joined))
    return response


def find_best_closing_time(store_log: str) -> int:
    closing_penalties = []
    list_log = store_log.split(" ")

    for hour in range(0, len(list_log) + 1):  # Produces [0, 1, 2, 3, 4]
        closing_penalties.append((hour, compute_penalty(store_log, hour)))

    return min(closing_penalties, key=lambda n: n[1])[0]


def compute_penalty(store_log: str, closing_time: int) -> int:
    if not store_log or closing_time < 0:
        raise Exception("Closing time must be greater than 0 and the store log must contain valid values of Y and N.")

    list_log = store_log.split(" ")

    if closing_time == 0:
        filtered_list = list(filter(lambda h: h.upper() == "Y", list_log))
        return len(filtered_list)

    penalty = 0

    # Split the list based on the index (closing_time)
    # evaluate the first half of the list looking for N's
    # evaluate the second half of the list looking for Y's
    open_half = list_log[0:closing_time]
    closing_half = list_log[closing_time::]

    for hour in open_half:
        if hour.upper() == "N":
            penalty += 1

    for hour in closing_half:
        if hour.upper() == "Y":
            penalty += 1

    return penalty


def run_asserts():
    assert compute_penalty("Y Y N Y", 4) == 1
    assert find_best_closing_time("Y Y") == 2
    assert get_best_closing_times("BEGIN Y Y END \nBEGIN N N END") == [2, 0]
    print("-----------------------------")
    assert get_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END") == [2]
    print("-----------------------------")
    assert get_best_closing_times("BEGIN N N END BEGIN Y Y\n END BEGIN Y N END") == [0, 2, 1]
    print("-----------------------------")
    assert get_best_closing_times("BEGIN N N END BEGIN Y Y\n BEGIN BEGIN N N END") == [0, 0]


if __name__ == "__main__":
    assert compute_penalty("Y Y N Y", 4) == 1
    assert find_best_closing_time("Y Y") == 2

    print(get_best_closing_times("BEGIN Y Y END \nBEGIN N N END"))
    print("-----------------------------")
    get_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END")
    print("-----------------------------")
    get_best_closing_times("BEGIN N N END BEGIN Y Y\n END BEGIN Y N END")
    print("-----------------------------")
    get_best_closing_times("BEGIN N N END BEGIN Y Y\n BEGIN BEGIN N N END")

    run_asserts()
