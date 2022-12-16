.PHONY: clean install_test test load_test docker_image

clean:
	find . -name '*.py[co]' -delete
	rm -rf build
	rm -rf *.egg-info
	rm -rf venv
	rm -rf .pytest_cache


install_test:
	virtualenv -p python3 --prompt '|> iotsink <| ' venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install pytest
	venv/bin/pip install locust
	@echo
	@echo "VirtualENV Setup Complete. Now run: source venv/bin/activate"


test:
	pytest -rA tests/


load_test:
	locust --headless -f load_tests/smoke_test.py -H http://127.0.0.1:1095
	locust --headless -f load_tests/load_test.py -H http://127.0.0.1:1095
	locust --headless -f load_tests/stress_test.py -H http://127.0.0.1:1095
	locust --headless -f load_tests/spike_test.py -H http://127.0.0.1:1095
	locust --headless -f load_tests/soak_test.py -H http://127.0.0.1:1095

mUID:=$(shell id -u)
mGID:=$(shell id -g)


docker_image:
	docker build --build-arg UID=$(mUID) --build-arg GID=$(mGID) -t iotsink:latest .


