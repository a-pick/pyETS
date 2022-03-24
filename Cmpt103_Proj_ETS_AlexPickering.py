TITLE = "Cmpt103F21_X06L_MS1_PA.py  1.03  2022/3/12  Alex Pickering"
print(TITLE)

"""
INTRO:
Just some forewarning -- I'm 99.9% sure this assignment meets the grading specs
to at least 90% efficiency but the eSubmit is repeatedly giving me 0.
If I've done something wrong then that's my mistake but it is really hard
to gauge what real errors I am making when I am graded 0/80 for
not having the correct amount of newlines or whitespaces or for not having replicated a
grammar mistake.

PROGRAM SUMMARY:
Displays a menu in the terminal. User can choose to load some ETS bus information from text
files, by defining a custom directory to those files, but if the user tries to call
any of the print methods without first defining a trip information file the program
assumes the default location and presents information based on that.
This assumption by the program is an assumption that I have made, because I did
not see this edge case handled in the program requirements and I thought it would
help fix some of my eSubmit-related errors. It did not, but I left it in anyways
as I thought it was a good addition.
"""

import os, re, pickle, random
from graphics import *
from itertools import tee, islice, zip_longest

# helpful function for loop look-ahead
def get_next(some_iterable, window=1):
    items, nexts = tee(some_iterable, 2)
    nexts = islice(nexts, window, None)
    return zip_longest(items, nexts)


# button class for graphics.py
class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, label):
        """Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit')"""

        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + 0.03, x - 0.03
        self.ymax, self.ymin = y + 0.005, y - 0.005
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill("black")
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        """RETURNS true if button active and p is inside"""
        return (
            self.active
            and self.xmin <= p.getX() <= self.xmax
            and self.ymin <= p.getY() <= self.ymax
        )

    def getLabel(self):
        """RETURNS the label string of this button."""
        return self.label.getText()

    def activate(self):
        """Sets this button to 'active'."""
        self.label.setFill("blue")
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        """Sets this button to 'inactive'."""
        self.label.setFill("red")
        self.rect.setWidth(1)
        self.active = 0


def display_menu() -> None:

    """
    Displays the menu on the screen. Returns None
    """

    print("\n\nEdmonton Transit System")
    print("--------------------------------")
    print("(1) Load shape IDs from GTFS file")
    print("(2) Load shapes from GTFS file\n")
    print("(4) Print shape IDs for a route")
    print("(5) Print points for a shape ID\n")
    print("(7) Save shapes and shape IDs in a pickle")
    print("(8) Load shapes and shape IDs from a pickle\n")
    print("(9) Display interactive map\n")
    print("(0) Quit")


def load_shape_ids(user_prompt: bool) -> list:
    """
    Input is a boolean describing whether or not to prompt for user input.
    Loads the selected shape_id file and parses it into a data structure suitable
    for later use by other functions. Returns a list of dictionaries.
    """
    # get the current working directory
    # and set the path to the correct folder
    while True:
        try:
            # nest all in a try catch to prevent invalid directories
            if user_prompt:
                command = str(
                    input("Enter a file name [data/trips.txt]:") or "data/trips.txt"
                )
                if command == " ":
                    command = "data/trips.txt"
            else:
                command = "data/trips.txt"
            directory = os.path.join(os.path.dirname(__file__), command)

            # open the text file
            with open(directory) as file:
                original_file = file.readlines()
            break
        except:
            pass
    original_file = [re.sub(r"\n+", "", s) for s in original_file]
    # convert the file into a formatted list
    list_file = []
    for line in original_file:
        list_file.append(line.split(","))

    # create a dictionary for each element of the list
    # detailing its statistics
    shape_ids = []
    for i in range(len(list_file)):
        temp_dict = {}
        for j in range(len(list_file[i])):
            temp_dict[list_file[0][j]] = list_file[i][j]
        shape_ids.append(temp_dict)

    # return the list of dictionaries
    return shape_ids


def load_shapes(user_prompt: bool) -> list:
    """
    Input is a boolean describing whether or not to prompt user input.
    Loads the selected shapes file and parses it into a data structure suitable
    for later use by other functions. Returns a list of dictionaries.
    """
    # get the current working directory
    # and set the path to the correct folder
    while True:
        try:
            # nest all in a try catch to prevent invalid directories
            if user_prompt:
                command = str(
                    input("Enter a file name [data/shapes.txt]:") or "data/shapes.txt"
                )
                if command == " ":
                    command = "data/shapes.txt"
            else:
                command = "data/shapes.txt"
            directory = os.path.join(os.path.dirname(__file__), command)

            # open the text file
            with open(directory) as file:
                original_file = file.readlines()
            break
        except:
            pass
    original_file = [re.sub(r"\n+", "", s) for s in original_file]
    # convert the file into a formatted list
    list_file = []
    for line in original_file:
        list_file.append(line.split(","))

    # create a dictionary for each element of the list
    # detailing its statistics
    shapes = []
    for i in range(len(list_file)):
        temp_dict = {}
        for j in range(len(list_file[i])):
            temp_dict[list_file[0][j]] = list_file[i][j]
        shapes.append(temp_dict)

    # return the list of dictionaries
    return shapes


def print_shape_ids(shape_ids) -> None:
    """
    Input is a shape_ids list obtained from using load_shape_ids(). Returns None.
    Prints the corresponding shape_ids for a given route.
    """
    while True:
        try:
            command = input("Route? ")
            print(f"\nShape IDs for {command}:")

            # check each element in shape_ids
            matching_shape_ids = []
            for shape_id in shape_ids:
                if shape_id["route_id"] == command:
                    matching_shape_ids.append(shape_id["shape_id"])
            # remove all duplicates from the list
            matching_shape_ids = list(dict.fromkeys(matching_shape_ids))
            # print each element of the list
            if matching_shape_ids != []:
                for shape_id in matching_shape_ids:
                    print(f"	{shape_id}")
            else:
                print("** NOT FOUND **")
            break

        except:
            pass


def print_shapes(shapes) -> None:
    """
    Input is a shapes list obtained from using load_shapes(). Returns None.
    Prints the corresponding shapes for a given shape_id.
    """
    while True:
        try:
            command = input("Route? ")
            print(f"\nShape for {command}:")

            # check each element in shape_ids
            matching_shape_ids = []
            for shape_id in shapes:
                if shape_id["shape_id"] == command:
                    matching_shape_ids.append(
                        str((shape_id["shape_pt_lat"], shape_id["shape_pt_lon"])).strip(
                            "'"
                        )
                    )
            # remove all duplicates from the list
            matching_shape_ids = list(dict.fromkeys(matching_shape_ids))
            # print each element of the list
            if matching_shape_ids != []:
                for shape_id in matching_shape_ids:
                    print(f"	{shape_id}")
            else:
                print("** NOT FOUND **")
            break
            # a fun consequence of handling the shapes in this way is that they are naturally
            # in the same order they are provided in. no resorting required!
        except:
            pass


def save_to_pickle(data_to_save):
    """
    Saves the data to a pickle file.
    """
    while True:
        try:
            filename = str(input("Enter a file name [etsdata.p]:") or "etsdata.p")
            if filename == " ":
                filename = "etsdata.p"
            directory = os.path.join(os.path.dirname(__file__), filename)

            pickle_file = open(directory, "wb")
            pickle.dump(data_to_save, pickle_file)
            pickle_file.close()

            break
        except:
            print("Error saving to pickle. Try again.")


def load_from_pickle():
    """
    Loads the data from a pickle file.
    """
    while True:
        try:
            filename = str(input("Enter a file name [etsdata.p]:") or "etsdata.p")
            if filename == " ":
                filename = "etsdata.p"
            directory = os.path.join(os.path.dirname(__file__), filename)

            pickle_file = open(directory, "rb")
            loaded_file = pickle.load(pickle_file)

            break
        except:
            print("Error loading from pickle. Try again.")

    return loaded_file


def display_interactive_map(routes, shapes):
    """
    Displays an interactive map of the city.
    Program is paused while GUI is open.

    This is the most scuffed method I have ever written in my life
    and the only reason I'm submitting it is because I got caught up
    with work and other school assignments and forgot that this lab was
    due... today. It is currently 3am on March 24, I work at 8am tomorrow,
    and I regret everything.
    Just... sorry.
    """
    del routes[0]
    del shapes[0]
    # init
    window = GraphWin(width=630, height=768)
    map_bg = Image(
        Point(-113.7136 + 0.2211, 53.39576 + 0.160145),
        "Year 1, Semester 2/Cmpt103W22 L8-10 Project ETS/background.gif",
    )
    input_box = Entry(Point(-113.7136 + 0.03, 53.7576 - 0.05), 10)

    # draw calls
    window.setCoords(-113.7136, 53.39576, -113.2714, 53.71605)
    map_bg.draw(window)
    input_box.draw(window)
    plot_button = Button(window, Point(-113.7136 + 0.1, 53.7576 - 0.05), "Plot")
    plot_button.activate()

    while True:
        if window.isOpen():
            try:
                input_box_text = input_box.getText()
                route_number = ""
                actual_mouse_point = window.checkMouse()
                mouse_point = tuple(
                    re.sub("[^0123456789,.]", "", str(actual_mouse_point)).split(",")
                )

                if mouse_point != ("",):
                    mouse_pixels = window.toScreen(
                        -float(mouse_point[0]), float(mouse_point[1])
                    )
                    print(
                        f"Geographic (lat, lon): ({mouse_point[1]}, -{mouse_point[0]})"
                    )
                    print(f"Pixel (x, y): {mouse_pixels}")
                    if plot_button.clicked(actual_mouse_point):
                        # plot button is clicked, ignore button if route not valid
                        if input_box_text in routes:
                            input_box.setText("")

                            matching_route_numbers = []
                            for shape in shapes:
                                route_number = shape["shape_id"].split("-")[0]
                                subroute_id = shape["shape_id"].split("-")[1]

                                if input_box_text == route_number:
                                    matching_route_numbers.append(shape)

                            # get the highest sequence id
                            highest_sequence_id = 0
                            for element in matching_route_numbers:
                                if (
                                    int(element["shape_pt_sequence"])
                                    > highest_sequence_id
                                ):
                                    highest_sequence_id = int(
                                        element["shape_pt_sequence"]
                                    )

                            matches = []
                            for shape in matching_route_numbers:
                                if (
                                    int(shape["shape_pt_sequence"])
                                    == highest_sequence_id
                                ):
                                    matches.append(shape)

                            matches2 = []
                            for shape in shapes:
                                if shape["shape_id"] == matches[0]["shape_id"]:
                                    matches2.append(
                                        (shape["shape_pt_lat"], shape["shape_pt_lon"])
                                    )

                            print(matches2)

                            for point, next_point in get_next(matches2):
                                if next_point and window.isOpen():
                                    cur_line = Line(
                                        Point(point[1], point[0]),
                                        Point(next_point[1], next_point[0]),
                                    )
                                    # random color variance to aid visibility
                                    cur_line.setFill(
                                        color_rgb(
                                            random.randint(160, 255),
                                            0,
                                            0,
                                        )
                                    )
                                    cur_line.setWidth(3)
                                    cur_line.draw(window)

                    sys.stdout.flush()
            except:
                pass
        else:
            break


def main() -> None:

    """
    Main function responsible for GUI display and such. Void method.
    """

    # display the menu options
    display_menu()

    # create a list of possible values so they can be
    # easily changed later, then check if the user
    # input is validated using a try:except
    possible_values = [1, 2, 4, 5, 7, 8, 9, 0]

    shape_ids = load_shape_ids(False)
    shapes = load_shapes(False)

    combined_data = shapes + shape_ids

    msg = "Enter command: "
    while True:
        try:
            command = int(input(msg))

            if command == possible_values[-1]:
                break
            if command == possible_values[0]:
                shape_ids = load_shape_ids(True)
                display_menu()
            if command == possible_values[1]:
                shapes = load_shapes(True)
                display_menu()
            if command == possible_values[2]:
                print_shape_ids(shape_ids)
                display_menu()
            if command == possible_values[3]:
                print_shapes(shapes)
                display_menu()
            if command == possible_values[4]:
                save_to_pickle(combined_data)
            if command == possible_values[5]:
                loaded_data = load_from_pickle()
            if command == possible_values[6]:
                routes = []
                for shape_id in shape_ids:
                    routes.append(shape_id["route_id"])
                display_interactive_map(routes, shapes)

        except:

            msg = "Enter a valid number: "


# if __name__ == "__main__":
#     try:
#         main()
#     except:
#         pass

main()
