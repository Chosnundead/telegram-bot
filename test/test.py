#####################
# !!!Import tic_tac_toe.py from this dir!!!
# from pathlib import Path
# import importlib
# import sys

# path = Path(__file__).parents[1]
# spec = importlib.util.spec_from_file_location(
#     "tic_tac_toe", "{}\\modules\\tic_tac_toe.py".format(path).replace("\\", "/")
# )
# tic_tac_toe = importlib.util.module_from_spec(spec)
# sys.modules["tic_tac_toe"] = tic_tac_toe
# spec.loader.exec_module(tic_tac_toe)

# game = tic_tac_toe.Game()
# game.start()
#####################
# import sqlite3 as sq
# import pathlib

# pathToDB = "{}\\db\\test.db".format(pathlib.Path(__file__).parents[0])
# with sq.connect(pathToDB) as db:
#     cursor = db.cursor()
#     cursor.execute(
#         """CREATE TABLE IF NOT EXISTS users (
#         id INTEGER NOT NULL PRIMARY KEY,
#         query TEXT
#     )"""
#     )
#####################
