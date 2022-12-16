from locust import HttpUser, TaskSet, task, constant, events, LoadTestShape



@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0



class PostUserTasks(TaskSet):
    @task
    def test(self):
        json = {"type": "load_test", "source": "load_tester", "data": {"cpu": 100, "io": 0.04}}
        self.client.post(url='/load_test', json=json)


class PostUser(HttpUser):
    wait_time = constant(0.5)
    tasks = [PostUserTasks]


class StressShape(LoadTestShape):

    time_limit = 100

    stages = [
        {"duration": 20, "users": 25, "spawn_rate": 2},
        {"duration": 30, "users": 40, "spawn_rate": 12},
        {"duration": 40, "users": 60, "spawn_rate": 12},
        {"duration": 50, "users": 2, "spawn_rate": 12}
    ]

    def tick(self):

        run_time = self.get_run_time()

        if run_time < self.time_limit:

            for stage in self.stages:

                if run_time < stage["duration"]:
                    return (stage["users"], stage["spawn_rate"])

        return None



