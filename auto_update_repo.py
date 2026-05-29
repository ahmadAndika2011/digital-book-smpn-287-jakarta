import subprocess

def auto_update(commit):
    print("-------- Start Update Repository --------")
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("git add success ✔️")
        
        subprocess.run(["git", "commit", "-m", f"'{commit}'"], check=True)
        print("git commit success ✔️")

        subprocess.run(["git", "push", "-u", "origin", 'main'], check=True)
        print("git push success ✔️")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    auto_update("test Update lagi")