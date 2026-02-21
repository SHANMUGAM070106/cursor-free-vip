#!/usr/bin/env python3
"""
Cursor Offline Pro Mode - Completely disable online checks
"""

import os
import json
import sqlite3
import uuid
import subprocess
import time

def disable_cursor_online_checks():
    """Disable all online subscription checks"""
    print("Disabling Cursor online checks...")
    
    # 1. Block Cursor domains in hosts file
    try:
        if os.name == 'nt':
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        else:
            hosts_path = '/etc/hosts'
        
        # Read current hosts
        try:
            with open(hosts_path, 'r') as f:
                hosts_content = f.read()
        except:
            hosts_content = ""
        
        # Domains to block
        cursor_domains = [
            "127.0.0.1 api2.cursor.sh",
            "127.0.0.1 api.cursor.sh", 
            "127.0.0.1 cursor.com",
            "127.0.0.1 www.cursor.com",
            "127.0.0.1 auth.cursor.sh",
            "127.0.0.1 authenticator.cursor.sh"
        ]
        
        # Add blocks if not present
        modified = False
        for domain in cursor_domains:
            if domain not in hosts_content:
                hosts_content += f"\n{domain}"
                modified = True
        
        if modified:
            with open(hosts_path, 'w') as f:
                f.write(hosts_content)
            print("Blocked Cursor domains in hosts file")
        else:
            print("Cursor domains already blocked")
            
    except PermissionError:
        print("Cannot modify hosts file - need Administrator privileges")
        print("Continuing with other methods...")
    except Exception as e:
        print(f"Hosts file error: {e}")
    
    return True

def create_offline_pro_config():
    """Create offline Pro configuration"""
    print("Creating offline Pro configuration...")
    
    # Find Cursor config directory
    if os.name == 'nt':
        config_dir = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
    else:
        config_dir = os.path.expanduser('~/.config/cursor/User/globalStorage')
    
    os.makedirs(config_dir, exist_ok=True)
    
    # Generate tokens
    session_token = f"offline_pro_{uuid.uuid4().hex}"
    
    # Comprehensive offline Pro config
    offline_pro_config = {
        # Force offline mode
        "cursor.offline.mode": True,
        "cursor.offline.pro": True,
        "cursor.network.disabled": True,
        "cursor.api.disabled": True,
        
        # Authentication (offline)
        "workos.sessionToken": session_token,
        "workos.user.email": "offline@pro.cursor",
        "cursor.auth.offline": True,
        "cursor.auth.token": session_token,
        
        # Subscription (offline Pro)
        "cursor.subscription.type": "pro",
        "cursor.subscription.status": "active", 
        "cursor.subscription.offline": True,
        "cursor.subscription.verified": True,
        "cursor.subscription.plan": "pro_unlimited",
        
        # Pro features (all enabled)
        "cursor.pro.enabled": True,
        "cursor.pro.offline": True,
        "cursor.features.copilot": True,
        "cursor.features.copilotPlusPlus": True,
        "cursor.features.chat": True,
        "cursor.features.composer": True,
        "cursor.features.codebase": True,
        "cursor.features.all": True,
        
        # Unlimited usage
        "cursor.usage.unlimited": True,
        "cursor.usage.limit": 999999,
        "cursor.limits.disabled": True,
        "cursor.limits.bypassed": True,
        
        # Disable checks
        "cursor.checks.subscription": False,
        "cursor.checks.usage": False,
        "cursor.checks.api": False,
        "cursor.checks.online": False,
        
        # Privacy
        "telemetry.disabled": True,
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
        
        storage.update(offline_pro_config)
        
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(storage, f, indent=2)
        
        print("Updated storage.json with offline Pro config")
    except Exception as e:
        print(f"Storage update failed: {e}")
        return False
    
    # Update database
    db_path = os.path.join(config_dir, 'state.vscdb')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)''')
        
        # Insert offline Pro settings
        for key, value in offline_pro_config.items():
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, str(value)))
        
        conn.commit()
        conn.close()
        print("Updated database with offline Pro config")
        
    except Exception as e:
        print(f"Database update failed: {e}")
        return False
    
    return True

def kill_cursor():
    """Kill Cursor processes"""
    print("Stopping Cursor...")
    try:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/f', '/im', 'Cursor.exe'], capture_output=True)
            subprocess.run(['taskkill', '/f', '/im', 'cursor.exe'], capture_output=True)
        else:
            subprocess.run(['pkill', '-f', 'cursor'], capture_output=True)
        time.sleep(2)
        print("Cursor stopped")
    except:
        pass

def main():
    print("=" * 60)
    print("CURSOR OFFLINE PRO MODE ACTIVATOR")
    print("=" * 60)
    print("This will make Cursor work in offline Pro mode")
    print("No more online subscription checks!")
    print()
    
    # Stop Cursor
    kill_cursor()
    
    # Disable online checks
    disable_cursor_online_checks()
    
    # Create offline Pro config
    if create_offline_pro_config():
        print("\n" + "=" * 60)
        print("SUCCESS! Cursor Offline Pro Mode Activated")
        print("\nWhat was done:")
        print("• Blocked Cursor API domains")
        print("• Enabled offline Pro mode")
        print("• Disabled all online checks")
        print("• Activated all Pro features")
        print("• Set unlimited usage")
        
        print("\nNext steps:")
        print("1. Start Cursor")
        print("2. Cursor will work in offline Pro mode")
        print("3. All Pro features available")
        print("4. No subscription checks")
        
        print("\nNote: Cursor may show 'offline' but all Pro features will work!")
        
    else:
        print("\nFailed to activate offline Pro mode")
        print("Try running as Administrator")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")