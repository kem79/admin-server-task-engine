"""
a module to hold sanity test tasks.
"""
from app.task_engine import app


@app.task
def hello(world):
    """
    a sanity check method to verify integration with administration server

    :type world: str
    :param world: a string to save in the backend
    :return: the world string
    """
    return world
