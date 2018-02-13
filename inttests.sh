#!/usr/local/bin/bash
#Integration Tests for Bookworm Solver
#Change the shebang line to point to your bash binary. 
testpath=tests

a=$(ls $testpath | grep "^test[0-9]" | grep -E -o "[0-9]+")
ec=0

for i in $a; do
    python3 bookworm_solver.py < "$testpath/test$i" > "$testpath/temp$i"
    if ! $(diff "$testpath/temp$i" "$testpath/answer$i"); then
        echo "test$i failed. "
        let "ec++"
    fi
done

rm -f $testpath/temp*

exit $ec