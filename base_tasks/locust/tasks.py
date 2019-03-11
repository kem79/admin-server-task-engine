from task_engine import app


@app.task
def start_locust():
    print("start locust!")
