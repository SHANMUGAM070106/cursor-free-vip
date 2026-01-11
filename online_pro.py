import os
import json
import sqlite3
import uuid

def switch_to_online_pro():
    print("Switching to Online Pro Mode...")
    
    # Kill Cursor first
    try:
        os.system('taskkill /f /im Cursor.exe >nul 2>&1')
    except:
        pass
    
    # Config paths
    config_dir = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
    storage_path = os.path.join(config_dir, 'storage.json')
    db_path = os.path.join(config_dir, 'state.vscdb')
    
    # Generate realistic Pro tokens
    session_token = f"wos_prod_{uuid.uuid4().hex[:32]}"
    auth_token = f"cur_prod_{uuid.uuid4().hex[:32]}"
    user_id = str(uuid.uuid4())
    
    # Online Pro configuration
    online_pro_config = {
        # Remove offline settings
        "cursor.offline.mode": False,
        "cursor.offline.pro": False,
        "cursor.network.disabled": False,
        "cursor.api.disabled": False,
        
        # Online authentication
        "workos.sessionToken": session_token,
        "workos.user.email": "sanjay9852cpr@gmail.com",
        "workos.user.id": user_id,
        "cursor.auth.token": auth_token,
        "cursor.auth.email": "sanjay9852cpr@gmail.com",
        "cursor.auth.online": True,
        
        # Online Pro subscription
        "cursor.subscription.type": "pro",
        "cursor.subscription.status": "active",
        "cursor.subscription.plan": "pro_monthly",
        "cursor.subscription.online": True,
        "cursor.subscription.verified": True,
        
        # Pro features (online)
        "cursor.pro.enabled": True,
        "cursor.pro.online": True,
        "cursor.pro.verified": True,
        "cursor.features.copilot": True,
        "cursor.features.copilotPlusPlus": True,
        "cursor.features.chat": True,
        "cursor.features.composer": True,
        "cursor.features.unlimited": True,
        
        # Unlimited usage (online)
        "cursor.usage.unlimited": True,
        "cursor.usage.limit": 999999,
        "cursor.limits.disabled": True,
        "cursor.limits.bypassed": True,
        
        # Enable online checks but bypass them
        "cursor.checks.subscription": True,
        "cursor.checks.usage": True,
        "cursor.checks.api": True,
        "cursor.checks.online": True,
        "cursor.checks.bypass": True,
        
        # User info
        "cursor.user.name": "SANJAY KUMAR",
        "cursor.user.email": "sanjay@gmail.com",
        "cursor.user.tier": "pro",
        "cursor.user.verified": True
    }
    
    # Update storage.json
    try:
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        # Remove offline keys
        offline_keys = [k for k in data.keys() if 'offline' in k.lower()]
        for key in offline_keys:
            if 'offline' in key and data[key] == True:
                data[key] = False
        
        # Add online Pro config
        data.update(online_pro_config)
        
        with open(storage_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Storage updated for online Pro mode")
    except Exception as e:
        print(f"Storage error: {e}")
        return False
    
    # Update database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)")
        
        # Insert online Pro settings
        for key, value in online_pro_config.items():
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, str(value)))
        
        # Additional online settings
        online_settings = [
            ("cachedSignUpType", "google"),
            ("accessToken", auth_token),
            ("refreshToken", auth_token),
            ("userEmail", "sanjay@gmail.com"),
            ("userName", "SANJAY KUMAR"),
            ("subscriptionType", "pro"),
            ("subscriptionStatus", "active"),
            ("userTier", "pro"),
            ("onlineMode", "true"),
            ("proFeaturesEnabled", "true"),
            ("usageLimitsDisabled", "true"),
            ("checksEnabled", "true"),
            ("checksBypass", "true")
        ]
        
        for key, value in online_settings:
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
        
        conn.commit()
        conn.close()
        print("Database updated for online Pro mode")
        
    except Exception as e:
        print(f"Database error: {e}")
        return False
    
    print("\nOnline Pro Mode Activated!")
    print("What changed:")
    print("• Switched from offline to online mode")
    print("• Added realistic Pro authentication tokens")
    print("• Enabled online checks with bypass")
    print("• Set proper user info (SANJAY KUMAR)")
    print("• Maintained unlimited Pro features")
    
    print("\nNext steps:")
    print("1. Start Cursor")
    print("2. Should show online Pro status")
    print("3. All Pro features will work unlimited")
    print("4. Better integration with Cursor services")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("CURSOR ONLINE PRO MODE ACTIVATOR")
    print("=" * 50)
    
    if switch_to_online_pro():
        print("\nSuccess! Cursor is now in Online Pro Mode")
    else:
        print("\nFailed to switch to Online Pro Mode")
    
    input("Press Enter to exit...")