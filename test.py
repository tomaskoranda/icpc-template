"""
Test a program given a folder, 
by scanning the folder for pairs of `.in` and `.ans` files,
and comparing the output of the program with the `.ans` files.
"""
import os
import argparse
import filecmp

################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("--path", required=True, help="Problem folder, containing both program and test files")
parser.add_argument("--py", default=False, action="store_true", help="Run python3")
parser.add_argument("--cpp", default=False, action="store_true", help="Run c++")

if __name__ == "__main__":
    # 0. Parse arguments
    args = parser.parse_args([] if "__file__" not in globals() else None)
    assert args.py ^ args.cpp, "Select Python or C++, not both"

    # 1. Parse input and answer files (does not check for pair correspondence)
    inputs, answers = [], []
    for f in sorted(os.listdir(args.path)):
        f = os.path.join(args.path, f)
        if f.endswith(".in"):
            inputs.append(f)
        if f.endswith(".ans"):
            answers.append(f)

    # 2. Get the executable file
    if args.cpp:
        compile_cmd = f'g++ -std=c++17 -pedantic -Wall -Wextra -o "{args.path}/a.out" "{args.path}/main.cpp"'
        os.system(compile_cmd)
        cmd = f'"{args.path}/a.out" '
    if args.py:
        cmd = f'python3  "{args.path}/main.py" '

    print(f"\n{'':_^80}\n")

    # 3. Run tests
    for test_index, (input, answer) in enumerate(zip(inputs, answers), start=1):
        # create a corresponding output file for given input file
        output = input.replace(".in", ".out")

        # run the program on input data
        os.system(cmd + " <  " + input + " > " + output)

        # compare the output with the answer
        if filecmp.cmp(answer, output, shallow=False) == True:
            print("\x1b[6;30;42m" + f"- Passed Test {test_index}     " + "\x1b[0m")
        else:
            print("\x1b[6;30;41m" + f"- Failed Test {test_index}     " + "\x1b[0m")
            os.system(f'diff -y "{answer}" "{output}"')
            break
