from locust import HttpUser, TaskSet, task, constant, events, LoadTestShape


@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
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


class SmokeShape(LoadTestShape):

    time_limit = 10
    spawn_rate = 1
    user_count = 1

    def tick(self):

        run_time = self.get_run_time()

        if run_time < self.time_limit:
            return (self.user_count, self.spawn_rate)

        return None



