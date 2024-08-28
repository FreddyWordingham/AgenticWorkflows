#!/bin/bash
set -e

# Get the version number from the pyproject.toml file
VERSION=$(grep -m 1 "^version" pyproject.toml | sed 's/version = "\(.*\)"/\1/')

# Print the captured version number
echo "The version number is: $VERSION"


# Update the README.md file with the version number
LINE="![Version Badge](https://img.shields.io/badge/version-"
ESCAPED_LINE=$(echo "$LINE" | sed 's/[^^]/[&]/g; s/\^/\\^/g')
REPLACEMENT="${LINE}${VERSION}-gold)"
sed "s|^$ESCAPED_LINE.*|$REPLACEMENT|" "README.md" > /tmp/tempfile && mv /tmp/tempfile "README.md"

# Run the calculate_complexity.sh script and capture its output
COMPLEXITY_OUTPUT=$(sh ./ci/calculate_complexity.sh)
COMPLEXITY_SCORE=$(echo "$COMPLEXITY_OUTPUT" | tail -n 1)

# Print the captured complexity score
echo "The captured complexity score is: $COMPLEXITY_SCORE"


# Update the README.md file with the complexity score
LINE="![Complexity Badge](https://img.shields.io/badge/complexity-"
ESCAPED_LINE=$(echo "$LINE" | sed 's/[^^]/[&]/g; s/\^/\\^/g')
REPLACEMENT="${LINE}${COMPLEXITY_SCORE}-cyan)"
sed "s|^$ESCAPED_LINE.*|$REPLACEMENT|" "README.md" > /tmp/tempfile && mv /tmp/tempfile "README.md"


# Run the calculate_maintainability.sh script and capture its output
MAINTAINABILITY_OUTPUT=$(sh ./ci/calculate_maintainability.sh)
MAINTAINABILITY_SCORE=$(echo "$MAINTAINABILITY_OUTPUT" | tail -n 1)

# Print the captured maintainability score
echo "The captured maintainability score is: $MAINTAINABILITY_SCORE"

# Update the README.md file with the maintainability score
LINE="![Maintainability Badge](https://img.shields.io/badge/maintainability-"
ESCAPED_LINE=$(echo "$LINE" | sed 's/[^^]/[&]/g; s/\^/\\^/g')
REPLACEMENT="${LINE}${MAINTAINABILITY_SCORE}%25-blue)"
sed "s|^$ESCAPED_LINE.*|$REPLACEMENT|" "README.md" > /tmp/tempfile && mv /tmp/tempfile "README.md"


# Run the calcualte_coverage.sh script and capture its output
COVERAGE_OUTPUT=$(sh ./ci/calculate_coverage.sh)
COVERAGE_PERCENT=$(echo "$COVERAGE_OUTPUT" | tail -n 1)

# Print the captured coverage percentage
echo "The captured coverage percentage is: $COVERAGE_PERCENT"

# Update the README.md file with the coverage percentage
LINE="![Coverage Badge](https://img.shields.io/badge/test_coverage-"
ESCAPED_LINE=$(echo "$LINE" | sed 's/[^^]/[&]/g; s/\^/\\^/g')
REPLACEMENT="${LINE}${COVERAGE_PERCENT}%25-brightgreen)"
sed "s|^$ESCAPED_LINE.*|$REPLACEMENT|" "README.md" > /tmp/tempfile && mv /tmp/tempfile "README.md"
