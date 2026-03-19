import sys

print("=== Command Quest ===")
if len(sys.argv) < 2:
    print("No arguments provided!")
    print(f"Program name: {sys.argv[0]}")
else:
    print(f"Program name: {sys.argv[0]}")
    print(f"Arguments received: {len(sys.argv) - 1}")
    cpt = 1
    for arg in sys.argv[1:]:
        print(f"Argument {cpt}: {arg}")
        cpt += 1
print(f"Total arguments: {len(sys.argv)}")
