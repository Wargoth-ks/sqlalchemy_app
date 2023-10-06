import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import subprocess
import time
import logging

from prompt_toolkit import prompt

from models import Base
from sqlalchemy.exc import OperationalError, DatabaseError, DisconnectionError

from settings.db import engine, db_user, db_password, db_name
from settings.db import engine
from seed import insert_data

from hello import hello
from my_select import *


def run_docker():
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            "container",
            "-p",
            "5432:5432",
            "-e",
            f"POSTGRES_USER={db_user}",
            "-e",
            f"POSTGRES_PASSWORD={db_password}",
            "-e",
            f"POSTGRES_DB={db_name}",
            "-v",
            "/mnt/docker/volumes/db_vol:/var/lib/postgresql/data",
            "-d",
            "postgres:alpine",
        ]
    )


def wait_for_db():
    while True:
        try:
            engine.connect()
            # Base.metadata.create_all(engine)
            break
        except OperationalError:
            print("Waiting for database...")
            time.sleep(1)


def main():
    while True:
        hello()
        try:
            user_input = int(prompt("\nEnter number: ", default=""))
            match user_input:
                case 0:
                    engine.dispose()
                    time.sleep(3)
                    subprocess.run(["docker", "stop", "container"])
                    print("\nStop & delete container")
                    print("\nExit program\n")
                    sys.exit()
                case n if n in range(1, 11):
                    res = globals()[f"select_{n}"]()
                    print("\n" + f"{res}")
                case "":
                    print("\nCommand not found!")
                case _:
                    print("\nPlease, enter number from 0 to 10")
        except ValueError:
            print("\n" + "Please, enter number from 0 to 10")


if __name__ == "__main__":
    try:
        run_docker()
        print("\nDocker is starting...\n")
        wait_for_db()
        print("\nDone! Docker is running!\n")
        time.sleep(2)
        # insert_data()
        main()
    except DatabaseError as e:
        print(f"{e}")
    except DisconnectionError as d:
        raise DisconnectionError(f"Disconnect Error: {d}")
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt: exit program")
    finally:
        subprocess.run(["docker", "rm", "-f", "container"])
