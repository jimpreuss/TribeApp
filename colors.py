from PyQt5.QtGui import QColor

class Colors:
    with open('style_sheet.qss', 'r') as f:
        standard_style = f.read()
    with open('alt_style_sheet.qss', 'r') as f:
        alt_style = f.read()
    pink1 = "#ff6296"
    pink2 = "#ff7ca7"
    pink3 = "#ffafcb"

    blue1 = "#3d6b82"
    blue2 = "#689fbc"
    blue3 = "#a7d9f4"

    yellow1 = "#a7d9f4"
    yellow2 = "#fde38a"
    yellow3 = "#fff3c6"

    orange1 = "#e8973d"
    orange2 = "#fbb975"
    orange3 = "#ffdaae"

    red1 = "#9d0a35"
    red2 = "#c03858"
    red3 = "#c696a0"

    green1 = "#c8cc5a"
    green2 = "#e8eb96"
    green3 = "#fdffdb"


    grey = "#bababa"
    black1 = "#000000"

    white1 = "#ffffff"
    white2 = "#fff4e8"
    white3 = "#fffaf5"

    black2 = "#282623"

    schriftart = "Helvetica"
    fontsize = "15px"

    colours = [pink1, pink2, pink3, blue1, blue2,blue3, yellow1, yellow2, yellow3, orange1, orange2,orange3,
               red1, red2, red3, green1, green2, green3, white1, grey, black1, white2, black2, white3, schriftart, fontsize]

    colour_names = ["pink1", "pink2", "pink3", "blue1", "blue2","blue3", "yellow1", "yellow2", "yellow3", "orange1", "orange2","orange3",
               "red1", "red2", "red3", "green1", "green2", "green3", "white1", "grey", "black1", "white2", "black2", "white3", "schriftart", "fontsize"]


    normal_text_edit_style = """background-color: white3;
                                selection-background-color: green2;
                                border: 10px solid white3;
                                """

    edited_text_edit_style = """background-color: white3;
                                selection-background-color: green2;
                                border: 10px solid white1;
                                """

    selected_text_edit_style = """  background-color: green3;
                                    selection-background-color: green2;
                                    border: 10px solid green3;
                                    """

    last_selected_text_edit_style = """  background-color: green3;
                                    selection-background-color: green2;
                                    border: 10px solid white1;
                                    """

    wish_normal_text_edit_style = """   background-color: pink3;
                                        selection-background-color: pink2;
                                        border: 10px solid pink3;
                                        """

    wish_edited_text_edit_style = """   background-color: pink3;
                                    selection-background-color: pink2;
                                    border: 10px solid white1;
                                    """

    wish_selected_text_edit_style = """  background-color: pink2;
                                        selection-background-color: pink1;
                                        border: 10px solid pink3;
                                        """

    last_wish_selected_text_edit_style = """  background-color: pink2;
                                        selection-background-color: pink1;
                                        border: 10px solid white1;
                                        """

    observation_normal_text_edit_style = """    background-color: yellow3;
                                                selection-background-color: yellow2;
                                                border: 10px solid yellow3;
                                                """

    observation_edited_text_edit_style = """background-color: yellow3;
                                            selection-background-color: yellow2;
                                            border: 10px solid white1;
                                            """

    observation_selected_text_edit_style = """  background-color: yellow2;
                                                selection-background-color: yellow1;
                                                border: 10px solid yellow3;
                                                """

    last_observation_selected_text_edit_style = """  background-color: yellow2;
                                                selection-background-color: yellow1;
                                                border: 10px solid white1;
                                                """

    negativ_normal_text_edit_style = """background-color: red3;
                                        selection-background-color: red2;
                                        border: 10px solid red3;
                                        """

    negativ_edited_text_edit_style = """background-color: red3;
                                        selection-background-color: red2;
                                        border: 10px solid white1;
                                        """

    negativ_selected_text_edit_style = """  background-color: red2;
                                            selection-background-color: red1;
                                            border: 10px solid red3;
                                            """

    last_negativ_selected_text_edit_style = """  background-color: red2;
                                            selection-background-color: red1;
                                            border: 10px solid white1;
                                            """

    solution_normal_text_edit_style = """   background-color: blue3;
                                            selection-background-color: blue2;
                                            border: 10px solid blue3;
                                            """

    solution_edited_text_edit_style = """   background-color: blue3;
                                            selection-background-color: blue2;
                                            border: 10px solid white1;
                                            """

    solution_selected_text_edit_style = """ background-color: blue2;
                                            selection-background-color: blue1;
                                            border: 10px solid blue3;
                                            """

    last_solution_selected_text_edit_style = """ background-color: blue2;
                                            selection-background-color: blue1;
                                            border: 10px solid white1;
                                            """



    for i in range(len(colours)):
        standard_style = standard_style.replace(colour_names[i], colours[i])
        alt_style = alt_style.replace(colour_names[i], colours[i])
        normal_text_edit_style = normal_text_edit_style.replace(colour_names[i], colours[i])
        selected_text_edit_style = selected_text_edit_style.replace(colour_names[i], colours[i])
        edited_text_edit_style = edited_text_edit_style.replace(colour_names[i], colours[i])

        wish_selected_text_edit_style = wish_selected_text_edit_style.replace(colour_names[i], colours[i])
        wish_edited_text_edit_style = wish_edited_text_edit_style.replace(colour_names[i], colours[i])
        wish_normal_text_edit_style = wish_normal_text_edit_style.replace(colour_names[i], colours[i])

        negativ_selected_text_edit_style = negativ_selected_text_edit_style.replace(colour_names[i], colours[i])
        negativ_normal_text_edit_style = negativ_normal_text_edit_style.replace(colour_names[i], colours[i])
        negativ_edited_text_edit_style = negativ_edited_text_edit_style.replace(colour_names[i], colours[i])

        observation_selected_text_edit_style = observation_selected_text_edit_style.replace(colour_names[i], colours[i])
        observation_edited_text_edit_style = observation_edited_text_edit_style.replace(colour_names[i], colours[i])
        observation_normal_text_edit_style = observation_normal_text_edit_style.replace(colour_names[i], colours[i])

        solution_selected_text_edit_style = solution_selected_text_edit_style.replace(colour_names[i], colours[i])
        solution_edited_text_edit_style = solution_edited_text_edit_style.replace(colour_names[i], colours[i])
        solution_normal_text_edit_style = solution_normal_text_edit_style.replace(colour_names[i], colours[i])

        last_selected_text_edit_style = last_selected_text_edit_style.replace(colour_names[i], colours[i])
        last_wish_selected_text_edit_style = last_wish_selected_text_edit_style.replace(colour_names[i], colours[i])
        last_negativ_selected_text_edit_style = last_negativ_selected_text_edit_style.replace(colour_names[i], colours[i])
        last_observation_selected_text_edit_style = last_observation_selected_text_edit_style.replace(colour_names[i], colours[i])
        last_solution_selected_text_edit_style = last_solution_selected_text_edit_style.replace(colour_names[i], colours[i])

