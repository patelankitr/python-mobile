import json
from pathlib import Path

class ConfigReader:
    """ Reads JSON config based on platform (android, iOS, lambdaTest, browserStack) """

    def __init__(self, config_file=None):
        self.config_file = config_file or (Path(__file__).parent.parent / "config" / "TestConfig.json")

    def read_json(self):
        """ Reads JSON file and returns the parsed data """
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return {}

    def get_config(self):
        """ Extracts configuration for the selected platform """
        data = self.read_json()
        platform_key = data.get("run", "")

        # Debugging logs
        print(f"Selected Platform: {platform_key}")
        print(f"Available Config Keys: {list(data.get('config', {}).keys())}")

        return data.get("config", {}).get(platform_key, {})


# Example Usage
if __name__ == "__main__":
    reader = ConfigReader("D:\\Projects\\python-mo-framework\\config\\TestConfig.json")
    config = reader.get_config()

    if config:
        platform = config.get("platform")
        app = config.get("app")
        platformVersion = config.get("platformVersion")

        print("Configuration Found:", config)
        print(f"Platform: {platform}")
        print(f"App: {app}")
        print(f"Platform Version: {platformVersion}")
    else:
        print("No configuration found for the selected platform.")
