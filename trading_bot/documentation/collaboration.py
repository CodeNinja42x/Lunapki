import os

def setup_git():
    os.system("git init")
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")

if __name__ == "__main__":
    setup_git()
    print("Git repository initialized.")
