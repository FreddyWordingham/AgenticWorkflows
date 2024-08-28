#!/bin/bash
set -e

poetry run black --check --diff agentic_workflows
