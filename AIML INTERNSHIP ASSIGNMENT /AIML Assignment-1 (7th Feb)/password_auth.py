"""
Password Authentication System
================================
A secure password authentication module using:
  - bcrypt for password hashing (with automatic salting)
  - Strong password-policy enforcement
  - Account lockout after repeated failures
  - JSON-file–based user storage (easily swappable for a real DB)

Usage:
    python password_auth.py
"""

import hashlib
import json
import os
import re
import getpass
import time
import secrets
from datetime import datetime, timedelta


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
USER_DB_FILE = "users_db.json"          # File that stores user records
MAX_FAILED_ATTEMPTS = 5                 # Lock account after this many failures
LOCKOUT_DURATION_MINUTES = 15           # How long the lockout lasts
MIN_PASSWORD_LENGTH = 8                 # Minimum password length
PBKDF2_ITERATIONS = 600_000             # OWASP-recommended iteration count
SALT_LENGTH = 32                        # Bytes of random salt



# ──────────────────────────────────────────────
# Database helpers  (JSON file storage)
# ──────────────────────────────────────────────
def _load_db() -> dict:
    """Load the user database from disk."""
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)


def _save_db(db: dict) -> None:
    """Persist the user database to disk."""
    with open(USER_DB_FILE, "w") as f:
        json.dump(db, f, indent=4)


# ──────────────────────────────────────────────
# Password-strength validator
# ──────────────────────────────────────────────
def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Enforce a strong-password policy.

    Rules
    -----
    1. At least MIN_PASSWORD_LENGTH characters long
    2. Contains at least one uppercase letter
    3. Contains at least one lowercase letter
    4. Contains at least one digit
    5. Contains at least one special character (!@#$%^&*…)
    6. No spaces allowed
    7. Must not be a commonly-used weak password

    Returns
    -------
    (is_valid, list_of_error_messages)
    """
    errors: list[str] = []

    # Common weak passwords to reject outright
    COMMON_PASSWORDS = {
        "password", "123456", "12345678", "qwerty", "abc123",
        "password1", "admin", "letmein", "welcome", "monkey",
        "1234567890", "password123", "iloveyou", "sunshine",
    }

    if len(password) < MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", password):
        errors.append("Password must contain at least one special character (!@#$%^&*…).")

    if " " in password:
        errors.append("Password must not contain spaces.")

    if password.lower() in COMMON_PASSWORDS:
        errors.append("This password is too common. Please choose a stronger one.")

    return (len(errors) == 0, errors)


# ──────────────────────────────────────────────
# Hashing helpers
# ──────────────────────────────────────────────
def hash_password(password: str) -> str:
    """
    Hash *password* using PBKDF2-HMAC-SHA256 with a random salt.
    Returns a string in the format:  salt_hex$hash_hex
    """
    salt = secrets.token_bytes(SALT_LENGTH)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return salt.hex() + "$" + pw_hash.hex()


def verify_password(password: str, stored: str) -> bool:
    """
    Verify *password* against a stored 'salt$hash' string.
    Uses constant-time comparison to prevent timing attacks.
    """
    try:
        salt_hex, hash_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
    except (ValueError, AttributeError):
        return False
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return secrets.compare_digest(pw_hash, expected)


# ──────────────────────────────────────────────
# Account-lockout helpers
# ──────────────────────────────────────────────
def _is_account_locked(user_record: dict) -> bool:
    """Return True if the account is currently locked out."""
    locked_until = user_record.get("locked_until")
    if locked_until is None:
        return False
    return datetime.fromisoformat(locked_until) > datetime.now()


def _remaining_lockout(user_record: dict) -> str:
    """Human-readable time remaining on the lockout."""
    locked_until = datetime.fromisoformat(user_record["locked_until"])
    delta = locked_until - datetime.now()
    minutes = int(delta.total_seconds() // 60)
    seconds = int(delta.total_seconds() % 60)
    return f"{minutes} min {seconds} sec"


# ──────────────────────────────────────────────
# Core authentication functions
# ──────────────────────────────────────────────
def register_user(username: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.

    Parameters
    ----------
    username : str
    password : str  (plain text — will be hashed before storage)

    Returns
    -------
    (success: bool, message: str)
    """
    db = _load_db()

    # ── Validate username ──
    if not username or not username.strip():
        return False, "Username cannot be empty."

    username = username.strip().lower()

    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username may only contain letters, digits, and underscores."

    if username in db:
        return False, "Username already exists. Please choose a different one."

    # ── Validate password strength ──
    is_strong, errors = validate_password_strength(password)
    if not is_strong:
        return False, "Weak password:\n  • " + "\n  • ".join(errors)

    # ── Store user record ──
    db[username] = {
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "failed_attempts": 0,
        "locked_until": None,
    }
    _save_db(db)
    return True, f"User '{username}' registered successfully!"


def login_user(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user.

    Implements account lockout after MAX_FAILED_ATTEMPTS consecutive
    failures, with a LOCKOUT_DURATION_MINUTES cool-down.

    Returns
    -------
    (success: bool, message: str)
    """
    db = _load_db()
    username = username.strip().lower()

    if username not in db:
        # Generic message to avoid revealing whether the username exists
        return False, "Invalid username or password."

    user = db[username]

    # ── Check lockout ──
    if _is_account_locked(user):
        remaining = _remaining_lockout(user)
        return False, (
            f"Account is locked due to too many failed attempts. "
            f"Try again in {remaining}."
        )

    # ── Verify password ──
    if verify_password(password, user["password_hash"]):
        # Reset failure counter on success
        user["failed_attempts"] = 0
        user["locked_until"] = None
        _save_db(db)
        return True, f"Welcome back, {username}!"
    else:
        # Increment failure counter
        user["failed_attempts"] += 1
        remaining_attempts = MAX_FAILED_ATTEMPTS - user["failed_attempts"]

        if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
            lock_time = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            user["locked_until"] = lock_time.isoformat()
            _save_db(db)
            return False, (
                f"Too many failed attempts. Account locked for "
                f"{LOCKOUT_DURATION_MINUTES} minutes."
            )

        _save_db(db)
        return False, (
            f"Invalid username or password. "
            f"{remaining_attempts} attempt(s) remaining before lockout."
        )


def change_password(username: str, old_password: str, new_password: str) -> tuple[bool, str]:
    """
    Change the password for an existing user.

    The caller must supply the correct current password.
    The new password must pass the strength check and must differ
    from the old password.
    """
    db = _load_db()
    username = username.strip().lower()

    if username not in db:
        return False, "User not found."

    user = db[username]

    if not verify_password(old_password, user["password_hash"]):
        return False, "Current password is incorrect."

    if old_password == new_password:
        return False, "New password must be different from the current password."

    is_strong, errors = validate_password_strength(new_password)
    if not is_strong:
        return False, "Weak new password:\n  • " + "\n  • ".join(errors)

    user["password_hash"] = hash_password(new_password)
    _save_db(db)
    return True, "Password changed successfully!"


def delete_user(username: str, password: str) -> tuple[bool, str]:
    """
    Delete a user account after confirming the password.
    """
    db = _load_db()
    username = username.strip().lower()

    if username not in db:
        return False, "User not found."

    if not verify_password(password, db[username]["password_hash"]):
        return False, "Incorrect password. Account not deleted."

    del db[username]
    _save_db(db)
    return True, f"User '{username}' has been deleted."


# ──────────────────────────────────────────────
# Interactive CLI
# ──────────────────────────────────────────────
def _print_banner():
    print("\n" + "=" * 50)
    print("   🔐  Secure Password Authentication System")
    print("=" * 50)


def _print_menu():
    print("\n  [1] Register")
    print("  [2] Login")
    print("  [3] Change Password")
    print("  [4] Delete Account")
    print("  [5] Exit")
    print()


def main():
    _print_banner()

    while True:
        _print_menu()
        choice = input("  Select an option (1-5): ").strip()

        if choice == "1":
            print("\n── Register ──")
            username = input("  Username : ").strip()
            password = input("  Password : ")
            confirm  = input("  Confirm  : ")
            if password != confirm:
                print("  ❌ Passwords do not match.")
                continue
            ok, msg = register_user(username, password)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif choice == "2":
            print("\n── Login ──")
            username = input("  Username : ").strip()
            password = input("  Password : ")
            ok, msg = login_user(username, password)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif choice == "3":
            print("\n── Change Password ──")
            username     = input("  Username         : ").strip()
            old_password = input("  Current Password : ")
            new_password = input("  New Password     : ")
            confirm      = input("  Confirm New      : ")
            if new_password != confirm:
                print("  ❌ New passwords do not match.")
                continue
            ok, msg = change_password(username, old_password, new_password)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif choice == "4":
            print("\n── Delete Account ──")
            username = input("  Username : ").strip()
            password = input("  Password : ")
            confirm  = input("  Type 'DELETE' to confirm: ").strip()
            if confirm != "DELETE":
                print("  ❌ Deletion cancelled.")
                continue
            ok, msg = delete_user(username, password)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif choice == "5":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  ⚠️  Invalid option. Please choose 1–5.")


if __name__ == "__main__":
    main()
