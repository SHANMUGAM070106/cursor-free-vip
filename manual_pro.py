import os
import json
import sqlite3
import uuid

# Find config path
config_path = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage\storage.json')
db_path = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage\state.vscdb')

print("Manual Pro Activation...")

# 1. Update storage.json
try:
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    
    # Add Pro settings
    data.update({
        "cursor.subscription.type": "pro",
        "cursor.subscription.status": "active",
        "cursor.pro.enabled": True,
        "cursor.features.copilot": True,
        "cursor.features.chat": True,
        "cursor.features.composer": True,
        "cursor.trial.remaining": 30
    })
    
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Storage updated")
except Exception as e:
    print(f"Storage error: {e}")

# 2. Update database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)")
    
    settings = [
        ("cursor.subscription.type", "pro"),
        ("cursor.subscription.status", "active"),
        ("cursor.pro.enabled", "true"),
        ("cursor.trial.remaining", "30")
    ]
    
    for key, value in settings:
        cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
    
    conn.commit()
    conn.close()
    print("✓ Database updated")
except Exception as e:
    print(f"Database error: {e}")

print("\nDone! Now restart Cursor")
input("Press Enter...")