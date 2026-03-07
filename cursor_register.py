import os
from colorama import Fore, Style, init
import time
import random
from cursor_auth import CursorAuth
from reset_machine_manual import MachineIDResetter

os.environ["PYTHONVERBOSE"] = "0"
os.environ["PYINSTALLER_VERBOSE"] = "0"

# Initialize colorama
init()

# Define emoji constants
EMOJI = {
    'START': '🚀',
    'FORM': '📝',
    'VERIFY': '🔄',
    'PASSWORD': '🔑',
    'CODE': '📱',
    'DONE': '✨',
    'ERROR': '❌',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'MAIL': '📧',
    'KEY': '🔐',
    'UPDATE': '🔄',
    'INFO': 'ℹ️'
}

class CursorRegistration:
    def __init__(self, translator=None):
        self.translator = translator
        # Set to display mode
        os.environ['BROWSER_HEADLESS'] = 'False'
        self.browser = None
        self.controller = None
        self.mail_url = "https://yopmail.com/zh/email-generator"
        self.sign_up_url = "https://authenticator.cursor.sh/sign-up"
        self.settings_url = "https://www.cursor.com/settings"
        self.email_address = None
        self.signup_tab = None
        self.email_tab = None
        
        # Account information
        self.password = self._generate_password()
        # Generate first name and last name separately
        first_name = random.choice([
            "James", "John", "Robert", "Michael", "William", "David", "Joseph", "Thomas",
            "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia",
            "Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mason", "Logan", "Alexander"
        ])
        self.last_name = random.choice([
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Anderson", "Wilson", "Taylor", "Thomas", "Moore", "Martin", "Jackson", "Lee",
            "Thompson", "White", "Harris", "Clark", "Lewis", "Walker", "Hall", "Young"
        ])
        
        # Modify first letter of first name
        new_first_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.first_name = new_first_letter + first_name[1:]
        
        print(f"\n{Fore.CYAN}{EMOJI['PASSWORD']} {self.translator.get('register.password')}: {self.password} {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['FORM']} {self.translator.get('register.first_name')}: {self.first_name} {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['FORM']} {self.translator.get('register.last_name')}: {self.last_name} {Style.RESET_ALL}")

    def _generate_password(self, length=12):
        """Generate Random Password"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(random.choices(chars, k=length))

    def setup_email(self):
        """Setup Email"""
        try:
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.browser_start')}...{Style.RESET_ALL}")
            
            # Create a temporary email using new_tempemail, passing translator
            from new_tempemail import NewTempEmail
            self.temp_email = NewTempEmail(self.translator)  # Pass translator
            
            # Create a temporary email
            email_address = self.temp_email.create_email()
            if not email_address:
                print(f"{Fore.RED}{EMOJI['ERROR']} Email creation failed{Style.RESET_ALL}")
                return False
            
            # Save email address
            self.email_address = email_address
            self.email_tab = self.temp_email  # Pass NewTempEmail instance
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Email setup error: {str(e)}{Style.RESET_ALL}")
            return False

    def register_cursor(self):
        """注册 Cursor"""
        browser_tab = None
        try:
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.register_start')}...{Style.RESET_ALL}")
            
            # Directly use new_signup.py to sign up
            from new_signup import main as new_signup_main
            
            # Execute the new registration process, passing translator
            result, browser_tab = new_signup_main(
                email=self.email_address,
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name,
                email_tab=self.email_tab,
                controller=self.controller,
                translator=self.translator
            )
            
            if result:
                # Use the returned browser instance to get account information
                self.signup_tab = browser_tab  # Save browser instance
                success = self._get_account_info()
                
                # Close browser after getting information
                if browser_tab:
                    try:
                        browser_tab.quit()
                    except:
                        pass
                
                return success
            
            return False
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.register_process_error', error=str(e))}{Style.RESET_ALL}")
            return False
        finally:
            # Ensure browser is closed in any case
            if browser_tab:
                try:
                    browser_tab.quit()
                except:
                    pass
                
    def _get_account_info(self):
        """Get Account Information and Token"""
        try:
            self.signup_tab.get(self.settings_url)
            time.sleep(2)
            
            usage_selector = (
                "css:div.col-span-2 > div > div > div > div > "
                "div:nth-child(1) > div.flex.items-center.justify-between.gap-2 > "
                "span.font-mono.text-sm\\/\\[0\\.875rem\\]"
            )
            usage_ele = self.signup_tab.ele(usage_selector)
            total_usage = "未知"
            if usage_ele:
                total_usage = usage_ele.text.split("/")[-1].strip()

            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('register.total_usage', usage=total_usage)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{EMOJI['WAIT']} {self.translator.get('register.get_token')}...{Style.RESET_ALL}")
            max_attempts = 30
            retry_interval = 2
            attempts = 0

            while attempts < max_attempts:
                try:
                    cookies = self.signup_tab.cookies()
                    for cookie in cookies:
                        if cookie.get("name") == "WorkosCursorSessionToken":
                            token = cookie["value"].split("%3A%3A")[1]
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.token_success')}{Style.RESET_ALL}")
                            self._save_account_info(token, total_usage)
                            return True

                    attempts += 1
                    if attempts < max_attempts:
                        print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.token_attempt', attempt=attempts, time=retry_interval)}{Style.RESET_ALL}")
                        time.sleep(retry_interval)
                    else:
                        print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.token_max_attempts', max=max_attempts)}{Style.RESET_ALL}")

                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.token_failed', error=str(e))}{Style.RESET_ALL}")
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.token_attempt', attempt=attempts, time=retry_interval)}{Style.RESET_ALL}")
                        time.sleep(retry_interval)

            return False

        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.account_error', error=str(e))}{Style.RESET_ALL}")
            return False

    def _save_account_info(self, token, total_usage):
        """Save Account Information to File"""
        try:
            # Update authentication information first
            print(f"{Fore.CYAN}{EMOJI['KEY']} {self.translator.get('register.update_cursor_auth_info')}...{Style.RESET_ALL}")
            if self.update_cursor_auth(email=self.email_address, access_token=token, refresh_token=token):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.cursor_auth_info_updated')}...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.cursor_auth_info_update_failed')}...{Style.RESET_ALL}")

            # Save account information to file
            account_info = {
                "email": self.email_address,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "token": token,
                "usage": total_usage
            }
            
            # Write to file
            try:
                with open("cursor_accounts.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {account_info['email']}\n")
                    f.write(f"Password: {account_info['password']}\n")
                    f.write(f"First Name: {account_info['first_name']}\n")
                    f.write(f"Last Name: {account_info['last_name']}\n")
                    f.write(f"Token: {account_info['token']}\n")
                    f.write(f"Usage: {account_info['usage']}\n")
                    f.write("-" * 50 + "\n")
                    
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.account_info_saved')}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.save_account_info_failed', error=str(e))}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.save_account_info_failed', error=str(e))}{Style.RESET_ALL}")

    def update_cursor_auth(self, email, access_token, refresh_token):
        """Update Cursor authentication information"""
        try:
            cursor_auth = CursorAuth()
            return cursor_auth.update_auth_info(
                email=email,
                access_token=access_token,
                refresh_token=refresh_token
            )
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Update auth error: {str(e)}{Style.RESET_ALL}")
            return False

    def run(self):
        """Run the registration process"""
        try:
            print(f"\n{'='*50}")
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.title')}{Style.RESET_ALL}")
            print(f"{'='*50}\n")
            
            # Setup email
            if not self.setup_email():
                return False
                
            # Register Cursor account
            if not self.register_cursor():
                return False
                
            print(f"\n{Fore.GREEN}{EMOJI['DONE']} {self.translator.get('register.cursor_registration_completed')}{Style.RESET_ALL}")
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}{EMOJI['EXIT']} {self.translator.get('register.exit_signal')}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.register_process_error', error=str(e))}{Style.RESET_ALL}")
            return False
        finally:
            # Clean up
            if hasattr(self, 'temp_email') and self.temp_email:
                try:
                    self.temp_email.close()
                except:
                    pass
            if self.signup_tab:
                try:
                    self.signup_tab.quit()
                except:
                    pass

def main(translator=None):
    """Main function for registration"""
    registration = CursorRegistration(translator)
    success = registration.run()
    
    if success:
        print(f"\n{Fore.GREEN}✅ Registration completed successfully!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ Registration failed!{Style.RESET_ALL}")
    
    input(f"\n{registration.translator.get('register.press_enter')}...")
    return success

if __name__ == "__main__":
    main()o_update_failed')}...{Style.RESET_ALL}")

            # Save account information to file
            account_info = {
                "email": self.email_address,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "token": token,
                "usage": total_usage
            }
            
            # Write to file
            try:
                with open("cursor_accounts.txt", "a", encoding="utf-8") as f:
                    f.write(f"Email: {account_info['email']}\n")
                    f.write(f"Password: {account_info['password']}\n")
                    f.write(f"First Name: {account_info['first_name']}\n")
                    f.write(f"Last Name: {account_info['last_name']}\n")
                    f.write(f"Token: {account_info['token']}\n")
                    f.write(f"Usage: {account_info['usage']}\n")
                    f.write("-" * 50 + "\n")
                    
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.account_info_saved')}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.save_account_info_failed', error=str(e))}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.save_account_info_failed', error=str(e))}{Style.RESET_ALL}")

    def update_cursor_auth(self, email, access_token, refresh_token):
        """Update Cursor authentication information"""
        try:
            cursor_auth = CursorAuth()
            return cursor_auth.update_auth_info(
                email=email,
                access_token=access_token,
                refresh_token=refresh_token
            )
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Update auth error: {str(e)}{Style.RESET_ALL}")
            return False

    def run(self):
        """Run the registration process"""
        try:
            print(f"\n{'='*50}")
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.title')}{Style.RESET_ALL}")
            print(f"{'='*50}\n")
            
            # Setup email
            if not self.setup_email():
                return False
                
            # Register Cursor account
            if not self.register_cursor():
                return False
                
            print(f"\n{Fore.GREEN}{EMOJI['DONE']} {self.translator.get('register.cursor_registration_completed')}{Style.RESET_ALL}")
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}{EMOJI['EXIT']} {self.translator.get('register.exit_signal')}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.register_process_error', error=str(e))}{Style.RESET_ALL}")
            return False
        finally:
            # Clean up
            if hasattr(self, 'temp_email') and self.temp_email:
                try:
                    self.temp_email.close()
                except:
                    pass
            if self.signup_tab:
                try:
                    self.signup_tab.quit()
                except:
                    pass

def main(translator=None):
    """Main function for registration"""
    registration = CursorRegistration(translator)
    success = registration.run()
    
    if success:
        print(f"\n{Fore.GREEN}✅ Registration completed successfully!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ Registration failed!{Style.RESET_ALL}")
    
    input(f"\n{registration.translator.get('register.press_enter')}...")
    return success

if __name__ == "__main__":
    main()o_update_failed')}...{Style.RESET_ALL}")

            # Reset machine ID
            print(f"{Fore.CYAN}{EMOJI['UPDATE']} {self.translator.get('register.reset_machine_id')}...{Style.RESET_ALL}")
            resetter = MachineIDResetter(self.translator)  # Pass translator when creating instance
            if not resetter.reset_machine_ids():  # Call reset_machine_ids method directly
                raise Exception("Failed to reset machine ID")
            
            # Save account information to file
            with open('cursor_accounts.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Email: {self.email_address}\n")
                f.write(f"Password: {self.password}\n")
                f.write(f"Token: {token}\n")
                f.write(f"Usage Limit: {total_usage}\n")
                f.write(f"{'='*50}\n")
                
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.account_info_saved')}...{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.save_account_info_failed', error=str(e))}{Style.RESET_ALL}")
            return False

    def start(self):
        """Start Registration Process"""
        try:
            if self.setup_email():
                if self.register_cursor():
                    print(f"\n{Fore.GREEN}{EMOJI['DONE']} {self.translator.get('register.cursor_registration_completed')}...{Style.RESET_ALL}")
                    return True
            return False
        finally:
            # Close email tab
            if hasattr(self, 'temp_email'):
                try:
                    self.temp_email.close()
                except:
                    pass

    def update_cursor_auth(self, email=None, access_token=None, refresh_token=None):
        """Update Cursor Auth Info"""
        auth_manager = CursorAuth(translator=self.translator)
        return auth_manager.update_auth(email, access_token, refresh_token)

def main(translator=None):
    """Main function to be called from main.py"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['START']} {translator.get('register.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    registration = CursorRegistration(translator)
    registration.start()

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} {translator.get('register.press_enter')}...")

if __name__ == "__main__":
    from main import translator as main_translator
    main(main_translator) 