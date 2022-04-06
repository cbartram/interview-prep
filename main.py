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
    current_sequence = []
    for i, begin_split in enumerate(aggregate_log.split("BEGIN")):
        begin_split = begin_split.replace(" ", "_") \
            .replace("\n", "")
        end_valid_sequence = begin_split.endswith("END") or begin_split.endswith("END_")
        if "_N_" in begin_split or "_Y_" in begin_split:
            current_sequence.append(begin_split)
        if end_valid_sequence:
            # It is the end of a valid sequence because we are splitting by BEGIN
            valid_sequences.append(current_sequence)
            current_sequence = []
    # For each valid sequence join it all together (since we know its 1 sequence) and parse out any END's
    for sequence in valid_sequences:
        joined = "".join(sequence)
        joined = joined.replace("_END_", "") \
            .replace("_END", "")\
            .replace("_", "")

        # Will be left with YYYYNNYNYNYYN
        print(" ".join(joined))
        response.append(find_best_closing_time(" ".join(joined)))
    return response


def find_best_closing_time(store_log: str) -> int:
    closing_penalties = []
    list_log = store_log.split(" ")

    for hour in range(0, len(list_log)):  # Produces [0, 1, 2, 3, 4]
        closing_penalties.append((hour, compute_penalty(store_log, hour)))

    return min(closing_penalties, key=lambda n: n[1])[0]


def compute_penalty(store_log: str, closing_time: int) -> int:
    if not store_log or closing_time < 0:
        raise Exception("Closing time must be greater than 0 and the store log must contain valid values of Y and N.")

    list_log = store_log.split(" ")

    if closing_time == 0:
        filtered_list = list(filter(lambda hour: hour.upper() == "Y", list_log))
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


if __name__ == "__main__":
    assert compute_penalty("Y Y N Y", 4) == 1
    assert find_best_closing_time("Y Y", )

    print(get_best_closing_times("BEGIN Y Y END \nBEGIN N N END"))
    assert get_best_closing_times("BEGIN Y Y END \nBEGIN N N END") == [2, 0]
    print("-----------------------------")
    assert get_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END") == [2]
    print("-----------------------------")
    assert get_best_closing_times("BEGIN N N END BEGIN Y Y\n END BEGIN Y N END") == [0, 2, 1]
    print("-----------------------------")
    assert get_best_closing_times("BEGIN N N END BEGIN Y Y\n BEGIN BEGIN N N END") == [0, 2]
