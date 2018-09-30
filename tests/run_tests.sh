#!/bin/sh
pytest ./tests/test_rest_api.py
behave ./tests/ui/features
