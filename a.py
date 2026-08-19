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

            print("localconfig.json deleted.")

        else:
            print(
                "adb push failed — is the phone connected? "
                "Run `adb devices` to check."
            )


if __name__ == "__main__":
    main()
