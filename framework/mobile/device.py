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