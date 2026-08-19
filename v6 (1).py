#!/usr/bin/env python3
"""
Dead-simple version: hardcode the URL below, run the script, pick 1 or 2.

  1) Activate   -> downloads URL, pushes it into
                   /sdcard/Android/data/com.dts.freefireth/files/
  2) Deactivate -> deletes localconfig.json from that same folder on the phone

Requires: adb installed and your phone connected (USB debugging on, or
already `adb connect`-ed over wireless debugging).

    pkg install android-tools     (Termux)
    apt install android-tools-adb (Linux)
"""

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
