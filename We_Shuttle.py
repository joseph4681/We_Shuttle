"""
This program generates 'We Shuttle' application,
a user interface to access player details, game results, individual & team records
"""

from DropDate.DropDate import *
from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import ImageTk, Image

root = Tk()
root.title("We Shuttle")
root.iconbitmap("C:/Users/sesa321516/PycharmProjects/MyTkinterProject/We_Shuttle/We_Shuttle.ico")
root.geometry("1025x645+0+0")


canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical")
scrollable_frame = Frame(canvas)

canvas.create_window((0, 0), window=scrollable_frame, anchor=W)


def scroll_region_update_func(event):
    canvas.config(scrollregion=canvas.bbox("all"))


scrollable_frame.bind("<Configure>", scroll_region_update_func)
canvas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

title_image = ImageTk.PhotoImage(Image.open("C:/Users/sesa321516/PycharmProjects/MyTkinterProject/We_Shuttle/We_Shuttle.jpg").resize((590, 50)))
title_image_l = Label(scrollable_frame, image=title_image, anchor=W)
title_image_l.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)

"""
Following commands shall be executed only once to create the database and tables
"""

"""
we_shuttle_connect = sqlite3.connect("WeShuttle.db")
we_shuttle_cursor = we_shuttle_connect.cursor()

we_shuttle_cursor.execute("CREATE TABLE players_list (t_f_name text, t_l_name text, t_age text)")

we_shuttle_connect.commit()
we_shuttle_connect.close()
"""

players_list_title = ("P_Id", "First Name", "Last Name", "Age", "P_Ref")
game_results_title = ("G_Ref", "Venue", "Winner Player 1", "Winner Player 2", "Scorecard",
                      "Runner Player 1", "Runner Player 2")
team_records_title = ("Team", "Total Wins", "Point Diff", "Games Played")
individual_records_title = ("Player", "Total Wins", "Point Diff", "Games Played")


class TreeFrame:
    def __init__(self, parent, row, column):
        self.parent = parent
        self.row = row
        self.column = column
        self.frame = Frame(self.parent)
        self.state = BooleanVar()
        self.state.set(False)
        self.sign = ">"

    def toggle(self):
        if self.state.get() is True:
            self.frame.grid_remove()
            self.state.set(False)
            self.sign = ">"
        else:
            self.frame.grid(row=self.row, column=self.column, sticky=NW, padx=10, pady=10, ipadx=5, ipady=5)
            self.state.set(True)
            self.sign = "v"

    def show(self):
        self.frame.grid(row=self.row, column=self.column, sticky=NW, padx=10, pady=10, ipadx=5, ipady=5)
        self.state.set(True)
        self.sign = "v"

    def hide(self):
        self.frame.grid_remove()
        self.state.set(False)
        self.sign = ">"

    def destroy_and_rebuild(self):
        self.frame.destroy()
        self.frame = Frame(self.parent)


def show_players_list_func():
    if show_players_list_f.sign == ">":
        show_players_list_f.destroy_and_rebuild()

        we_shuttle_connect = sqlite3.connect("WeShuttle.db")
        we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
        we_shuttle_cursor = we_shuttle_connect.cursor()

        we_shuttle_cursor.execute("SELECT * FROM players_list ORDER BY t_p_id ASC")
        records_players_list = we_shuttle_cursor.fetchall()

        we_shuttle_connect.commit()
        we_shuttle_connect.close()

        records_players_list.insert(0, players_list_title)

        # print(records_players_list)

        x = 0

        for record in records_players_list:
            if x == 0:
                Label(show_players_list_f.frame, text=record[0], width=10, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=x, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            else:
                Label(show_players_list_f.frame, text=record[0], width=10, anchor=W).\
                    grid(row=x, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            x += 1

        for y in range(1, 4):
            x = 0
            for record in records_players_list:
                if x == 0:
                    Label(show_players_list_f.frame, text=record[y], width=15, anchor=W, font="Helvetica 9 bold") \
                        .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                else:
                    Label(show_players_list_f.frame, text=record[y], width=15, anchor=W)\
                        .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                x += 1

    show_players_list_f.toggle()
    show_players_list_b.config(text=show_players_list_f.sign + " Show Players List")


def show_game_results_f_func():
    if show_game_results_f.sign == "v":
        last_ten_res_f.hide()
        show_game_results_f_last_ten_res_b.config(text=last_ten_res_f.sign + " Last 10 Results")
    show_game_results_f.toggle()
    show_game_results_b.config(text=show_game_results_f.sign + " Show Game Results")


def last_ten_res_func():
    if last_ten_res_f.sign == ">":
        last_ten_res_f.destroy_and_rebuild()

        we_shuttle_connect = sqlite3.connect("WeShuttle.db")
        we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
        we_shuttle_cursor = we_shuttle_connect.cursor()

        we_shuttle_cursor.execute("SELECT t_g_ref, t_venue, t_a_player_1, t_a_player_2, "
                                  "t_a_points, t_b_points, t_b_player_1, t_b_player_2 "
                                  "FROM game_results ORDER BY t_g_ref DESC LIMIT 10")
        records_game_results_list = we_shuttle_cursor.fetchall()

        we_shuttle_connect.commit()
        we_shuttle_connect.close()

        x = 0

        for title in game_results_title:
            if x == 0 or x == 1:
                Label(last_ten_res_f.frame, text=title, width=10, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=0, column=x, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            elif x == 4:
                Label(last_ten_res_f.frame, text=title, width=8, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=0, column=x, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            else:
                Label(last_ten_res_f.frame, text=title, width=18, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=0, column=x, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            x += 1

        x = 1
        for record in records_game_results_list:
            if record[4] > record[5]:
                for y, z in [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (6, 5), (7, 6)]:
                    if y == 0 or y == 1:
                        Label(last_ten_res_f.frame, text=record[y], width=10, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    elif y == 4:
                        Label(last_ten_res_f.frame, text=str(record[4]) + " - " + str(record[5]), width=8, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    else:
                        Label(last_ten_res_f.frame, text=record[y], width=18, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                x += 1

            elif record[5] > record[4]:
                for y, z in [(0, 0), (1, 1), (6, 2), (7, 3), (5, 4), (2, 5), (3, 6)]:
                    if y == 0 or y == 1:
                        Label(last_ten_res_f.frame, text=record[y], width=10, anchor=W) \
                            .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    elif y == 5:
                        Label(last_ten_res_f.frame, text=str(record[5]) + " - " + str(record[4]), width=8, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    else:
                        Label(last_ten_res_f.frame, text=record[y], width=18, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                x += 1

    last_ten_res_f.toggle()
    show_game_results_f_last_ten_res_b.config(text=last_ten_res_f.sign + " Last 10 Results")


def all_res_func():
    if all_res_f.sign == ">":
        all_res_f.destroy_and_rebuild()

        we_shuttle_connect = sqlite3.connect("WeShuttle.db")
        we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
        we_shuttle_cursor = we_shuttle_connect.cursor()

        we_shuttle_cursor.execute("SELECT t_g_ref, t_venue, t_a_player_1, t_a_player_2, "
                                  "t_a_points, t_b_points, t_b_player_1, t_b_player_2 "
                                  "FROM game_results ORDER BY t_g_ref DESC")
        records_game_results_list = we_shuttle_cursor.fetchall()

        we_shuttle_connect.commit()
        we_shuttle_connect.close()

        x = 0

        for title in game_results_title:
            if x == 0 or x == 1:
                Label(all_res_f.frame, text=title, width=10, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=0, column=x, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            elif x == 4:
                Label(all_res_f.frame, text=title, width=8, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=0, column=x, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            else:
                Label(all_res_f.frame, text=title, width=18, anchor=W, font="Helvetica 9 bold"). \
                    grid(row=0, column=x, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            x += 1

        x = 1
        for record in records_game_results_list:
            if record[4] > record[5]:
                for y, z in [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (6, 5), (7, 6)]:
                    if y == 0 or y == 1:
                        Label(all_res_f.frame, text=record[y], width=10, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    elif y == 4:
                        Label(all_res_f.frame, text=str(record[4]) + " - " + str(record[5]), width=8, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    else:
                        Label(all_res_f.frame, text=record[y], width=18, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                x += 1

            elif record[5] > record[4]:
                for y, z in [(0, 0), (1, 1), (6, 2), (7, 3), (5, 4), (2, 5), (3, 6)]:
                    if y == 0 or y == 1:
                        Label(all_res_f.frame, text=record[y], width=10, anchor=W) \
                            .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    elif y == 5:
                        Label(all_res_f.frame, text=str(record[5]) + " - " + str(record[4]), width=8, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                    else:
                        Label(all_res_f.frame, text=record[y], width=18, anchor=W) \
                            .grid(row=x, column=z, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
                x += 1

    all_res_f.toggle()
    show_game_results_f_all_res_b.config(text=all_res_f.sign + " All Results")


def team_records_func():
    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
    we_shuttle_cursor = we_shuttle_connect.cursor()

    we_shuttle_cursor.execute("""
                            SELECT sub_table_2.t_w_team, sub_table_2.t_wins, sub_table_2.t_point_diff, sub_table_4.t_games_played FROM
                                (SELECT t_w_team, COUNT(*) AS t_wins, AVG(t_point_diff) AS t_point_diff FROM 
                                    (SELECT CASE WHEN t_w_player_1 <= t_w_player_2  
                                    THEN t_w_player_1 || ' & ' || t_w_player_2 
                                    ELSE t_w_player_2 || ' & ' || t_w_player_1 
                                    END AS t_w_team, t_point_diff AS t_point_diff
                                    FROM game_results) AS sub_table_1 
                                GROUP BY t_w_team) AS sub_table_2
                            LEFT JOIN 
                                (SELECT t_team AS t_team, COUNT(*) AS t_games_played FROM 
                                    (SELECT CASE WHEN t_a_player_1 <= t_a_player_2  
                                    THEN t_a_player_1 || ' & ' || t_a_player_2 
                                    ELSE t_a_player_2 || ' & ' || t_a_player_1 
                                    END AS t_team
                                    FROM game_results 
                                    UNION ALL
                                    SELECT CASE WHEN t_b_player_1 <= t_b_player_2  
                                    THEN t_b_player_1 || ' & ' || t_b_player_2 
                                    ELSE t_b_player_2 || ' & ' || t_b_player_1 
                                    END
                                    FROM game_results) AS sub_table_3 
                                GROUP BY t_team) AS sub_table_4 
                            ON sub_table_2.t_w_team = sub_table_4.t_team
                            ORDER BY sub_table_2.t_wins DESC, sub_table_2.t_point_diff DESC, sub_table_4.t_games_played DESC
                            """)
    records_team_records = we_shuttle_cursor.fetchall()
    print(records_team_records)

    we_shuttle_connect.commit()
    we_shuttle_connect.close()

    Label(team_records_f.frame, text=team_records_title[0], width=40, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    Label(team_records_f.frame, text=team_records_title[1], width=8, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    Label(team_records_f.frame, text=team_records_title[2], width=8, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    Label(team_records_f.frame, text=team_records_title[3], width=12, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=3, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    x = 1

    for record in records_team_records:
        for y in range(0, 4):
            if y == 0:
                Label(team_records_f.frame, text=record[y], width=40, anchor=W) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            elif y == 2:
                Label(team_records_f.frame, text=round(record[y], 2), width=8, anchor=CENTER) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            elif y == 3:
                Label(team_records_f.frame, text=record[y], width=12, anchor=CENTER) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            else:
                Label(team_records_f.frame, text=record[y], width=8, anchor=CENTER) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

        x += 1

    team_records_f.toggle()
    team_records_b.config(text=team_records_f.sign + " Team Records")


def individual_records_f_func():
    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
    we_shuttle_cursor = we_shuttle_connect.cursor()

    we_shuttle_cursor.execute("""
                              SELECT sub_table_2.t_w_player, sub_table_2.t_wins, sub_table_2.t_point_diff, sub_table_4.t_games_played FROM 
                              (SELECT t_w_player AS t_w_player, SUM(t_wins) AS t_wins, AVG(t_point_diff) AS t_point_diff FROM   
                              (SELECT t_w_player_1 AS t_w_player, COUNT(t_w_player_1) AS t_wins, AVG(t_point_diff) AS t_point_diff
                              FROM game_results GROUP BY t_w_player_1 
                              UNION ALL 
                              SELECT t_w_player_2, COUNT(t_w_player_2) , AVG(t_point_diff)
                              FROM game_results GROUP BY t_w_player_2) AS sub_table_1 
                              GROUP BY t_w_player) AS sub_table_2 
                              LEFT JOIN (
                              SELECT t_player AS t_player, SUM(t_games_played) AS t_games_played FROM
                                  (SELECT t_a_player_1 AS t_player, COUNT(t_a_player_1) AS t_games_played 
                                  FROM game_results 
                                  GROUP BY t_a_player_1
                                  UNION ALL
                                  SELECT t_a_player_2, COUNT(t_a_player_2)
                                  FROM game_results 
                                  GROUP BY t_a_player_2
                                  UNION ALL
                                  SELECT t_b_player_1, COUNT(t_b_player_1)
                                  FROM game_results 
                                  GROUP BY t_b_player_1
                                  UNION ALL
                                  SELECT t_b_player_2, COUNT(t_b_player_2)
                                  FROM game_results 
                                  GROUP BY t_b_player_2) AS sub_table_3 
                                  GROUP BY t_player
                              ) AS sub_table_4 ON sub_table_2.t_w_player = sub_table_4.t_player
                              ORDER BY sub_table_2.t_wins DESC, sub_table_2.t_point_diff DESC, sub_table_4.t_games_played DESC
                              """)

    records_individual_records = we_shuttle_cursor.fetchall()
    #print(records_individual_records)

    we_shuttle_connect.commit()
    we_shuttle_connect.close()

    Label(individual_records_f.frame, text=individual_records_title[0], width=18, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    Label(individual_records_f.frame, text=individual_records_title[1], width=8, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    Label(individual_records_f.frame, text=individual_records_title[2], width=8, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    Label(individual_records_f.frame, text=individual_records_title[3], width=12, anchor=W, font="Helvetica 9 bold") \
        .grid(row=0, column=3, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

    x = 1

    for record in records_individual_records:
        for y in range(0, 4):
            if y == 0:
                Label(individual_records_f.frame, text=record[y], width=18, anchor=W) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            elif y == 2:
                Label(individual_records_f.frame, text=round(record[y],2), width=8, anchor=CENTER) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            elif y == 3:
                Label(individual_records_f.frame, text=record[y], width=12, anchor=CENTER) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
            else:
                Label(individual_records_f.frame, text=record[y], width=8, anchor=CENTER) \
                    .grid(row=x, column=y, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

        x += 1

    individual_records_f.toggle()
    individual_records_b.config(text=individual_records_f.sign + " Individual Records")


def all_players_id_func():
    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
    we_shuttle_connect.row_factory = lambda cursor, row: row[0]
    we_shuttle_cursor = we_shuttle_connect.cursor()

    we_shuttle_cursor.execute("SELECT t_p_id FROM players_list ORDER BY t_p_id ASC")
    records_all_players_id = we_shuttle_cursor.fetchall()

    we_shuttle_connect.row_factory = None
    we_shuttle_connect.commit()
    we_shuttle_connect.close()

    return records_all_players_id


def all_players_list_func():
    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
    we_shuttle_connect.row_factory = lambda cursor, row: row[0]
    we_shuttle_cursor = we_shuttle_connect.cursor()

    we_shuttle_cursor.execute("SELECT t_p_ref FROM players_list ORDER BY t_p_ref ASC")
    records_all_players_list = we_shuttle_cursor.fetchall()

    we_shuttle_connect.row_factory = None
    we_shuttle_connect.commit()
    we_shuttle_connect.close()

    return records_all_players_list


def all_game_results_func():
    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
    we_shuttle_connect.row_factory = lambda cursor, row: row[0]
    we_shuttle_cursor = we_shuttle_connect.cursor()

    we_shuttle_cursor.execute("SELECT t_g_ref FROM game_results ORDER BY t_g_ref ASC")
    records_all_game_results = we_shuttle_cursor.fetchall()

    we_shuttle_connect.row_factory = None
    we_shuttle_connect.commit()
    we_shuttle_connect.close()

    return records_all_game_results


def add_result_f_func():
    if add_result_f.sign == ">":
        add_result_f_player_list_refresh_func()
    # Initialize Add Result Frame
    add_result_f_g_id_e.delete(0, END)
    add_result_f_venue_e.delete(0, END)
    add_result_f_date_d.set_default()
    add_result_f_a_player_1.set("")
    add_result_f_a_player_2.set("")
    add_result_f_b_player_1.set("")
    add_result_f_b_player_2.set("")
    add_result_f_a_points_e.delete(0, END)
    add_result_f_b_points_e.delete(0, END)
    # Toggle Add Result Frame
    add_result_f.toggle()
    add_result_b.config(text=add_result_f.sign + " Add Game Result")


def add_result_f_player_list_refresh_func():
    records_all_players_list = all_players_list_func()

    menu_a_player_1 = add_result_f_a_player_1_om["menu"]
    menu_a_player_1.delete(0, END)
    for option in records_all_players_list:
        menu_a_player_1.add_command(label=option, command=tk._setit(add_result_f_a_player_1, option))

    menu_a_player_2 = add_result_f_a_player_2_om["menu"]
    menu_a_player_2.delete(0, END)
    for option in records_all_players_list:
        menu_a_player_2.add_command(label=option, command=tk._setit(add_result_f_a_player_2, option))

    menu_b_player_1 = add_result_f_b_player_1_om["menu"]
    menu_b_player_1.delete(0, END)
    for option in records_all_players_list:
        menu_b_player_1.add_command(label=option, command=tk._setit(add_result_f_b_player_1, option))

    menu_b_player_2 = add_result_f_b_player_2_om["menu"]
    menu_b_player_2.delete(0, END)
    for option in records_all_players_list:
        menu_b_player_2.add_command(label=option, command=tk._setit(add_result_f_b_player_2, option))


def add_result_func():
    g_id = str(add_result_f_g_id_e.get()).zfill(2)

    if len(g_id) == 2 and g_id.isnumeric() and g_id != "00":
        g_id = "G" + str(g_id)

        if add_result_f_a_player_1.get() != add_result_f_a_player_2.get() and add_result_f_a_player_1.get() != add_result_f_b_player_1.get() \
                and add_result_f_a_player_1.get() != add_result_f_b_player_2.get() and add_result_f_a_player_2.get() != add_result_f_b_player_1.get() \
                and add_result_f_a_player_2.get() != add_result_f_b_player_2.get() and add_result_f_b_player_1.get() != add_result_f_b_player_2.get():

            try:
                a_points = int(add_result_f_a_points_e.get())
                b_points = int(add_result_f_b_points_e.get())

                if a_points != b_points:

                    if a_points > b_points:
                        w_player_1 = add_result_f_a_player_1.get()
                        w_player_2 = add_result_f_a_player_2.get()
                        point_diff = a_points - b_points

                    else:
                        w_player_1 = add_result_f_b_player_1.get()
                        w_player_2 = add_result_f_b_player_2.get()
                        point_diff = b_points - a_points

                    g_ref = str(add_result_f_date_d.year_entered.get()) + str(
                        add_result_f_date_d.month_entered.get()).zfill(2) + \
                        str(add_result_f_date_d.date_entered.get()).zfill(2) + "_" + g_id

                    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
                    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
                    we_shuttle_cursor = we_shuttle_connect.cursor()

                    we_shuttle_cursor.execute(
                        "INSERT INTO game_results VALUES (:g_ref, :year, :month, :date, :g_id, :venue, "
                        ":a_player_1, :a_player_2, :b_player_1, :b_player_2, :a_points, :b_points, "
                        ":w_player_1, :w_player_2, :point_diff)",
                        {
                            'g_ref': g_ref,
                            'year': add_result_f_date_d.year_entered.get(),
                            'month': add_result_f_date_d.month_entered.get(),
                            'date': add_result_f_date_d.date_entered.get(),
                            'g_id': g_id,
                            'venue': add_result_f_venue_e.get(),
                            'a_player_1': add_result_f_a_player_1.get(),
                            'a_player_2': add_result_f_a_player_2.get(),
                            'b_player_1': add_result_f_b_player_1.get(),
                            'b_player_2': add_result_f_b_player_2.get(),
                            'a_points': a_points,
                            'b_points': b_points,
                            'w_player_1': w_player_1,
                            'w_player_2': w_player_2,
                            'point_diff': point_diff
                        }
                    )
                    messagebox.showinfo(title="Add Game Result", message="Game Result Added To Records")

                    we_shuttle_connect.commit()
                    we_shuttle_connect.close()

                else:
                    messagebox.showinfo(title="Add Game Result", message="Team A & B Points Cannot Be Equal")

            except ValueError as err:
                error_msg = str(err)
                if error_msg == "invalid literal for int() with base 10: ''":
                    messagebox.showinfo(title="Add Game Result", message="Points Field Cannot Be Empty")

            except sqlite3.IntegrityError as err:
                error_msg = str(err)
                if error_msg == "UNIQUE constraint failed: game_results.t_g_ref":
                    messagebox.showinfo(title="Add Game Result",
                                        message="Game With Game Id = " + str(add_result_f_g_id_e.get()) + " Already Exists")

        else:
            messagebox.showinfo(title="Add Game Result",
                                message="Players Cannot Be Duplicated Across Teams Or Within A Team")

    else:
        messagebox.showinfo(title="Add Game Result", message="Game Id Must Be 1-99")


def add_player_f_func():
    # Initialize Add Player Frame
    add_player_f_p_id_e.delete(0, END)
    add_player_f_f_name_e.delete(0, END)
    add_player_f_l_name_e.delete(0, END)
    add_player_f_age_e.delete(0, END)
    # Toggle Add Player Frame
    add_player_f.toggle()
    add_player_b.config(text=add_player_f.sign + " Add New Player")


def add_player_func():
    p_id = str(add_player_f_p_id_e.get()).zfill(2)

    if len(p_id) == 2 and p_id.isnumeric() and p_id != "00":
        p_id = "W" + str(p_id)

        if len(add_player_f_f_name_e.get()) <= 12 and len(add_player_f_l_name_e.get()) <= 12:

            if str(add_player_f_age_e.get()).isnumeric() and int(add_player_f_age_e.get()) != 0 and int(add_player_f_age_e.get()) <= 100:

                we_shuttle_connect = sqlite3.connect("WeShuttle.db")
                we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
                we_shuttle_cursor = we_shuttle_connect.cursor()

                try:
                    we_shuttle_cursor.execute("INSERT INTO players_list VALUES (:p_id, :f_name, :l_name, :age, :p_ref)",
                                              {
                                                  'p_id': p_id,
                                                  'f_name': add_player_f_f_name_e.get(),
                                                  'l_name': add_player_f_l_name_e.get(),
                                                  'age': add_player_f_age_e.get(),
                                                  'p_ref': p_id + " " + str(add_player_f_f_name_e.get()) + " " + str(add_player_f_l_name_e.get())
                                              }
                                              )
                    messagebox.showinfo(title="Add New Player", message="Player Added To Records")

                except sqlite3.IntegrityError as err:
                    error_msg = str(err)
                    if error_msg == "UNIQUE constraint failed: players_list.t_p_id":
                        messagebox.showinfo(title="Add New Player",
                                            message="Player With Player Id = " + str(add_player_f_p_id_e.get()) + " Already Exists")

                we_shuttle_connect.commit()
                we_shuttle_connect.close()

                add_player_f_func()

            else:
                messagebox.showinfo(title="Add New Player", message="Player Age Must Be 1-99")

        else:
            messagebox.showinfo(title="Add New Player",
                                message="Player First & Last Names Cannot Be More Than 12 Characters")

    else:
        messagebox.showinfo(title="Add New Player", message="Player ID Must Be 1-99")


def upd_del_result_f_func():
    if upd_del_result_f.sign == ">":
        sel_ref_f_game_result_refresh_func()
        sel_result_f_player_list_refresh_func()
    # Initialize Select Ref Frame
    sel_ref_f_sel_ref.set("")
    # Initialize Select Result Frame
    sel_result_f_venue_e.delete(0, END)
    sel_result_f_a_player_1.set("")
    sel_result_f_a_player_2.set("")
    sel_result_f_a_points_e.delete(0, END)
    sel_result_f_b_player_1.set("")
    sel_result_f_b_player_2.set("")
    sel_result_f_b_points_e.delete(0, END)
    # Hide Select Result Frame
    sel_result_f.grid_remove()
    # Toggle Update Delete Player Frame
    upd_del_result_f.toggle()
    upd_del_result_b.config(text=upd_del_result_f.sign + " Update/Delete Result")


def sel_ref_f_game_result_refresh_func():
    records_all_game_results = all_game_results_func()

    menu_sel_ref = sel_ref_f_sel_ref_om["menu"]
    menu_sel_ref.delete(0, END)
    for option in records_all_game_results:
        menu_sel_ref.add_command(label=option, command=tk._setit(sel_ref_f_sel_ref, option, sel_ref_show_result_func))

    sel_ref_f_sel_ref.set("")


def sel_result_f_player_list_refresh_func():
    records_all_players_list = all_players_list_func()

    menu_a_player_1 = sel_result_f_a_player_1_om["menu"]
    menu_a_player_1.delete(0, END)
    for option in records_all_players_list:
        menu_a_player_1.add_command(label=option, command=tk._setit(sel_result_f_a_player_1, option))

    menu_a_player_2 = sel_result_f_a_player_2_om["menu"]
    menu_a_player_2.delete(0, END)
    for option in records_all_players_list:
        menu_a_player_2.add_command(label=option, command=tk._setit(sel_result_f_a_player_2, option))

    menu_b_player_1 = sel_result_f_b_player_1_om["menu"]
    menu_b_player_1.delete(0, END)
    for option in records_all_players_list:
        menu_b_player_1.add_command(label=option, command=tk._setit(sel_result_f_b_player_1, option))

    menu_b_player_2 = sel_result_f_b_player_2_om["menu"]
    menu_b_player_2.delete(0, END)
    for option in records_all_players_list:
        menu_b_player_2.add_command(label=option, command=tk._setit(sel_result_f_b_player_2, option))


def sel_ref_show_result_func(event):
    we_shuttle_connect = sqlite3.connect("WeShuttle.db")
    we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
    we_shuttle_cursor = we_shuttle_connect.cursor()

    we_shuttle_cursor.execute("SELECT * FROM game_results WHERE t_g_ref = :g_ref",
                              {
                                  'g_ref': sel_ref_f_sel_ref.get(),
                              }
                              )
    record_result = we_shuttle_cursor.fetchall()

    we_shuttle_connect.commit()
    we_shuttle_connect.close()

    try:
        record = record_result[0]

        sel_result_f_venue_e.delete(0, END)
        sel_result_f_a_points_e.delete(0, END)
        sel_result_f_b_points_e.delete(0, END)

        sel_result_f_venue_e.insert(0, record[5])
        sel_result_f_a_player_1.set(record[6])
        sel_result_f_a_player_2.set(record[7])
        sel_result_f_a_points_e.insert(0, record[10])
        sel_result_f_b_player_1.set(record[8])
        sel_result_f_b_player_2.set(record[9])
        sel_result_f_b_points_e.insert(0, record[11])

        sel_result_f.grid(row=1, column=0, sticky=NW)

    except IndexError:
        sel_ref_f_sel_ref.set("")
        sel_result_f_venue_e.delete(0, END)
        sel_result_f_a_points_e.delete(0, END)
        sel_result_f_b_points_e.delete(0, END)

        sel_result_f.grid_remove()
        messagebox.showinfo(title="Select Ref", message="No Such Ref Exists In Record")


def upd_result_func():
    if sel_result_f_a_player_1.get() != sel_result_f_a_player_2.get() and sel_result_f_a_player_1.get() != sel_result_f_b_player_1.get() \
            and sel_result_f_a_player_1.get() != sel_result_f_b_player_2.get() and sel_result_f_a_player_2.get() != sel_result_f_b_player_1.get() \
            and sel_result_f_a_player_2.get() != sel_result_f_b_player_2.get() and sel_result_f_b_player_1.get() != sel_result_f_b_player_2.get():

        try:
            a_points = int(sel_result_f_a_points_e.get())
            b_points = int(sel_result_f_b_points_e.get())

            if a_points != b_points:

                if a_points > b_points:
                    w_player_1 = sel_result_f_a_player_1.get()
                    w_player_2 = sel_result_f_a_player_2.get()
                    point_diff = a_points - b_points

                else:
                    w_player_1 = sel_result_f_b_player_1.get()
                    w_player_2 = sel_result_f_b_player_2.get()
                    point_diff = b_points - a_points

                we_shuttle_connect = sqlite3.connect("WeShuttle.db")
                we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
                we_shuttle_cursor = we_shuttle_connect.cursor()

                we_shuttle_cursor.execute("UPDATE game_results SET "
                                          "t_venue = :venue, t_a_player_1 = :a_player_1, t_a_player_2 = :a_player_2, "
                                          "t_b_player_1 = :b_player_1, t_b_player_2 = :b_player_2, "
                                          "t_a_points = :a_points, t_b_points = :b_points, t_w_player_1 = :w_player_1, "
                                          "t_w_player_2 = :w_player_2, t_point_diff = :point_diff "
                                          "WHERE t_g_ref = :g_ref",
                                          {
                                              'g_ref': sel_ref_f_sel_ref.get(),
                                              'venue': sel_result_f_venue_e.get(),
                                              'a_player_1': sel_result_f_a_player_1.get(),
                                              'a_player_2': sel_result_f_a_player_2.get(),
                                              'b_player_1': sel_result_f_b_player_1.get(),
                                              'b_player_2': sel_result_f_b_player_2.get(),
                                              'a_points': a_points,
                                              'b_points': b_points,
                                              'w_player_1': w_player_1,
                                              'w_player_2': w_player_2,
                                              'point_diff': point_diff
                                          }
                                          )

                we_shuttle_connect.commit()
                we_shuttle_connect.close()

                messagebox.showinfo(title="Update Player", message="Player Details Updated")
                sel_ref_f_sel_ref.set("")
                sel_result_f.grid_remove()

            else:
                messagebox.showinfo(title="Add Game Result", message="Team A & B Points Cannot Be Equal")

        except ValueError as err:
            error_msg = str(err)
            if error_msg == "invalid literal for int() with base 10: ''":
                messagebox.showinfo(title="Update/Delete Game Result", message="Points Field Cannot Be Empty")

    else:
        messagebox.showinfo(title="Add Game Result",
                            message="Players Cannot Be Duplicated Across Teams Or Within A Team")


def del_result_func():
    user_input = messagebox.askokcancel(title="Update/Delete Result", message="Delete Game Result Record ?")

    if user_input:
        we_shuttle_connect = sqlite3.connect("WeShuttle.db")
        we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
        we_shuttle_cursor = we_shuttle_connect.cursor()

        we_shuttle_cursor.execute("DELETE FROM game_results WHERE t_g_ref = :g_ref",
                                  {
                                      'g_ref': sel_ref_f_sel_ref.get(),
                                  }
                                  )

        we_shuttle_connect.commit()
        we_shuttle_connect.close()

        messagebox.showinfo(title="Update/Delete Result", message="Game Result Record Deleted")
        sel_ref_f_game_result_refresh_func()
        sel_result_f.grid_remove()


def upd_del_player_f_func():
    if upd_del_player_f.sign == ">":
        sel_id_f_player_id_refresh_func()
    # Initialize Select Player Frame
    sel_player_f_f_name_e.config(state=NORMAL)
    sel_player_f_l_name_e.config(state=NORMAL)
    sel_player_f_f_name_e.delete(0, END)
    sel_player_f_l_name_e.delete(0, END)
    sel_player_f_age_e.delete(0, END)
    # Initialize Select Id Frame
    sel_id_f_sel_id.set("")
    # Hide Select Player Frame
    sel_player_f.grid_remove()
    # Toggle Update Delete Player Frame
    upd_del_player_f.toggle()
    upd_del_player_b.config(text=upd_del_player_f.sign + " Update/Delete Player")


def sel_id_f_player_id_refresh_func():
    records_all_players_id = all_players_id_func()

    menu_sel_id = sel_id_f_sel_id_om["menu"]
    menu_sel_id.delete(0, END)
    for option in records_all_players_id:
        menu_sel_id.add_command(label=option, command=tk._setit(sel_id_f_sel_id, option, sel_id_show_player_func))

    sel_id_f_sel_id.set("")


def sel_id_show_player_func(event):
    if sel_id_f_sel_id.get() == "W99":
        messagebox.showinfo(title="Update/Delete Player", message="Cannot Update Or Delete Default Player")

    else:
        we_shuttle_connect = sqlite3.connect("WeShuttle.db")
        we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
        we_shuttle_cursor = we_shuttle_connect.cursor()

        we_shuttle_cursor.execute("SELECT * FROM players_list WHERE t_p_id = :p_id",
                                  {
                                      'p_id': sel_id_f_sel_id.get(),
                                  }
                                  )
        record_player = we_shuttle_cursor.fetchall()

        we_shuttle_connect.commit()
        we_shuttle_connect.close()

        try:
            record = record_player[0]
            sel_player_f_f_name_e.config(state=NORMAL)
            sel_player_f_l_name_e.config(state=NORMAL)
            sel_player_f_f_name_e.delete(0, END)
            sel_player_f_l_name_e.delete(0, END)
            sel_player_f_age_e.delete(0, END)
            sel_player_f_f_name_e.insert(0, record[1])
            sel_player_f_l_name_e.insert(0, record[2])
            sel_player_f_age_e.insert(0, record[3])
            sel_player_f_f_name_e.config(state=DISABLED)
            sel_player_f_l_name_e.config(state=DISABLED)

            sel_player_f.grid(row=1, column=0, sticky=NW)

        except IndexError:
            sel_player_f_f_name_e.delete(0, END)
            sel_player_f_l_name_e.delete(0, END)
            sel_player_f_age_e.delete(0, END)

            sel_player_f.grid_remove()
            messagebox.showinfo(title="Select ID", message="No Such ID Exists In Record")


def upd_player_func():
    if len(sel_player_f_f_name_e.get()) <= 12 and len(sel_player_f_l_name_e.get()) <= 12:

        if str(sel_player_f_age_e.get()).isnumeric() and int(sel_player_f_age_e.get()) != 0 and int(sel_player_f_age_e.get()) <= 100:

            we_shuttle_connect = sqlite3.connect("WeShuttle.db")
            we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
            we_shuttle_cursor = we_shuttle_connect.cursor()

            we_shuttle_cursor.execute("UPDATE players_list SET "
                                      "t_f_name = :f_name, t_l_name = :l_name, t_age = :age, t_p_ref = :p_ref "
                                      "WHERE t_p_id = :p_id",
                                      {
                                        'p_id': sel_id_f_sel_id.get(),
                                        'f_name': sel_player_f_f_name_e.get(),
                                        'l_name': sel_player_f_l_name_e.get(),
                                        'age': sel_player_f_age_e.get(),
                                        'p_ref': str(sel_id_f_sel_id.get()) + " " + str(sel_player_f_f_name_e.get()) + " " + str(sel_player_f_l_name_e.get())
                                      }
                                      )

            we_shuttle_connect.commit()
            we_shuttle_connect.close()

            messagebox.showinfo(title="Update Player", message="Player Details Updated")

            sel_id_f_sel_id.set("")
            upd_del_player_f_func()

        else:
            messagebox.showinfo(title="Add New Player", message="Player Age Must Be 1-99")

    else:
        messagebox.showinfo(title="Add New Player",
                            message="Player First & Last Names Cannot Be More Than 12 Characters")


def del_player_func():
    user_input = messagebox.askokcancel(title="Update/Delete Player", message="Delete Player Record ?")

    if user_input:
        we_shuttle_connect = sqlite3.connect("WeShuttle.db")
        we_shuttle_connect.execute("PRAGMA foreign_keys = ON")
        we_shuttle_cursor = we_shuttle_connect.cursor()

        we_shuttle_cursor.execute("DELETE FROM players_list WHERE t_p_id = :p_id",
                                  {
                                      'p_id': sel_id_f_sel_id.get(),
                                  }
                                  )

        we_shuttle_connect.commit()
        we_shuttle_connect.close()
        messagebox.showinfo(title="Update/Delete Player", message="Player Record Deleted")

        sel_id_f_sel_id.set("")
        upd_del_player_f_func()


query_lf = LabelFrame(scrollable_frame, text="Query")
query_lf.grid(row=1, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)

show_players_list_b = Button(query_lf, text="> Show Players List", width=77, command=show_players_list_func, anchor=W)
show_players_list_b.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)
show_game_results_b = Button(query_lf, text="> Show Game Results", width=77, command=show_game_results_f_func, anchor=W)
show_game_results_b.grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)
team_records_b = Button(query_lf, text="> Team Records", width=77, command=team_records_func, anchor=W)
team_records_b.grid(row=4, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)
individual_records_b = Button(query_lf, text="> Individual Records", width=77, command=individual_records_f_func, anchor=W)
individual_records_b.grid(row=6, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)

show_players_list_f = TreeFrame(query_lf, 1, 0)

show_game_results_f = TreeFrame(query_lf, 3, 0)

show_game_results_f_last_ten_res_b = Button\
    (show_game_results_f.frame, text="> Last 10 Results", width=76, command=last_ten_res_func, anchor=W)
show_game_results_f_last_ten_res_b.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NW)
show_game_results_f_all_res_b = Button\
    (show_game_results_f.frame, text="> All Results", width=76, command=all_res_func, anchor=W)
show_game_results_f_all_res_b.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NW)

last_ten_res_f = TreeFrame(show_game_results_f.frame, 1, 0)
all_res_f = TreeFrame(show_game_results_f.frame, 3, 0)

team_records_f = TreeFrame(query_lf, 5, 0)
individual_records_f = TreeFrame(query_lf, 7, 0)


commands_lf = LabelFrame(scrollable_frame, text="Commands")
commands_lf.grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)

add_result_b = Button(commands_lf, text="> Add Game Result", width=77, command=add_result_f_func, anchor=W)
add_result_b.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)
add_player_b = Button(commands_lf, text="> Add New Player", width=77, command=add_player_f_func, anchor=W)
add_player_b.grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)
upd_del_result_b = Button(commands_lf, text="> Update/Delete Game Result", width=77,
                          command=upd_del_result_f_func, anchor=W)
upd_del_result_b.grid(row=4, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)
upd_del_player_b = Button(commands_lf, text="> Update/Delete Player", width=77, command=upd_del_player_f_func, anchor=W)
upd_del_player_b.grid(row=6, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky=NW)

add_result_f = TreeFrame(commands_lf, 1, 0)

add_result_f_date_d = DropDate(add_result_f.frame)
add_result_f_date_d.year_l.grid(row=2, column=0, padx=5, pady=0, ipadx=2, ipady=2)
add_result_f_date_d.month_l.grid(row=3, column=0, padx=5, pady=0, ipadx=2, ipady=2)
add_result_f_date_d.date_l.grid(row=4, column=0, padx=5, pady=0, ipadx=2, ipady=2)
add_result_f_date_d.year_om.grid(row=2, column=1, padx=0, pady=0, ipadx=2, ipady=2, sticky=EW)
add_result_f_date_d.month_om.grid(row=3, column=1, padx=0, pady=0, ipadx=2, ipady=2, sticky=EW)
add_result_f_date_d.date_om.grid(row=4, column=1, padx=0, pady=0, ipadx=2, ipady=2, sticky=EW)

add_result_f_g_id_l = Label(add_result_f.frame, text="Game Id", width=12, anchor=W)
add_result_f_g_id_l.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2)

add_result_f_g_id_e = Entry(add_result_f.frame, width=12)
add_result_f_g_id_e.grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=EW)

add_result_f_venue_l = Label(add_result_f.frame, text="Venue", width=12, anchor=W)
add_result_f_venue_l.grid(row=1, column=0, padx=5, pady=5, ipadx=2, ipady=2)

add_result_f_venue_e = Entry(add_result_f.frame, width=24)
add_result_f_venue_e.grid(row=1, column=1, padx=5, pady=5, ipadx=2, ipady=2, columnspan=2, sticky=EW)

add_result_f_player_1_l = Label(add_result_f.frame, text="Player 1", width=12, anchor=W)
add_result_f_player_1_l.grid(row=6, column=0, padx=5, pady=5, ipadx=2, ipady=2)

add_result_f_player_2_l = Label(add_result_f.frame, text="Player 2", width=12, anchor=W)
add_result_f_player_2_l.grid(row=7, column=0, padx=5, pady=5, ipadx=2, ipady=2)

add_result_f_team_a_l = Label(add_result_f.frame, text="Team A", width=12, anchor=W)
add_result_f_team_a_l.grid(row=5, column=1, padx=0, pady=0, ipadx=2, ipady=2)

add_result_f_team_b_l = Label(add_result_f.frame, text="Team B", width=12, anchor=W)
add_result_f_team_b_l.grid(row=5, column=3, padx=0, pady=0, ipadx=2, ipady=2)

add_result_f_points_l = Label(add_result_f.frame, text="Points", width=12, anchor=W)
add_result_f_points_l.grid(row=8, column=0, padx=5, pady=5, ipadx=2, ipady=2)

add_result_f_a_points_e = Entry(add_result_f.frame, width=12, justify=RIGHT)
add_result_f_a_points_e.grid(row=8, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=EW)

add_result_f_b_points_e = Entry(add_result_f.frame, width=12, justify=RIGHT)
add_result_f_b_points_e.grid(row=8, column=4, padx=5, pady=5, ipadx=2, ipady=2, sticky=EW)

add_result_f_add_res_b = Button(add_result_f.frame, text="Add Result", width=48, command=add_result_func, anchor=CENTER)
add_result_f_add_res_b.grid(row=9, column=1, padx=5, pady=10, ipadx=2, ipady=2, columnspan=4)


all_players_list = all_players_list_func()
add_result_f_a_player_1 = StringVar()
add_result_f_a_player_1_om = OptionMenu(add_result_f.frame, add_result_f_a_player_1, *all_players_list)
add_result_f_a_player_1_om.grid(row=6, column=1, padx=0, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)
add_result_f_a_player_2 = StringVar()
add_result_f_a_player_2_om = OptionMenu(add_result_f.frame, add_result_f_a_player_2, *all_players_list)
add_result_f_a_player_2_om.grid(row=7, column=1, padx=0, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)
add_result_f_b_player_1 = StringVar()
add_result_f_b_player_1_om = OptionMenu(add_result_f.frame, add_result_f_b_player_1, *all_players_list)
add_result_f_b_player_1_om.grid(row=6, column=3, padx=0, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)
add_result_f_b_player_2 = StringVar()
add_result_f_b_player_2_om = OptionMenu(add_result_f.frame, add_result_f_b_player_2, *all_players_list)
add_result_f_b_player_2_om.grid(row=7, column=3, padx=0, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)


add_player_f = TreeFrame(commands_lf, 3, 0)
# P_Id
add_player_f_p_id_l = Label(add_player_f.frame, text="Player ID", width=12, anchor=W)
add_player_f_p_id_l.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
add_player_f_p_id_e = Entry(add_player_f.frame, width=30)
add_player_f_p_id_e.grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
# First Name
add_player_f_f_name_l = Label(add_player_f.frame, text="First Name", width=12, anchor=W)
add_player_f_f_name_l.grid(row=1, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
add_player_f_f_name_e = Entry(add_player_f.frame, width=30)
add_player_f_f_name_e.grid(row=1, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
add_player_f_f_name_max_l = Label(add_player_f.frame, text="(Max 12 Char)", width=12, anchor=W)
add_player_f_f_name_max_l.grid(row=1, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
# Last Name
add_player_f_l_name_l = Label(add_player_f.frame, text="Last Name", width=12, anchor=W)
add_player_f_l_name_l.grid(row=2, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
add_player_f_l_name_e = Entry(add_player_f.frame, width=30)
add_player_f_l_name_e.grid(row=2, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
add_player_f_l_name_max_l = Label(add_player_f.frame, text="(Max 12 Char)", width=12, anchor=W)
add_player_f_l_name_max_l.grid(row=2, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
# Age
add_player_f_age_l = Label(add_player_f.frame, text="Age", width=12, anchor=W)
add_player_f_age_l.grid(row=3, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
add_player_f_age_e = Entry(add_player_f.frame, width=30)
add_player_f_age_e.grid(row=3, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
# Add Player
add_player_f_add_player_b = Button(add_player_f.frame, text="Add Player", width=20,
                                   command=add_player_func, anchor=CENTER)
add_player_f_add_player_b.grid(row=4, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=N)


upd_del_result_f = TreeFrame(commands_lf, 5, 0)

# Select ID
sel_ref_f = Frame(upd_del_result_f.frame)

sel_ref_f_sel_ref_l = Label(sel_ref_f, text="Select Ref", width=12, anchor=W)
sel_ref_f_sel_ref_l.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=W)
all_game_results = all_game_results_func()
sel_ref_f_sel_ref = StringVar()
sel_ref_f_sel_ref_om = OptionMenu(sel_ref_f, sel_ref_f_sel_ref, *all_game_results, command=sel_ref_show_result_func)
sel_ref_f_sel_ref_om.grid(row=0, column=1, padx=3, pady=5, ipadx=2, ipady=2, sticky=EW)
sel_ref_f_empty_1_1_l = Label(sel_ref_f, text="", width=27, anchor=W)
sel_ref_f_empty_1_1_l.grid(row=1, column=1, padx=0, pady=0, ipadx=2, ipady=2, sticky=W)


sel_ref_f.grid(row=0, column=0, sticky=NW)

sel_result_f = Frame(upd_del_result_f.frame)

sel_result_f_venue_l = Label(sel_result_f, text="Venue", width=12, anchor=W)
sel_result_f_venue_l.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2)
sel_result_f_a_player_1_l = Label(sel_result_f, text="Team A Player 1", width=12, anchor=W)
sel_result_f_a_player_1_l.grid(row=1, column=0, padx=5, pady=5, ipadx=2, ipady=2)
sel_result_f_a_player_2_l = Label(sel_result_f, text="Team A Player 2", width=12, anchor=W)
sel_result_f_a_player_2_l.grid(row=2, column=0, padx=5, pady=5, ipadx=2, ipady=2)
sel_result_f_a_points_l = Label(sel_result_f, text="Team A Points", width=12, anchor=W)
sel_result_f_a_points_l.grid(row=3, column=0, padx=5, pady=5, ipadx=2, ipady=2)
sel_result_f_b_player_1_l = Label(sel_result_f, text="Team B Player 1", width=12, anchor=W)
sel_result_f_b_player_1_l.grid(row=4, column=0, padx=5, pady=5, ipadx=2, ipady=2)
sel_result_f_b_player_2_l = Label(sel_result_f, text="Team B Player 2", width=12, anchor=W)
sel_result_f_b_player_2_l.grid(row=5, column=0, padx=5, pady=5, ipadx=2, ipady=2)
sel_result_f_b_points_l = Label(sel_result_f, text="Team B Points", width=12, anchor=W)
sel_result_f_b_points_l.grid(row=6, column=0, padx=5, pady=5, ipadx=2, ipady=2)


sel_result_f_venue_e = Entry(sel_result_f, width=30)
sel_result_f_venue_e.grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)

all_players_list = all_players_list_func()
sel_result_f_a_player_1 = StringVar()
sel_result_f_a_player_1_om = OptionMenu(sel_result_f, sel_result_f_a_player_1, *all_players_list)
sel_result_f_a_player_1_om.grid(row=1, column=1, padx=3, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)
sel_result_f_a_player_2 = StringVar()
sel_result_f_a_player_2_om = OptionMenu(sel_result_f, sel_result_f_a_player_2, *all_players_list)
sel_result_f_a_player_2_om.grid(row=2, column=1, padx=3, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)

sel_result_f_a_points_e = Entry(sel_result_f, width=12, justify=RIGHT)
sel_result_f_a_points_e.grid(row=3, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=E)

sel_result_f_b_player_1 = StringVar()
sel_result_f_b_player_1_om = OptionMenu(sel_result_f, sel_result_f_b_player_1, *all_players_list)
sel_result_f_b_player_1_om.grid(row=4, column=1, padx=3, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)
sel_result_f_b_player_2 = StringVar()
sel_result_f_b_player_2_om = OptionMenu(sel_result_f, sel_result_f_b_player_2, *all_players_list)
sel_result_f_b_player_2_om.grid(row=5, column=1, padx=3, pady=5, ipadx=2, ipady=2, sticky=EW, columnspan=2)

sel_result_f_b_points_e = Entry(sel_result_f, width=12, justify=RIGHT)
sel_result_f_b_points_e.grid(row=6, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=E)
# Update Result
upd_result_b = Button(sel_result_f, text="Update Result", width=20, command=upd_result_func, anchor=CENTER)
upd_result_b.grid(row=7, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=N)
# Delete Result
del_result_b = Button(sel_result_f, text="Delete Result", width=20, command=del_result_func, anchor=CENTER)
del_result_b.grid(row=8, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=N)


upd_del_player_f = TreeFrame(commands_lf, 7, 0)

# Select ID
sel_id_f = Frame(upd_del_player_f.frame)

sel_id_f_sel_id_l = Label(sel_id_f, text="Select ID", width=12, anchor=W)
sel_id_f_sel_id_l.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=W)
all_players_id = all_players_id_func()
sel_id_f_sel_id = StringVar()
sel_id_f_sel_id_om = OptionMenu(sel_id_f, sel_id_f_sel_id, *all_players_id, command=sel_id_show_player_func)
sel_id_f_sel_id_om.grid(row=0, column=1, padx=3, pady=5, ipadx=2, ipady=2, sticky=EW)
sel_id_f_empty_1_1_l = Label(sel_id_f, text="", width=27, anchor=W)
sel_id_f_empty_1_1_l.grid(row=1, column=1, padx=0, pady=0, ipadx=2, ipady=2, sticky=W)


sel_id_f.grid(row=0, column=0, sticky=NW)

sel_player_f = Frame(upd_del_player_f.frame)

sel_player_f_f_name_l = Label(sel_player_f, text="First Name", width=12, anchor=W)
sel_player_f_f_name_l.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_f_name_max_l = Label(sel_player_f, text="(Max 12 Char)", width=12, anchor=W)
sel_player_f_f_name_max_l.grid(row=0, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_l_name_l = Label(sel_player_f, text="Last Name", width=12, anchor=W)
sel_player_f_l_name_l.grid(row=1, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_l_name_max_l = Label(sel_player_f, text="(Max 12 Char)", width=12, anchor=W)
sel_player_f_l_name_max_l.grid(row=1, column=2, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_age_l = Label(sel_player_f, text="Age", width=12, anchor=W)
sel_player_f_age_l.grid(row=2, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_f_name_e = Entry(sel_player_f, width=30)
sel_player_f_f_name_e.grid(row=0, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_l_name_e = Entry(sel_player_f, width=30)
sel_player_f_l_name_e.grid(row=1, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
sel_player_f_age_e = Entry(sel_player_f, width=30)
sel_player_f_age_e.grid(row=2, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=NW)
# Update Player
upd_player_b = Button(sel_player_f, text="Update Player", width=20, command=upd_player_func, anchor=CENTER)
upd_player_b.grid(row=3, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=N)
# Delete Player
del_player_b = Button(sel_player_f, text="Delete Player", width=20, command=del_player_func, anchor=CENTER)
del_player_b.grid(row=4, column=1, padx=5, pady=5, ipadx=2, ipady=2, sticky=N)


root.mainloop()
