# —- decode —-
echo "48 45 4C 4C 4F" | ./compile_then_execute.sh 1 | grep -xc "H E L L O"
echo "48454C4C4F" | ./compile_then_execute.sh 1 | grep -xc "n/a"

## —- encode —-
echo "W O R L D" | ./compile_then_execute.sh 0 | grep -xc "57 4F 52 4C 44"
echo "WORLD" | ./compile_then_execute.sh 0 | grep -xc "n/a"
echo "WO RLD" | ./compile_then_execute.sh 0 | grep -xc "n/a"
echo "WO RLD" | ./compile_then_execute.sh 0 | grep -xc "n/a"
