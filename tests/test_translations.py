"""
Test translation files for validity.
"""
import json
import glob
import os

# Files that should have all required keys (new or updated translations)
FULL_TRANSLATIONS = {'en.json', 'it.json', 'pl.json', 'ar.json', 'ja.json', 'ko.json', 'fr.json'}


def test_all_translations_valid():
    """Test that all translation JSON files are valid."""
    locales_dir = os.path.join(os.path.dirname(__file__), '..', 'locales')
    
    for file_path in glob.glob(os.path.join(locales_dir, '*.json')):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                json.load(f)
                print(f"✅ {os.path.basename(file_path)} is valid")
            except json.JSONDecodeError as e:
                print(f"❌ {os.path.basename(file_path)}: {e}")
                raise


def test_translations_have_required_keys():
    """Test that translations have required top-level keys."""
    required_keys = {
        'menu', 'languages', 'quit_cursor', 'reset', 'register',
        'auth', 'control', 'email', 'update', 'updater',
        'totally_reset', 'github_register', 'account_info',
        'config', 'oauth', 'chrome_profile', 'account_delete',
        'bypass', 'auth_check', 'bypass_token_limit'
    }
    
    locales_dir = os.path.join(os.path.dirname(__file__), '..', 'locales')
    
    for file_path in glob.glob(os.path.join(locales_dir, '*.json')):
        filename = os.path.basename(file_path)
        
        # Only validate files that should have full translations
        if filename not in FULL_TRANSLATIONS:
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            missing = required_keys - set(data.keys())
            if missing:
                print(f"❌ {filename} missing keys: {missing}")
                raise AssertionError(f"Missing keys in {file_path}")
    
    print(f"✅ All full translations have required keys")


def test_english_is_complete():
    """Test that English translation is complete reference."""
    en_path = os.path.join(os.path.dirname(__file__), '..', 'locales', 'en.json')
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    locales_dir = os.path.join(os.path.dirname(__file__), '..', 'locales')
    
    for file_path in glob.glob(os.path.join(locales_dir, '*.json')):
        filename = os.path.basename(file_path)
        
        # Only validate files that should have full translations
        if filename not in FULL_TRANSLATIONS or filename == 'en.json':
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check that translation has same structure as English
        def compare_keys(en_section, trans_section, path=''):
            for key in en_section:
                if isinstance(en_section[key], dict):
                    if key not in trans_section:
                        print(f"❌ Missing section '{path}{key}' in {filename}")
                        raise AssertionError(f"Missing section {path}{key}")
                    compare_keys(en_section[key], trans_section[key], f"{path}{key}.")
        
        compare_keys(en_data, data)
    
    print(f"✅ All full translations have correct structure")


if __name__ == "__main__":
    print("Running translation tests...")
    test_all_translations_valid()
    test_translations_have_required_keys()
    test_english_is_complete()
    print("\n✅ All tests passed!")
