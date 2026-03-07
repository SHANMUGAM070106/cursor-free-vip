import os
import sys
import platform
import random
import datetime


def log_step(step_name: str) -> None:
    """Print a timestamped log message.
    
    Args:
        step_name: Description of the current step
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {step_name}")

def get_user_documents_path():
    """Get user documents path"""
    if platform.system() == "Windows":
        return os.path.expanduser("~\\Documents")
    else:
        return os.path.expanduser("~/Documents")

def get_default_chrome_path():
    """Get default Chrome path"""
    if sys.platform == "win32":
        #  Trying to find chrome in PATH
        try:
            import shutil
            chrome_in_path = shutil.which("chrome")
            if chrome_in_path:
                return chrome_in_path
        except:
            pass
        # Going to default path
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    elif sys.platform == "darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:
        return "/usr/bin/google-chrome"

def get_linux_cursor_path():
    """Get Linux Cursor path"""
    possible_paths = [
        "/opt/Cursor/resources/app",
        "/usr/share/cursor/resources/app",
        "/opt/cursor-bin/resources/app",
        "/usr/lib/cursor/resources/app",
        os.path.expanduser("~/.local/share/cursor/resources/app")
    ]
    
    # return the first path that exists
    return next((path for path in possible_paths if os.path.exists(path)), possible_paths[0])

def get_random_wait_time(config, timing_key):
    """Get random wait time based on configuration timing settings
    
    Args:
        config (dict): Configuration dictionary containing timing settings
        timing_key (str): Key to look up in the timing settings
        
    Returns:
        float: Random wait time in seconds
    """
    try:
        # Get timing value from config
        timing = config.get('Timing', {}).get(timing_key)
        if not timing:
            # Default to 0.5-1.5 seconds if timing not found
            return random.uniform(0.5, 1.5)
            
        # Check if timing is a range (e.g., "0.5-1.5" or "0.5,1.5")
        if isinstance(timing, str):
            if '-' in timing:
                min_time, max_time = map(float, timing.split('-'))
            elif ',' in timing:
                min_time, max_time = map(float, timing.split(','))
            else:
                # Single value, use it as both min and max
                min_time = max_time = float(timing)
        else:
            # If timing is a number, use it as both min and max
            min_time = max_time = float(timing)
            
        return random.uniform(min_time, max_time)
        
    except (ValueError, TypeError, AttributeError):
        # Return default value if any error occurs
        return random.uniform(0.5, 1.5) 