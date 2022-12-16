
# IOTsink

server app that acts as a message sink

fastapi app exposed on gunicorn running uvicorn workers


### test
```
make install_test

source venv/bin/activate

make test
```
#### run individual test eg.
```
pytest -rA tests/test_config.py
```

### load test
```
make docker_image
./run_container.sh

make install_test

source venv/bin/activate

make load_test
```
#### run individual load test eg.
```
locust -f load_tests/load_test.py -H http://127.0.0.1:1095
hit http://127.0.0.1:8089/
```


### drone
```
edit .drone.yml workspace path, set to project pwd
```


### configuration file:
#### .env
```
cp envs/env_sample envs/.env
```
#### handler.json sample
```
{
	"info": 
	[
		"ExampleDBPlugin"
	],
	"event":
    [
		"ExampleElasticsearchPlugin",
		"ExampleKafkaPlugin",
		"ExampleRedisPlugin"
	],
    "load_test":
	[
		"LoadTestPlugin"
	]
}
```
#### plugins.json sample
```
{
    "ExampleDBPlugin" :
    {
        "config":
        {
            "databases":
            [
                "dev_db"
            ]
        } 
    },
    "ExampleKafkaPlugin" :
    {
        "config": 
        {
            "topic": "dev_event_topic"
        }
    },
    "ExampleRedisPlugin" :
    {
        "config":
        {
            "connections":
            [
                "dev"
            ],
            "expire_seconds": 60
        }
    },
    "ExampleElasticsearchPlugin" :
    {
        "config":
        {
            "connections":
            [
                "dev"
            ]
        } 
    },
    "LoadTestPlugin" :
    {
        "config": {} 
    }
}
```

### deployment


#### docker

```
make docker_image

run: ./run_container.sh
```

### fastapi docs
```
http://127.0.0.1:1095/docs
```

### sink samples

#### info
```
curl --header "Content-Type: application/json" --request POST --data '{"type": "info", "source": "MY_SOURCE", "data": {"Temperature": 30, "Humidity": 50, "Light": 90}}' http://127.0.0.1:1095/route
```

#### event
```
curl --header "Content-Type: application/json" --request POST --data '{"type": "event", "source": "MY_SOURCE", "data": {"movement": "true"}}' http://127.0.0.1:1095/route
```

