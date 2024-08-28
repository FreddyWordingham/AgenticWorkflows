#!/bin/bash
set -e

# Run the radon command and capture the output
OUTPUT=$(poetry run radon cc agentic_workflows -a)

# Print all output
echo "$OUTPUT"

# Extract the complexity score using sed
COMPLEXITY_SCORE=$(echo "$OUTPUT" | sed -n "s/^Average complexity: \([A-Z]\).*/\1/p")

# Print the complexity score
echo $COMPLEXITY_SCORE
