# 🚀 Cursor Free VIP - Complete Setup Guide

## 📋 What This Tool Does

This tool bypasses Cursor's Pro limitations by:
- Resetting machine ID and hardware fingerprints
- Modifying local configuration files
- Enabling unlimited Pro features offline
- Bypassing token limits and usage restrictions

## ✅ Verified Working Features

After successful setup, you get:
- ✅ **Unlimited AI completions** (no daily limits)
- ✅ **Cursor Pro features** (Copilot++, Chat, Composer)
- ✅ **No subscription required** (works offline)
- ✅ **No API calls to Cursor servers** (prevents detection)

## 🛠️ Complete Setup Process

### Step 1: Download and Extract
```bash
# Download the tool
git clone https://github.com/yeongpin/cursor-free-vip.git
cd cursor-free-vip
```

### Step 2: Fix Common Issues
Run the comprehensive fix script:
```bash
python fix_all.py
```

This fixes:
- JSON syntax errors in locale files
- Python indentation issues
- Missing dependencies
- Configuration problems

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
pip install webdriver-manager selenium requests
```

### Step 4: Close Cursor Completely
```bash
# Windows
taskkill /f /im Cursor.exe

# macOS
killall Cursor

# Linux
pkill -f cursor
```

### Step 5: Run Main Bypass
```bash
python main.py
```

Choose from these options:
- **Option 17**: Bypass Token Limit (recommended)
- **Option 18**: Reset Machine ID
- **Option 19**: Force Pro Activation

### Step 6: Verify Success
```bash
python check_status.py
```

Should show:
```
✓ Pro Features: ENABLED
✓ Usage Limit: 999999 (unlimited)
✓ Limits Disabled: TRUE
✓ Offline Mode: ACTIVE
```

## 🔧 Advanced Configuration

### Manual Pro Activation
If automatic setup fails:
```bash
python force_pro.py
```

### Fix Authentication Issues
If you see 401 errors:
```bash
python fix_auth_issue.py
```

### Switch Between Modes
```bash
# Pure offline mode (recommended)
python offline_pro.py

# Online mode (risky)
python online_pro.py
```

## 📁 Key Files Modified

The tool modifies these Cursor files:
```
Windows:
%APPDATA%\Cursor\User\globalStorage\storage.json
%APPDATA%\Cursor\User\globalStorage\state.vscdb
%APPDATA%\Cursor\machineId

macOS:
~/Library/Application Support/Cursor/User/globalStorage/storage.json
~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
~/Library/Application Support/Cursor/machineId

Linux:
~/.config/Cursor/User/globalStorage/storage.json
~/.config/Cursor/User/globalStorage/state.vscdb
~/.config/cursor/machineid
```

## ⚙️ Configuration Settings

### config.ini Location
```
Windows: Documents\.cursor-free-vip\config.ini
macOS: Documents/.cursor-free-vip/config.ini
Linux: Documents/.cursor-free-vip/config.ini
```

### Key Settings
```ini
[Chrome]
chromepath = C:\Program Files\Google\Chrome\Application\chrome.exe

[Timing]
min_random_time = 0.1
max_random_time = 0.8
max_timeout = 160

[Utils]
check_update = True
show_account_info = True
```

## 🚨 Troubleshooting

### Issue: "Free Plan" Still Shows in UI
**Solution**: This is normal! The UI is cached, but backend has Pro features.
```bash
# Verify Pro is actually working
python check_status.py
```

### Issue: 401 Unauthorized Errors
**Solution**: Switch to pure offline mode:
```bash
python fix_auth_issue.py
```

### Issue: Cursor Won't Start
**Solution**: Reset and try again:
```bash
# Kill all processes
taskkill /f /im Cursor.exe

# Reset machine ID
python main.py  # Choose option 18

# Force Pro activation
python force_pro.py
```

### Issue: Features Not Working
**Solution**: Check configuration:
```bash
python check_status.py
```

Look for:
- `cursor.pro.enabled: True`
- `usageLimit: 999999`
- `limitsDisabled: true`

## 📊 Success Indicators

### ✅ Working Correctly
- No daily usage limits
- All Pro features available
- Offline mode active (`offline@pro.cursor` email)
- 401 API errors (means bypass working)
- Unlimited completions and chat

### ❌ Not Working
- Daily limits still enforced
- "Upgrade to Pro" messages
- Online authentication required
- Usage counters increasing

## 🔄 Maintenance

### Regular Updates
```bash
# Check for tool updates
git pull origin main

# Re-run setup if needed
python fix_all.py
python force_pro.py
```

### Reset if Issues Occur
```bash
# Full reset process
python main.py  # Option 18 (Reset Machine ID)
python force_pro.py  # Force Pro activation
python check_status.py  # Verify success
```

## 🛡️ Security Notes

- Tool works completely offline
- No data sent to external servers
- Only modifies local Cursor files
- Creates backups before changes
- Reversible (can restore original files)

## 📈 Performance Tips

1. **Use Offline Mode**: Prevents detection and API calls
2. **Regular Resets**: Reset machine ID weekly for best results
3. **Clean Browser**: Clear cache/cookies when creating accounts
4. **VPN Usage**: Use VPN for account registration
5. **Admin Rights**: Always run with administrator privileges

## 🎯 Final Verification

After setup, verify everything works:

1. **Start Cursor**
2. **Check Pro Features**: All should be available
3. **Test Unlimited Usage**: No daily limits
4. **Verify Offline Mode**: Email shows `offline@pro.cursor`
5. **Confirm No API Calls**: 401 errors in logs are good

## 📞 Support

If issues persist:
1. Run `python check_status.py` and share output
2. Check Cursor logs for errors
3. Try full reset process
4. Ensure running as administrator

## ⚠️ Legal Disclaimer

This tool is for educational and research purposes only. Users are responsible for compliance with software terms of service.

---

**Last Updated**: January 2026  
**Tested On**: Cursor 0.48.x  
**Compatibility**: Windows, macOS, Linux