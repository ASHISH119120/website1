import hashlib
import os
import json
from datetime import datetime

# === Configuration ===
HASH_DB = "hash_db.json"
MONITORED_FILES = ["example.txt", "config.ini"]  # Add your files here

# === Utility Functions ===
def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def load_hash_db():
    """Load the stored hash database from a JSON file."""
    if not os.path.exists(HASH_DB):
        return {}
    with open(HASH_DB, "r") as db_file:
        return json.load(db_file)

def save_hash_db(db):
    """Save the hash database to a JSON file."""
    with open(HASH_DB, "w") as db_file:
        json.dump(db, db_file, indent=4)

def monitor_files():
    """Compare current hashes with stored hashes and detect changes."""
    db = load_hash_db()
    changes_detected = False

    print("\n📊 File Integrity Scan Report:")
    print(f"Timestamp: {datetime.now()}\n")

    for file in MONITORED_FILES:
        current_hash = calculate_hash(file)

        if current_hash is None:
            print(f"❌ File not found: {file}")
            continue

        stored_hash = db.get(file)

        if stored_hash is None:
            print(f"➕ New file detected: {file}")
            db[file] = current_hash
            changes_detected = True
        elif current_hash != stored_hash:
            print(f"⚠️  Change detected in: {file}")
            print(f"   Old Hash: {stored_hash}")
            print(f"   New Hash: {current_hash}")
            db[file] = current_hash
            changes_detected = True
        else:
            print(f"✅ No change: {file}")

    if not changes_detected:
        print("\n🎉 All monitored files are unchanged.")

    save_hash_db(db)

# === Entry Point ===
if __name__ == "__main__":
    print("🔍 File Integrity Monitor")
    print("=" * 30)
    monitor_files()
