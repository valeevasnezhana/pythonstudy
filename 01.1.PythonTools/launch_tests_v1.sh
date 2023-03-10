echo $'3 3\n1 2 3\n4 5 6\n7 8 9\n' | ./compile_then_execute.sh | grep -xc $'1 6 7\n2 5 8\n3 4 9\n\n1 2 3\n6 5 4\n7 8 9' | grep -xc '7'
echo $'2 4\n1 2 3 4\n5 6 7 8\n' | ./compile_then_execute.sh | grep -xc $'1 4 5 8\n2 3 6 7\n\n1 2 3 4\n8 7 6 5\n' | grep -xc '5'
echo $'0 0' | ./compile_then_execute.sh | grep -xc $'n/a' | grep -xc '1'
echo $'3 3\n-1 -2 -3\n-4 -5 -6\n-7 -8 -9\n' | ./compile_then_execute.sh | grep -xc $'\-9 \-4 \-3\n\-8 \-5 \-2\n\-7 \-6 \-1\n\n-9 \-8 \-7\n\-4 \-5 \-6\n\-3 \-2 \-1' | grep -xc '7'
