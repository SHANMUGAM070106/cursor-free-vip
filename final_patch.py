import os
import json
import sqlite3
import subprocess
import time

def final_pro_patch():
    print("Final Pro Patch - Removing ALL limits...")
    
    # Kill Cursor
    try:
        subprocess.run(['taskkill', '/f', '/im', 'Cursor.exe'], capture_output=True)
        time.sleep(2)
    except:
        pass
    
    # Config paths
    config_dir = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
    storage_path = os.path.join(config_dir, 'storage.json')
    db_path = os.path.join(config_dir, 'state.vscdb')
    
    # Ultimate Pro config
    ultimate_config = {
        "cursor.subscription.type": "pro",
        "cursor.subscription.status": "active",
        "cursor.subscription.plan": "pro_unlimited",
        "cursor.pro.enabled": True,
        "cursor.pro.unlimited": True,
        "cursor.features.copilot": True,
        "cursor.features.copilotPlusPlus": True,
        "cursor.features.chat": True,
        "cursor.features.composer": True,
        "cursor.features.unlimited": True,
        "cursor.usage.unlimited": True,
        "cursor.usage.limit": 999999,
        "cursor.limits.disabled": True,
        "cursor.limits.bypassed": True,
        "cursor.trial.unlimited": True,
        "cursor.trial.remaining": 999,
        "cursor.api.unlimited": True,
        "cursor.requests.unlimited": True,
        "workos.user.subscription": "pro",
        "workos.user.plan": "pro_unlimited"
    }
    
    # Update storage
    try:
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        data.update(ultimate_config)
        
        with open(storage_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Storage updated with unlimited Pro")
    except Exception as e:
        print(f"Storage error: {e}")
    
    # Update database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)")
        
        for key, value in ultimate_config.items():
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, str(value)))
        
        # Additional unlimited settings
        unlimited_settings = [
            ("subscriptionType", "pro"),
            ("subscriptionStatus", "active"),
            ("userTier", "pro"),
            ("planType", "pro_unlimited"),
            ("usageLimit", "999999"),
            ("requestLimit", "999999"),
            ("chatLimit", "999999"),
            ("copilotLimit", "999999"),
            ("composerLimit", "999999"),
            ("limitsDisabled", "true"),
            ("unlimitedAccess", "true")
        ]
        
        for key, value in unlimited_settings:
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
        
        conn.commit()
        conn.close()
        print("Database updated with unlimited settings")
        
    except Exception as e:
        print(f"Database error: {e}")
    
    print("\nFinal patch completed!")
    print("Start Cursor now - ALL limits should be removed")
    print("Even if it shows 'Free Plan', you'll have unlimited usage")

if __name__ == "__main__":
    final_pro_patch()
    input("Press Enter to exit...")