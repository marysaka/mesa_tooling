#!/usr/bin/env python3

import os
import sys
import argparse
import urllib.request
import ssl
import json
import platform
import subprocess

GITEA_API_BASE_URL = "https://lastorder/git/api/v1"

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rel", help="Release to use", default="latest")
    return parser.parse_args()


def get_latest_release_data() -> str:
    with urllib.request.urlopen(
        f"{GITEA_API_BASE_URL}/repos/Mary/cts_build_scripts/releases/latest",
        context=ssl_ctx,
    ) as f:
        return json.loads(f.read())


def main(args: argparse.Namespace) -> int:
    rel = args.rel

    assert rel == "latest"

    arch = platform.machine()
    res = get_latest_release_data()
    cts_build_url = None

    for asset in res["assets"]:
        if arch in asset["name"]:
            cts_build_url = asset["browser_download_url"]

    subprocess.check_call(["install_cts_build", cts_build_url])
    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args()))
