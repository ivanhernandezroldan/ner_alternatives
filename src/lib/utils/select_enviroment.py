import os
from dotenv import load_dotenv

enviroment_files = {
    "default": ".env",
}

ROOT_DIR = os.path.dirname(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)


def select_enviroment(user="default"):
    if user in enviroment_files:
        env_dir = os.path.join(ROOT_DIR, enviroment_files[user])
        print(f"Selected enviroment: {env_dir}")
        load_dotenv(dotenv_path=env_dir, override=True)
    else:
        raise ValueError(f"Invalid user: {user}")
