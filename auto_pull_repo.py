import subprocess

def auto_update(commit):
    print("-------- Start Update Repository --------")
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        print("git pull success ✔️")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    auto_update("test Update lagi")