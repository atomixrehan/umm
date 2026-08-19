#!/usr/bin/env python3
import os
import subprocess
import tempfile
import urllib.request

# ---- EDIT THIS ----
URL = "https://raw.githubusercontent.com/atomixrehan/localconfig/refs/heads/main/localconfig.json"
# -------------------

PACKAGE = "com.dts.freefireth"
REMOTE_DIR = f"/sdcard/Android/data/{PACKAGE}/files"

result = subprocess.run(
    ["adb", "shell", "pm", "list", "packages", PACKAGE],
    capture_output=True,
    text=True
)

if f"package:{PACKAGE}" in result.stdout:
    print("Connected to FreeFire")
else:
    print("FreeFire is not installed")


import time


def main():
    filename = URL.rstrip("/").split("/")[-1]
    remote_path = f"{REMOTE_DIR}/{filename}"

    with tempfile.TemporaryDirectory() as tmp:
        local_path = os.path.join(tmp, filename)

        print("Connecting...")
        urllib.request.urlretrieve(URL, local_path)

        print("Executing...")
        subprocess.run(
            ["adb", "shell", "mkdir", "-p", REMOTE_DIR],
            check=False
        )

        result = subprocess.run(
            ["adb", "push", local_path, remote_path]
        )

        if result.returncode == 0:
            print("Done.")

            subprocess.run([
                "adb",
                "shell",
                "monkey",
                "-p",
                PACKAGE,
                "-c",
                "android.intent.category.LAUNCHER",
                "1"
            ])

            time.sleep(10)

            subprocess.run([
                "adb",
                "shell",
                "rm",
                "-f",
                f"{REMOTE_DIR}/localconfig.json"
            ])

            print("Bypass Activated")

        else:
            print(
                "execution failed"
                "Make Sure Shizuku Is Running"
            )


if __name__ == "__main__":
    main()
