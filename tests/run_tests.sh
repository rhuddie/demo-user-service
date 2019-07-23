#!/bin/sh
pytest ./tests/py/test_rest_api.py
behave ./tests/py/ui/features
cucumber ./tests/rb/features/
