#!/usr/bin/env bash
##
##
me="${0##*/}"
#
if [[ -z $1 ]]; then
    echo "Usage: $me <newday>" 1>&2
    echo "Example: $me 20" 1>&2
    exit 1
fi

newday=$1
src="src/day${newday}.py"
if [[ -f "${src}" ]]; then
    echo "WARNING: ${src} already exists" 1>&2
else
    cp "template/src/day00.py" "${src}"
    sed -i "" "s/00/${newday}/" "${src}"
    echo "Created ${src}"
fi

test="tests/test_day${newday}.py"
if [[ -f "${test}" ]]; then
    echo "WARNING: ${test} already exists" 1>&2
else
    cp "template/tests/test_day00.py" "${test}"
    sed -i "" "s/00/${newday}/" "${test}"
    echo "Created ${test}"
fi

touch "data/day${newday}.txt" "data/day${newday}_test0.txt"
