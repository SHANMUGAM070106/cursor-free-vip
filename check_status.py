#!/usr/bin/env python3
"""
Check what's actually working in Cursor
"""

import os
import json
import sqlite3

def check_cursor_status():
    print("Checking Cursor Status...")
    print("=" * 50)
    
    # Check config files
    config_dir = os.path.expandvars(r'%APPDATA%\Cursor\User\globalStorage')
    storage_path = os.path.join(config_dir, 'storage.json')
    db_path = os.path.join(config_dir, 'state.vscdb')
    
    print(f"Config directory: {config_dir}")
    print(f"Storage exists: {os.path.exists(storage_path)}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    # Check storage.json
    if os.path.exists(storage_path):
        try:
            with open(storage_path, 'r') as f:
                data = json.load(f)
            
            print("\nStorage.json settings:")
            pro_keys = [k for k in data.keys() if 'pro' in k.lower() or 'subscription' in k.lower() or 'limit' in k.lower()]
            for key in pro_keys:
                print(f"  {key}: {data[key]}")
                
        except Exception as e:
            print(f"Storage read error: {e}")
    
    # Check database
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%pro%' OR key LIKE '%subscription%' OR key LIKE '%limit%'")
            results = cursor.fetchall()
            
            print(f"\nDatabase settings ({len(results)} found):")
            for key, value in results:
                print(f"  {key}: {value}")
            
            conn.close()
            
        except Exception as e:
            print(f"Database read error: {e}")
    
    print("\n" + "=" * 50)
    print("TESTING INSTRUCTIONS:")
    print("1. Open Cursor")
    print("2. Try Ctrl+K (Copilot++) - should work unlimited")
    print("3. Try Ctrl+L (Chat) - should work unlimited") 
    print("4. Try Ctrl+I (Composer) - should work")
    print("5. If any of these work unlimited, bypass is successful!")
    print("\nNote: UI may still show 'Free Plan' but features should work")

if __name__ == "__main__":
    check_cursor_status()
    input("\nPress Enter to exit...")