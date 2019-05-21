from os import path, listdir
from os.path import isfile, join, expanduser


def get_download_path():
    """Returns the path of download folder"""
    return path.join(path.expanduser("~"), "downloads")


def get_downloaded_srt_files(download_path):
    """Returns all .srt files in download_path"""
    return [f for f in listdir(download_path) if isfile(
        join(download_path, f)) and f.endswith(".srt")]


def get_unique_file(srt_files):
    """Gets file_name from user. Checks if this matches a unique file. If true returns the full file_name.
    Else prints appropiate error_msg and returns None"""
    file_name = input(
        "Enter name of .srt file (unique partial name will work)\n-> ")
    matching_files = []
    for file in srt_files:
        if file_name == file:
            return file_name
        elif file_name in file:
            matching_files.append(file)
    if len(matching_files) == 0:
        print('No files found containing name "' + file_name + '"')
    elif len(matching_files) > 1:
        error_msg = "More than one compatible file found. Files found:"
        for file in matching_files:
            error_msg += '\n"' + file + '"'
        print(error_msg)
    else:
        return matching_files[0]
    return None


def is_valid_correction_amount(c_amount, file_name, download_path):
    """Checks if c_amount is a valid correction amount according to specific rules"""
    operator = c_amount[0]
    if operator != "-" and operator != "+":
        print('Operator not recognized. Must be "+" or "-"')
        return False

    c_amount = c_amount[1::]
    if "," in c_amount:
        time_list = c_amount.split(",")
        if int(time_list[0]) > 99 or int(time_list[1]) > 999:
            print("Time not in valid range")
            return False
    else:
        print('"," must be used as separator')
        return False

    if operator == "-":
        with open(download_path + "/" + file_name, "r") as file:
            for i, line in enumerate(file):
                if i == 1:
                    start_time_list = line.split(" --> ")[0].split(":")
                    start_time_list.extend(start_time_list[2].split(","))
                    del start_time_list[2]
                    start_time_list = [int(x) for x in start_time_list]
                    total_time_in_milliseconds = start_time_list[0] * 3600000 + start_time_list[1] * 60000 + \
                        start_time_list[2] * 1000 + start_time_list[3] - (int(time_list[0]) * 1000 + int(time_list[1]))
                    if total_time_in_milliseconds < 0:
                        print(
                            "Subtraction amount will result in negative start value. Invalid")
                        return False
                    break
    return True


def time_correct_file(file_name, download_path):
    """Produces a time-corrected .srt file by performing simple calculations using
    the get_new_time method"""
    c_amount = input(
        "Choose correction amount. Format is -ss,SSS or +ss,SSS\n-> ")
    if not is_valid_correction_amount(c_amount, file_name, download_path):
        return False

    amount = c_amount[1::]
    operation = c_amount[0]

    with open(download_path + "/" + file_name, "r") as original_file:
        with open(download_path + "/" + file_name.split(".srt")[0] + "_corrected" + ".srt", "w") as corrected_file:
            for line in original_file:
                if "-->" in line:
                    time_segment_list = line.split(" --> ")
                    new_start_time = get_new_time(
                        time_segment_list[0], amount, operation)
                    new_end_time = get_new_time(
                        time_segment_list[1], amount, operation)
                    line = new_start_time + " --> " + new_end_time + "\n"
                corrected_file.write(line)
    return True


def get_new_time(old_time, amount, operation):
    """Takes a time-string (old_time) formatted as HH:mm:ss,SSS and adds or subtracts amount,
    formatted as ss,SSS, to or from old_time based on the value of operation (+/-)"""
    amount_list = amount.split(",")
    total_adjust_in_milliseconds = int(
        amount_list[0]) * 1000 + int(amount_list[1])
    time_list = old_time.split(":")
    time_list.extend(time_list[2].split(","))
    del time_list[2]
    time_list = [int(x) for x in time_list]

    if operation == "+":
        total_time_in_milliseconds = time_list[0] * 3600000 + time_list[1] * \
            60000 + time_list[2] * 1000 + time_list[3] + total_adjust_in_milliseconds
    else:
        total_time_in_milliseconds = time_list[0] * 3600000 + time_list[1] * \
            60000 + time_list[2] * 1000 + time_list[3] - total_adjust_in_milliseconds

    hour = total_time_in_milliseconds // 3600000
    remainder = total_time_in_milliseconds % 3600000
    minute = remainder // 60000
    remainder = remainder % 60000
    seconds = remainder // 1000
    remainder = remainder % 1000
    milliseconds = remainder

    hour = str(hour)
    minute = str(minute)
    seconds = str(seconds)
    milliseconds = str(milliseconds)

    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute
    if len(seconds) == 1:
        seconds = "0" + seconds
    if len(milliseconds) == 1:
        milliseconds = "00" + milliseconds
    elif len(milliseconds) == 2:
        milliseconds = "0" + milliseconds

    return hour + ":" + minute + ":" + seconds + "," + milliseconds


def print_startup_info():
    """Prints info about the behaviour of the program"""
    print("Time correction tool for srt-scripts on macos and linux")
    print("Assumes script is located in download-folder of user ")


def main():
    "Main-method which is executed when running the script"
    print_startup_info()

    download_path = get_download_path()
    downloaded_srt_files = get_downloaded_srt_files(download_path)

    file_name = None
    while file_name is None:
        file_name = get_unique_file(downloaded_srt_files)

    while not time_correct_file(file_name, download_path):
        time_correct_file(file_name, download_path)


if __name__ == '__main__':
    main()
