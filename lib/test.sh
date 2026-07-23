#! /usr/bin/env bash

# Install pytest if needed
pip install pytest

# Run tests
pytest test_random_unique_generator.py -v
