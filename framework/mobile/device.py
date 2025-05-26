from framework.mobile.prints import text_print

class Device:
    def __init__(self, driver):
        if not driver:
            raise ValueError("Driver cannot be None")
        self.driver = driver
        text_print("Device class initialized successfully", 'green')

    def get_device_battery_level(self):
        """
        Gets the current battery level of the device.

        Returns:
            int: Battery level percentage (0-100)
        """
        try:
            # Get battery info from device
            battery_info = self.driver.execute_script('mobile: batteryInfo')
            
            # Extract battery level and convert to percentage
            battery_level = int(float(battery_info.get('level', 0)) * 100)
            
            text_print(f"Device battery level: {battery_level}%", 'green')
            return battery_level
            
        except Exception as e:
            raise Exception(f"Error getting device battery level: {str(e)}")

    def rotate_device(self, orientation):
        """
        Rotates the device to the specified orientation.

        Args:
            orientation (str): Desired orientation ('PORTRAIT', 'LANDSCAPE', 'PORTRAIT_REVERSE', 'LANDSCAPE_REVERSE')
        """
        try:
            # Validate orientation
            valid_orientations = ['PORTRAIT', 'LANDSCAPE', 'PORTRAIT_REVERSE', 'LANDSCAPE_REVERSE']
            orientation = orientation.upper()
            
            if orientation not in valid_orientations:
                raise ValueError(f"Invalid orientation. Must be one of {valid_orientations}")
            
            # Rotate device
            self.driver.orientation = orientation
            text_print(f"Device rotated to {orientation}", 'green')
            
        except Exception as e:
            raise Exception(f"Error rotating device: {str(e)}")

    def lock_device(self, duration=None):
        """
        Locks the device for a specified duration or indefinitely.

        Args:
            duration (int, optional): Duration in seconds to keep device locked. 
                                    If None, device stays locked until unlock_device is called.
        """
        try:
            # Lock the device
            self.driver.lock()
            text_print("Device locked", 'green')
            
            # If duration specified, wait and then unlock
            if duration:
                import time
                time.sleep(duration)
                self.driver.unlock()
                text_print(f"Device automatically unlocked after {duration} seconds", 'green')
            
        except Exception as e:
            raise Exception(f"Error locking device: {str(e)}")

    def unlock_device(self, password=None):
        """
        Unlocks the device. If device requires password/PIN, it can be provided.

        Args:
            password (str, optional): Password/PIN to unlock the device if required
        """
        try:
            # Check if device is locked
            if self.driver.is_locked():
                # First unlock the screen
                self.driver.unlock()
                
                # If password provided, enter it using keycode events
                if password:
                    for digit in password:
                        # Convert string digit to integer keycode (0 = 7, 1 = 8, etc.)
                        keycode = int(digit) + 7
                        self.driver.press_keycode(keycode)
                    
                    # Press enter/confirm key
                    self.driver.press_keycode(66)  # KEYCODE_ENTER
                
                text_print("Device unlocked successfully", 'green')
            else:
                text_print("Device is already unlocked", 'green')
            
        except Exception as e:
            raise Exception(f"Error unlocking device: {str(e)}")


