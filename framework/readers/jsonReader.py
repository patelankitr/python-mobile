import json
# D:\\Projects\\python-mobile\\config\\TestConfig.json
class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self._read_config()

    def _read_config(self):
        """Read and parse the JSON config file"""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in config file: {self.file_path}")

    def get_config(self):
        """Get the complete config"""
        return self.config

    def get_platform_config(self, platform=None):
        """
        Get platform-specific configuration
        If platform is not specified, uses the 'run' value from config
        """
        try:
            if platform is None:
                platform = self.config.get("run")
                if not platform:
                    raise ValueError("'run' parameter is missing in config file")

            # Handle iOS case sensitivity
            if platform.lower() == "ios":
                platform = "iOS"

            platform_config = self.config.get("config", {}).get(platform)
            if not platform_config:
                raise ValueError(f"Configuration for platform '{platform}' not found")

            return platform_config

        except Exception as e:
            raise ValueError(f"Error getting platform config: {str(e)}")

    def get_run_platform(self):
        """Get the current run platform from config"""
        return self.config.get("run")

    def get_capabilities(self, platform=None):
        """Get capabilities for specific platform"""
        platform_config = self.get_platform_config(platform)
        return platform_config.get("capabilities", {})