from flask import Flask, render_template, request, json
import configparser

from setup_logging import logger
from werkzeug.exceptions import HTTPException
import pathlib
from typing import Tuple
from src.fernet_cipher import FernetCipher, Fernet
from src.directions import Directions
from src.simple_server_utilities import split_coordinates
from src.maze import Maze

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
@app.route('/start.html', methods=["GET", "POST"])
def start() -> Tuple[str, int]:
    title = "Maze Start"
    if request.method == "GET":
        logger.info("GET method displays start page")
    if request.method == "POST":
        if request.form['submit_button'] == "save_maze":
            logger.info("save button clicked")
            maze.save_maze()
            logger.info("save completed")
        if request.form['submit_button'] == "load_maze":
            logger.info("load button clicked")
            maze.load_maze()
            logger.info("load completed")
    return render_template(
        'start.html',
        hostname=request.host,
        start_url=maze._start_url,
        title_text=title
    ), 200


@app.route('/maze/<coordinates>')
def show_room(coordinates: bytes | str) -> Tuple[str, int]:
    cipher = Fernet(secret_key)
    coordinates = cipher.decrypt(coordinates).decode()
    x, y, z = split_coordinates(coordinates)
    title = "Maze Room"
    logger.info(f"showing room {x} {y} {z}")
    return (
        render_template(
            'room.html',
            title_text=title,
            hostname=request.host,
            roomname=maze.get_room(x, y, z).get_formatted_room_name(True),
            exits=maze.get_room(x, y, z).get_formatted_exits(True)),
        200
    )   


@app.errorhandler(HTTPException)
def handle_exception(e) -> str:
    # start with the correct headers and status code from the error
    response = e.get_response()
    if e.code == 404:
        return render_template("404.html")
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(pathlib.Path(__file__).parent.parent / "config" / "maze.ini")
    simple_server_logger = logger
    secret_key = Fernet.generate_key()
    fernet_cipher = FernetCipher(secret_key, logger)
    these_directions = Directions(logger)

    maze_name, maze_file_name = config["DEFAULT"]["MazeName"], config["DEFAULT"]["MazeFile"]
    default_x_start, default_y_start, default_z_start = [int(config["DEFAULT"][f"{v}_start"]) for v in ["x", "y", "z"]]
    default_xbound, default_ybound, default_zbound = [int(config["DEFAULT"][f"{v}bound"]) for v in ["x", "y", "z"]]
    maze = Maze(
        maze_name,
        maze_file_name,
        these_directions,
        fernet_cipher,
        logger,
        request,
        default_x_start,
        default_y_start,
        default_z_start,
        default_xbound,
        default_ybound,
        default_zbound
    )
    maze.build_maze_automatically()
    app.run(host='0.0.0.0', port=8080, debug=False)
