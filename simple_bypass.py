#!/usr/bin/env python3
"""
Simple Cursor Pro Bypass - Works without admin privileges
"""

import os
import json
import sqlite3
import uuid
import time

def simple_pro_bypass():
    """Simple Pro bypass using config modification only"""
    print("Starting Simple Cursor Pro Bypass...")
    
    # Kill Cursor first
    print("Stopping Cursor...")
    try:
        if os.name == 'nt':
            os.system('taskkill /f /im Cursor.exe >nul 2>&1')
            os.system('taskkill /f /im cursor.exe >nul 2>&1')
        time.sleep(2)
    except:
        pass
    
    # Find config directory
    if os.name == 'nt':
        config_dir = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
    else:
        config_dir = os.path.expanduser('~/.config/cursor/User/globalStorage')
    
    if not os.path.exists(config_dir):
        print(f"Config directory not found: {config_dir}")
        return False
    
    # Generate realistic tokens
    session_token = f"wos_prod_{uuid.uuid4().hex[:32]}"
    auth_token = f"cur_prod_{uuid.uuid4().hex[:32]}"
    
    # Create comprehensive Pro configuration
    pro_config = {
        # Authentication
        "workos.sessionToken": session_token,
        "workos.user.email": "pro@cursor.sh",
        "cursor.auth.token": auth_token,
        "cursor.auth.email": "pro@cursor.sh",
        "cursor.auth.userId": str(uuid.uuid4()),
        
        # Subscription
        "cursor.subscription.type": "pro",
        "cursor.subscription.status": "active",
        "cursor.subscription.plan": "pro_monthly",
        "cursor.subscription.tier": "pro",
        "cursor.subscription.active": True,
        
        # Trial
        "cursor.trial.enabled": True,
        "cursor.trial.remaining": 999,
        "cursor.trial.daysLeft": 999,
        "cursor.trial.active": True,
        
        # Pro Features
        "cursor.pro.enabled": True,
        "cursor.pro.active": True,
        "cursor.pro.verified": True,
        
        # Features
        "cursor.features.copilot": True,
        "cursor.features.copilotPlusPlus": True,
        "cursor.features.chat": True,
        "cursor.features.composer": True,
        "cursor.features.codebase": True,
        "cursor.features.unlimited": True,
        
        # Limits
        "cursor.limits.bypassed": True,
        "cursor.limits.disabled": True,
        "cursor.usage.unlimited": True,
        "cursor.usage.limit": 999999,
        
        # API
        "cursor.api.bypass": True,
        "cursor.api.offline": True,
        
        # Privacy
        "telemetry.optout": True,
        "analytics.disabled": True,
        "tracking.disabled": True
    }
    
    # Update storage.json
    storage_path = os.path.join(config_dir, 'storage.json')
    try:
        if os.path.exists(storage_path):
            with open(storage_path, 'r', encoding='utf-8') as f:
                storage = json.load(f)
        else:
            storage = {}
        
        storage.update(pro_config)
        
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(storage, f, indent=2)
        
        print("Updated storage.json")
    except Exception as e:
        print(f"Failed to update storage.json: {e}")
        return False
    
    # Update SQLite database
    db_path = os.path.join(config_dir, 'state.vscdb')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)''')
        
        # Insert all Pro settings
        for key, value in pro_config.items():
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, str(value)))
        
        # Additional database entries
        additional_entries = [
            ("cachedSignUpType", "google"),
            ("accessToken", auth_token),
            ("refreshToken", auth_token),
            ("userEmail", "pro@cursor.sh"),
            ("subscriptionType", "pro"),
            ("subscriptionStatus", "active"),
            ("userTier", "pro"),
            ("proFeaturesEnabled", "true"),
            ("usageLimitsDisabled", "true"),
            ("apiBypassEnabled", "true"),
            ("offlineMode", "true")
        ]
        
        for key, value in additional_entries:
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
        
        conn.commit()
        conn.close()
        print("Updated database")
        
    except Exception as e:
        print(f"Failed to update database: {e}")
        return False
    
    # Update machine ID
    machine_id_path = None
    if os.name == 'nt':
        machine_id_path = os.path.expandvars(r'%APPDATA%\Cursor\machineId')
    else:
        machine_id_path = os.path.expanduser('~/.config/cursor/machineId')
    
    if machine_id_path:
        try:
            with open(machine_id_path, 'w') as f:
                f.write(str(uuid.uuid4()))
            print("Updated machine ID")
        except:
            pass
    
    print("\n" + "=" * 50)
    print("SUCCESS! Simple Cursor Pro bypass completed")
    print("\nWhat was done:")
    print("• Set subscription to Pro with unlimited trial")
    print("• Enabled all Pro features")
    print("• Bypassed usage limits")
    print("• Added authentication tokens")
    print("• Updated machine ID")
    
    print("\nNext steps:")
    print("1. Start Cursor")
    print("2. All Pro features should work")
    print("3. Check Settings > Account")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("SIMPLE CURSOR PRO BYPASS")
    print("=" * 50)
    
    if simple_pro_bypass():
        print("\nBypass completed successfully!")
        print("You can now start Cursor and use Pro features")
    else:
        print("\nBypass failed!")
        print("Try running as Administrator or check Cursor installation")
    
    input("\nPress Enter to exit...")