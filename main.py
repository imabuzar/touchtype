import curses
import random
import time

main_menu_text = "Whether you're starting from scratch or looking to improve your typing speed,\nwe've designed a systematic approach to help you master the keyboard.\nChoose your skill level below to begin your typing journey.\n"

modes = {
    "novice": {
        "name": "Novice - Home Row",
        "words_count": 15,
        "letters": "asdfghjkl;",
    },
    "beginner": {
        "name": "Beginner - Home Row + Easy Reach",
        "words_count": 20,
        "letters": "asdfghjkl;wertiop",
    },
    "intermediate": {
        "name": "Intermediate - Adding Bottom Row",
        "words_count": 30,
        "letters": "asdfghjkl;wertyuiopzxcvbnm,.",
    },
    "advanced": {
        "name": "Advanced - Full Keyboard",
        "words_count": 50,
        "letters": "asdfghjkl;wertyuiopzxcvbnm,.QWERTYUIOPASDFGHJKLZXCVBNM",
    },
    "expert": {
        "name": "Expert - Special Characters",
        "words_count": 75,
        "letters": "asdfghjkl;wertyuiopzxcvbnm,.QWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()",
    },
    "custom": {
        "name": "Custom - Create your own",
        "words_count": None,
        "letters": "",
    },
}

# list of all mode names
mode_names = list(modes.keys())


# function to read all words from file
def load_words() -> list:
    try:
        with open("words.txt", "r") as f:
            words = f.readlines()
        return [word.strip() for word in words]  # remove newlines from end
    except FileNotFoundError:
        print("Error: words.txt not found")
        exit(1)
    except Exception as e:
        print(f"Error loading words: {e}")
        exit(1)


def get_text(letters: str, words_count: int = 20) -> str:
    words = load_words()  # load all words list
    # filter words based on letters
    filtered_words = [word for word in words if set(
        word).issubset(set(letters))]
    # pick 'words_count' words from the filtered_words
    word_list = random.sample(filtered_words, words_count)

    # joining each word with space to create string
    text = " ".join(word_list)
    return text


def calculate_result(
    time_elapsed: float,
    total_letters: int,
    errors: int,
) -> tuple:
    # WPM = (characters per minute / 5) where 5 is average word length
    cpm = total_letters / time_elapsed
    wpm = cpm / 5
    # calculate accuracy
    accuracy = ((total_letters - errors) / total_letters) * 100

    return round(wpm, 2), round(accuracy, 2)


# result screen that is called in start() to dislay results
def result_screen(
    mode_name: str,
    time_elapsed: float,
    wpm: float,
    accuracy: float,
    stdscr: curses.window,
):
    stdscr.clear()
    stdscr.addstr(
        f"TouchType | {modes[mode_name]['name']}\n", curses.color_pair(1))
    stdscr.addstr("\nResult\n", curses.color_pair(2))
    stdscr.addstr("------\n", curses.color_pair(2))

    stdscr.addstr(
        f"{time_elapsed} minutes ({round(time_elapsed*60)} sec) elapsed\n")
    stdscr.addstr(f"{wpm} words per minute\n")
    stdscr.addstr(f"{accuracy}% accuracy\n")

    # getting input for what next
    stdscr.addstr("\n\nWant to start again? (y/n)", curses.color_pair(2))
    key = stdscr.getkey()

    if key.lower() == "y":
        start(mode_name, stdscr)  # starting again with same mode
    elif key.lower() == "n":
        menu_screen(stdscr)  # back to main screen
    else:
        result_screen(mode_name, time_elapsed, wpm, accuracy, stdscr)


def start(mode: str, stdscr: curses.window):
    # for the text user has typed
    current = []
    # current text index
    current_index = 0

    if mode == "custom":
        # Custom mode implementation
        stdscr.clear()
        stdscr.addstr(0, 0, "TouchType | Custom Mode", curses.color_pair(1))
        stdscr.addstr(
            2, 0, "Enter the characters you want to practice (e.g., asdf123): ")
        curses.echo()  # Enable echo to see what you're typing
        custom_letters = stdscr.getstr(2, 60).decode('utf-8')
        curses.noecho()  # Disable echo

        stdscr.addstr(4, 0, "Enter the number of words to practice: ")
        curses.echo()
        words_count_str = stdscr.getstr(4, 40).decode('utf-8')
        curses.noecho()

        try:
            words_count = int(words_count_str)
            if words_count <= 0:
                raise ValueError
        except ValueError:
            stdscr.addstr(
                6, 0, "Invalid input. Using default of 20 words.", curses.color_pair(4))
            stdscr.refresh()
            time.sleep(2)
            words_count = 20

        # Update the custom mode settings
        modes["custom"]["letters"] = custom_letters
        modes["custom"]["words_count"] = words_count

        # Check if there are enough words with the chosen characters
        words = load_words()
        filtered_words = [word for word in words if set(
            word).issubset(set(custom_letters))]

        if len(filtered_words) < words_count:
            stdscr.clear()
            stdscr.addstr(0, 0, "TouchType | Custom Mode",
                          curses.color_pair(1))
            stdscr.addstr(
                2, 0, f"Not enough words found with those characters.", curses.color_pair(4))
            stdscr.addstr(
                3, 0, f"Found {len(filtered_words)} words, but {words_count} were requested.", curses.color_pair(4))
            stdscr.addstr(5, 0, "Press any key to return to the menu.")
            stdscr.refresh()
            stdscr.getch()
            menu_screen(stdscr)
            return

    # Get total_words using mode name
    total_words = modes[mode]["words_count"]
    # Get target string for user to type
    target_string = get_text(modes[mode]["letters"], total_words)
    # Start and end time
    start_time = time.time()
    end_time = None
    # Variable to keep track of errors made
    errors = 0

    while True:
        stdscr.clear()
        stdscr.addstr(
            0, 0, f"TouchType | {modes[mode]['name']}", curses.color_pair(1))

        # get terminal height (not using), and width
        _, width = stdscr.getmaxyx()

        # display original text
        stdscr.addstr(2, 0, target_string)

        i = 0  # for width tracking
        j = 0  # for height tracking

        # displaying written text by user character by character
        for char in current:
            # when line completes
            if i > (width - 1):
                i = 0
                j += 1

            # Calculate current character index
            char_index = i + (j * width)
            # Select color based on correctness
            char_color = (
                curses.color_pair(3)
                if char == target_string[char_index]
                else curses.color_pair(4)
            )
            # Add character with the appropriate color
            stdscr.addstr(j + 2, i, char, char_color)
            # Move to the next position
            i += 1

        # if typed letters become equal to total letters
        if len(target_string) == len(current):
            end_time = time.time()
            # calculate total time in minutes
            time_elapsed = (end_time - start_time) / 60
            # get results
            wpm, accuracy = calculate_result(
                time_elapsed,
                len(target_string),
                errors,
            )
            result_screen(mode, round(time_elapsed, 2), wpm, accuracy, stdscr)
            break

        stdscr.refresh()
        # character input
        ch = stdscr.getkey()

        if ch == "\x1b":  # Escape key
            break
        elif ch in ("KEY_BACKSPACE", "\b", "\x7f"):  # Backspace key
            if current:
                current.pop()  # Remove the last character
                current_index -= 1  # move to index back
        elif len(ch) == 1 and ch.isprintable():  # Allow only printable characters
            current.append(ch)  # Append typed character
            # if typed letter is incorrect
            if ch != target_string[current_index]:
                errors += 1
                curses.beep()
            current_index += 1  # move to next index


def menu_screen(stdscr: curses.window):
    stdscr.clear()
    stdscr.addstr("Welcome to TouchType!\n\n", curses.color_pair(1))
    stdscr.addstr(main_menu_text)
    stdscr.addstr("\n\n0. Exit the program\n\n")

    # display each mode name from modes dict
    for i, mode in enumerate(mode_names, start=1):
        stdscr.addstr(f"{i}. {modes[mode]['name']}\n")

    stdscr.addstr("\n\nSelect the mode: ", curses.color_pair(2))
    stdscr.refresh()

    # take key input as a single character string
    key = stdscr.getkey()

    # wrong or undesired input
    if (not key.isdigit()) or (int(key) not in range(0, 7)):
        menu_screen(stdscr)
    elif key == "0":
        exit()  # exit program
    else:  # start the typing with input mode
        start(mode_names[int(key) - 1], stdscr)
        menu_screen(stdscr)


# check for required terminal size
def check_terminal_size(stdscr):
    height, width = stdscr.getmaxyx()
    if height < 20 or width < 80:
        raise curses.error(
            "Terminal window too small. Minimum 80x20 required.")


def main(stdscr: curses.window):
    # color pairs to be used with curses to display text
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    check_terminal_size(stdscr)
    menu_screen(stdscr)


curses.wrapper(main)
