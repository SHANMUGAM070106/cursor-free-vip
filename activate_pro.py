#!/usr/bin/env python3
"""
Cursor Pro Activator - Run after successful OAuth
"""

import os
import json
import sqlite3
from pathlib import Path

def activate_pro_features():
    """Activate Pro features after OAuth"""
    print("🚀 Activating Cursor Pro features...")
    
    # Find Cursor config paths
    if os.name == 'nt':  # Windows
        config_base = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
        storage_path = os.path.join(config_base, 'storage.json')
        db_path = os.path.join(config_base, 'state.vscdb')
    else:
        config_base = os.path.expanduser('~/.config/cursor/User/globalStorage')
        storage_path = os.path.join(config_base, 'storage.json')
        db_path = os.path.join(config_base, 'state.vscdb')
    
    try:
        # Update storage.json for Pro features
        if os.path.exists(storage_path):
            with open(storage_path, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # Add Pro subscription info
            storage.update({
                "cursor.subscription.type": "pro",
                "cursor.subscription.status": "active",
                "cursor.trial.enabled": True,
                "cursor.trial.remaining": 14,
                "cursor.pro.enabled": True,
                "cursor.features.copilot": True,
                "cursor.features.chat": True,
                "cursor.features.composer": True
            })
            
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(storage, f, indent=2)
            
            print("✅ Updated storage.json with Pro features")
        
        # Update SQLite database
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            pro_settings = [
                ("cursor.subscription.type", "pro"),
                ("cursor.subscription.status", "active"),
                ("cursor.trial.enabled", "true"),
                ("cursor.trial.remaining", "14"),
                ("cursor.pro.enabled", "true"),
                ("cursor.features.copilot", "true"),
                ("cursor.features.chat", "true"),
                ("cursor.features.composer", "true")
            ]
            
            for key, value in pro_settings:
                cursor.execute(
                    "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
                    (key, value)
                )
            
            conn.commit()
            conn.close()
            print("✅ Updated database with Pro features")
        
        print("\n🎉 Cursor Pro features activated!")
        print("📋 Next steps:")
        print("1. Restart Cursor")
        print("2. Check Settings > Account for Pro status")
        print("3. Try using Copilot++ or Composer features")
        
    except Exception as e:
        print(f"❌ Error activating Pro features: {e}")

if __name__ == "__main__":
    activate_pro_features()