#!/usr/bin/env python3
"""
Cursor Free VIP - Quick Fix Script
This script fixes common issues with the Cursor Free VIP tool
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def fix_json_syntax():
    """Fix JSON syntax errors"""
    print("Fixing JSON syntax errors...")
    
    json_files = [
        "locales/en.json",
        "locales/zh_cn.json", 
        "locales/zh_tw.json",
        "locales/vi.json"
    ]
    
    for json_file in json_files:
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix common JSON issues
                content = content.replace(',\n    }', '\n    }')  # Remove trailing commas
                content = content.replace(',\n}', '\n}')
                
                # Validate JSON
                json.loads(content)
                
                # Write back if valid
                with open(json_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"Fixed {json_file}")
            except Exception as e:
                print(f"Error fixing {json_file}: {e}")

def install_dependencies():
    """Install missing dependencies"""
    print("Installing missing dependencies...")
    
    dependencies = [
        "webdriver-manager",
        "DrissionPage",
        "colorama",
        "requests"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Installed {dep}")
        except:
            print(f"Failed to install {dep}")

def clear_cache():
    """Clear Python cache files"""
    print("Clearing Python cache...")
    
    try:
        # Remove __pycache__ directories
        for root, dirs, files in os.walk("."):
            if "__pycache__" in dirs:
                cache_dir = os.path.join(root, "__pycache__")
                try:
                    import shutil
                    shutil.rmtree(cache_dir)
                    print(f"Removed {cache_dir}")
                except:
                    pass
        
        # Remove .pyc files
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith('.pyc'):
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
                        
        print("Cache cleared")
    except Exception as e:
        print(f"Error clearing cache: {e}")

def fix_permissions():
    """Fix file permissions (Windows)"""
    if os.name == 'nt':
        print("Checking permissions...")
        try:
            # Check if running as admin
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("For full functionality, run as Administrator")
            else:
                print("Running with Administrator privileges")
        except:
            print("Could not check admin status")

def create_shortcuts():
    """Create helpful shortcuts"""
    print("Creating shortcuts...")
    
    # Create run as admin batch file
    batch_content = '''@echo off
cd /d "%~dp0"
echo Starting Cursor Free VIP...
python main.py
pause'''
    
    try:
        with open("run_as_admin.bat", "w") as f:
            f.write(batch_content)
        print("Created run_as_admin.bat")
    except:
        print("Failed to create batch file")

def test_functionality():
    """Test basic functionality"""
    print("Testing functionality...")
    
    try:
        # Test JSON loading
        with open("locales/en.json", "r", encoding="utf-8") as f:
            json.load(f)
        print("JSON files load correctly")
        
        # Test module imports
        try:
            import new_tempemail
            print("new_tempemail module imports correctly")
        except Exception as e:
            print(f"new_tempemail import error: {e}")
            
        try:
            import oauth_auth
            print("oauth_auth module imports correctly")
        except Exception as e:
            print(f"oauth_auth import error: {e}")
            
    except Exception as e:
        print(f"Test failed: {e}")

def main():
    """Main fix function"""
    print("Cursor Free VIP - Quick Fix Script")
    print("=" * 50)
    
    fix_json_syntax()
    install_dependencies()
    clear_cache()
    fix_permissions()
    create_shortcuts()
    test_functionality()
    
    print("\n" + "=" * 50)
    print("Fix script completed!")
    print("\nNext steps:")
    print("1. Close all Chrome/Chromium browsers")
    print("2. Run as Administrator for full functionality:")
    print("   - Right-click run_as_admin.bat -> Run as administrator")
    print("   - Or right-click main.py -> Run as administrator")
    print("3. Use Option 1 or 10 to reset Machine ID")
    print("4. Use Option 5 for manual registration")
    print("\nOAuth options (3,4) may need manual intervention due to Cursor's anti-automation measures")

if __name__ == "__main__":
    main()