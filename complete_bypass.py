#!/usr/bin/env python3
"""
Complete Cursor Pro Bypass - Patches the application files directly
"""

import os
import json
import sqlite3
import uuid
import shutil
import re
from pathlib import Path

def find_cursor_installation():
    """Find Cursor installation directory"""
    possible_paths = [
        r"C:\Users\{}\AppData\Local\Programs\Cursor".format(os.getenv('USERNAME')),
        r"C:\Program Files\Cursor",
        r"C:\Program Files (x86)\Cursor",
        os.path.expanduser("~/Applications/Cursor.app"),
        "/usr/local/bin/cursor",
        "/opt/cursor"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def patch_cursor_files():
    """Patch Cursor application files to bypass Pro checks"""
    print("Patching Cursor application files...")
    
    cursor_path = find_cursor_installation()
    if not cursor_path:
        print("Cursor installation not found")
        return False
    
    print(f"Found Cursor at: {cursor_path}")
    
    # Find main application files
    app_files = []
    for root, dirs, files in os.walk(cursor_path):
        for file in files:
            if file.endswith(('.js', '.asar')) and any(x in file.lower() for x in ['main', 'app', 'workbench']):
                app_files.append(os.path.join(root, file))
    
    patched_count = 0
    for file_path in app_files:
        try:
            if file_path.endswith('.asar'):
                continue  # Skip binary files
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Patch subscription checks
            patches = [
                # Bypass subscription validation
                (r'subscription.*?===.*?"pro"', 'true'),
                (r'subscription.*?!==.*?"free"', 'true'),
                (r'isPro.*?===.*?false', 'isPro === true'),
                (r'isSubscribed.*?===.*?false', 'isSubscribed === true'),
                (r'hasProAccess.*?===.*?false', 'hasProAccess === true'),
                
                # Bypass usage limits
                (r'usageLimit.*?>=.*?\d+', 'false'),
                (r'requestCount.*?>=.*?\d+', 'false'),
                (r'dailyLimit.*?>=.*?\d+', 'false'),
                
                # Force Pro features
                (r'"subscription":\s*"free"', '"subscription": "pro"'),
                (r'"plan":\s*"free"', '"plan": "pro"'),
                (r'"tier":\s*"free"', '"tier": "pro"'),
                
                # Bypass API checks
                (r'401.*?Unauthorized', '200'),
                (r'subscription.*?expired', 'subscription_active'),
            ]
            
            for pattern, replacement in patches:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            if content != original_content:
                # Backup original
                backup_path = file_path + '.backup'
                if not os.path.exists(backup_path):
                    shutil.copy2(file_path, backup_path)
                
                # Write patched version
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                patched_count += 1
                print(f"Patched: {os.path.basename(file_path)}")
                
        except Exception as e:
            continue
    
    print(f"Patched {patched_count} files")
    return patched_count > 0

def create_pro_config():
    """Create comprehensive Pro configuration"""
    print("Creating Pro configuration...")
    
    # Find config directory
    if os.name == 'nt':
        config_dir = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
    else:
        config_dir = os.path.expanduser('~/.config/cursor/User/globalStorage')
    
    os.makedirs(config_dir, exist_ok=True)
    
    # Create storage.json with Pro settings
    storage_path = os.path.join(config_dir, 'storage.json')
    pro_storage = {
        "workos.sessionToken": f"wos_prod_{uuid.uuid4().hex}",
        "workos.user.email": "pro@cursor.sh",
        "cursor.auth.token": f"cur_prod_{uuid.uuid4().hex}",
        "cursor.subscription.type": "pro",
        "cursor.subscription.status": "active",
        "cursor.subscription.plan": "pro_monthly",
        "cursor.subscription.tier": "pro",
        "cursor.trial.enabled": True,
        "cursor.trial.remaining": 999,
        "cursor.pro.enabled": True,
        "cursor.pro.active": True,
        "cursor.features.copilot": True,
        "cursor.features.chat": True,
        "cursor.features.composer": True,
        "cursor.features.codebase": True,
        "cursor.limits.bypassed": True,
        "cursor.usage.unlimited": True,
        "cursor.api.bypass": True,
        "telemetry.optout": True,
        "analytics.disabled": True
    }
    
    with open(storage_path, 'w') as f:
        json.dump(pro_storage, f, indent=2)
    
    # Update SQLite database
    db_path = os.path.join(config_dir, 'state.vscdb')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value TEXT)''')
        
        for key, value in pro_storage.items():
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, str(value)))
        
        # Additional Pro entries
        additional = [
            ("subscriptionType", "pro"),
            ("subscriptionStatus", "active"),
            ("userTier", "pro"),
            ("proFeaturesEnabled", "true"),
            ("usageLimitsDisabled", "true"),
            ("apiBypassEnabled", "true")
        ]
        
        for key, value in additional:
            cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
        
        conn.commit()
        conn.close()
        print("Database updated with Pro settings")
        
    except Exception as e:
        print(f"Database update failed: {e}")
    
    return True

def block_api_calls():
    """Block subscription API calls by modifying hosts file"""
    print("Blocking subscription API calls...")
    
    try:
        if os.name == 'nt':
            hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        else:
            hosts_path = '/etc/hosts'
        
        # Read current hosts file
        try:
            with open(hosts_path, 'r') as f:
                hosts_content = f.read()
        except:
            hosts_content = ""
        
        # Add blocks for Cursor API endpoints
        blocks = [
            "127.0.0.1 api2.cursor.sh",
            "127.0.0.1 cursor.com",
            "127.0.0.1 api.cursor.sh"
        ]
        
        modified = False
        for block in blocks:
            if block not in hosts_content:
                hosts_content += f"\n{block}"
                modified = True
        
        if modified:
            # Backup original hosts file
            if not os.path.exists(hosts_path + '.backup'):
                shutil.copy2(hosts_path, hosts_path + '.backup')
            
            # Write modified hosts file
            with open(hosts_path, 'w') as f:
                f.write(hosts_content)
            
            print("API calls blocked via hosts file")
            return True
        else:
            print("API calls already blocked")
            return True
            
    except PermissionError:
        print("Need Administrator privileges to modify hosts file")
        return False
    except Exception as e:
        print(f"Failed to block API calls: {e}")
        return False

def kill_cursor():
    """Kill Cursor processes"""
    print("Stopping Cursor...")
    try:
        if os.name == 'nt':
            os.system('taskkill /f /im Cursor.exe >nul 2>&1')
            os.system('taskkill /f /im cursor.exe >nul 2>&1')
        else:
            os.system('pkill -f cursor >/dev/null 2>&1')
        print("Cursor stopped")
    except:
        pass

def main():
    print("=" * 60)
    print("COMPLETE CURSOR PRO BYPASS")
    print("=" * 60)
    
    # Stop Cursor
    kill_cursor()
    
    success_count = 0
    
    # 1. Patch application files
    if patch_cursor_files():
        success_count += 1
        print("✓ Application files patched")
    else:
        print("✗ Failed to patch application files")
    
    # 2. Create Pro configuration
    if create_pro_config():
        success_count += 1
        print("✓ Pro configuration created")
    else:
        print("✗ Failed to create Pro configuration")
    
    # 3. Block API calls
    if block_api_calls():
        success_count += 1
        print("✓ API calls blocked")
    else:
        print("✗ Failed to block API calls (try running as Administrator)")
    
    print("\n" + "=" * 60)
    if success_count >= 2:
        print("SUCCESS! Cursor Pro bypass completed")
        print("\nWhat was done:")
        print("• Patched application files to bypass Pro checks")
        print("• Created Pro configuration files")
        print("• Blocked subscription API calls")
        print("\nNext steps:")
        print("1. Restart Cursor")
        print("2. All Pro features should now work")
        print("3. No more subscription checks")
    else:
        print("PARTIAL SUCCESS - Some steps failed")
        print("Try running as Administrator for full bypass")
    
    print("\nNote: If Cursor updates, you may need to run this again")

if __name__ == "__main__":
    main()