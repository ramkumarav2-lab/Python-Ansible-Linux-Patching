#!/usr/bin/env python3
import os
import sys
import subprocess

INVENTORY = "inventory/hosts"
PLAYBOOK_DIR = "playbooks"

PLAYBOOKS = {
    "1": "pre_req_check.yml",
    "2": "pre_patch_validation.yml",
    "3": "patching_with_reboot.yml",
    "4": "download_only.yml"
}

def run_playbook(playbook):
    playbook_path = os.path.join(PLAYBOOK_DIR, playbook)

    if not os.path.exists(playbook_path):
        print(f"[ERROR] Playbook not found: {playbook_path}")
        sys.exit(1)

    cmd = [
        "ansible-playbook",
        "-i", INVENTORY,
        playbook_path
    ]

    print("\n[INFO] Executing:", " ".join(cmd))
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("[ERROR] Playbook execution failed")
        sys.exit(result.returncode)
    else:
        print("[SUCCESS] Playbook completed successfully")

def reboot_confirmation():
    choice = input("\nReboot required. Proceed with reboot? (yes/no): ").lower()
    if choice == "yes":
        run_playbook("patching_with_reboot.yml")
    else:
        print("[INFO] Reboot skipped")

def menu():
    print("\n===== Linux L2 Patching Automation =====")
    print("1. Pre-requisite checks")
    print("2. Pre-patching validation")
    print("3. Automated patching with reboot")
    print("4. Download-only mode (offline updates)")
    print("5. Exit")

def main():
    while True:
        menu()
        choice = input("\nEnter your choice: ").strip()

        if choice in ["1", "2", "4"]:
            run_playbook(PLAYBOOKS[choice])

        elif choice == "3":
            run_playbook("patching_with_reboot.yml")
            reboot_confirmation()

        elif choice == "5":
            print("\nExiting automation launcher.")
            sys.exit(0)

        else:
            print("[WARNING] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
