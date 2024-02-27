#!/bin/bash

# Remove any previous executable
rm -f ./a.out

# Compile the uploaded C++ program (assumed to be saved as uploads/walk.cc)
g++ uploads/walk.cc -o ./a.out
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# Assuming test.sh is your script that tests the compiled program
# Execute the test script and capture its outcome
./test.sh > output.txt
retcode=$?

# Assuming the test script updates the score based on the program's output correctness
echo "Score: $retcode out of 2 correct."

# Optionally, display the original submission
echo "*************Original submission*************"
cat uploads/walk.cc

# Exit with the score (retcode) if needed
exit $retcode

