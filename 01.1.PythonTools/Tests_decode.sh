## —- encode —-
echo "W O R L D" | ./compile_then_execute.sh 0 | grep -xc "57 4F 52 4C 44"
echo "w o r l d" | ./compile_then_execute.sh 0 | grep -xc "77 6F 72 6C 64"
echo "w o r L D" | ./compile_then_execute.sh 0 | grep -xc "77 6F 72 4C 44"
echo "W O R LD" | ./compile_then_execute.sh 0 | grep -xc "57 4F 52 n/a"
echo "WO RLD" | ./compile_then_execute.sh 0 | grep -xc "n/a"
echo "WO RLD" | ./compile_then_execute.sh 0 | grep -xc "n/a"
echo "H e l l o , w o r l d :" | ./compile_then_execute.sh 0 | grep -xc "48 65 6C 6C 6F 2C 77 6F 72 6C 64 3A"
echo "@ H e @ l l o w o r l d : 2 3" | ./compile_then_execute.sh 0 | grep -xc "40 48 65 40 6C 6C 6F 77 6F 72 6C 64 3A 32 33"

# —- decode —-
echo "48 45 4C 4C 4F" | ./compile_then_execute.sh 1 | grep -xc "H E L L O"
echo "48 45 4C4C" | ./compile_then_execute.sh 1 | grep -xc "H E n/a"
echo "48 45 4C 4C 4F 77 4F 52 4C 44" | ./compile_then_execute.sh 1 | grep -xc "H E L L O w O R L D"
echo "48454C4C4F" | ./compile_then_execute.sh 1 | grep -xc "n/a"
echo "48 65 6C 6C 6F 2C 20 77 6F 72 6C 64 3A" | ./compile_then_execute.sh 1 | grep -xc "H e l l o , w o r l d :"
echo "48 65 6C 6C 6F 2C 20 20 20 77 6F 72 6C 64 3A" | ./compile_then_execute.sh 1 | grep -xc "H e l l o , w o r l d :"
echo "40 48 65 40 6C 6C 6F 77 6F 72 6C 64 3A 32 33" | ./compile_then_execute.sh 1 | grep -xc "@ H e @ l l o w o r l d : 2 3"
