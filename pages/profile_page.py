import time
from os import times

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProfilePage:
    def __init__(self, driver):
        self.appium_driver = driver

    # Method to tap on the Profile button
    def click_profile_button(self):
        try:
            # Find the Profile icon using XPath
            profile_button = self.appium_driver.find_element(by=AppiumBy.XPATH,
                                                             value="//android.widget.TextView[@text='Profile']")
            # Click the Profile button
            profile_button.click()
            print("Appium: Clicked on 'Profile' button.")
            time.sleep(5)
        except Exception as e:
            print(f"Failed to click Profile button: {str(e)}")

    def verify_profile_page_elements(self):
        wait = WebDriverWait(self.appium_driver, 10)

        # List of element names and their XPaths for the Profile page
        elements_to_verify = {
            "Profile icon": "//android.view.View[@content-desc='Profile']/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup",
            "Profile text": "//android.widget.TextView[@text='Profile']",
            "Guest user image": "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.ImageView",
            "Settings icon": "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup",
            "Chat icon": "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.view.ViewGroup",
            "Guest user name": "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.view.ViewGroup",
            "Guest user handle": "//android.widget.TextView[@text='@NoHandleYet']",
            "Signin button": "//android.widget.TextView[@text='Sign in']",
            "Signin with Google": "//android.widget.TextView[@text='Sign in with Google']",


            # Will add more elements as needed
        }
        # Loop through the elements and verify if each is displayed and enabled
        for element_name, xpath in elements_to_verify.items():
            try:
                # Locate the element using the provided XPath
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

                # Verify if the element is displayed
                is_displayed = element.is_displayed()

                # Verify if the element is enabled
                is_enabled = element.is_enabled()

                # Print results for each element
                if is_displayed and is_enabled:
                    print(f"{element_name}: Displayed and Enabled.")
                else:
                    print(f"{element_name}: Displayed or Enabled status failed.")
            except TimeoutException:
                print(f"{element_name}: Not found (Timeout).")

    # Method to profile stats (Followers, Following, Likes)
    def profile_stats(self):
        wait = WebDriverWait(self.appium_driver, 10)

        try:
            # Retrieve and print Followers count and label
            followers_count_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[7]')))
            followers_count = followers_count_element.text
            followers_label_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[8]')))
            followers_label = followers_label_element.text
            print(f"{followers_label}: {followers_count}")

            # Retrieve and print Following count and label
            following_count_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[9]')))
            following_count = following_count_element.text
            following_label_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[10]')))
            following_label = following_label_element.text
            print(f"{following_label}: {following_count}")

            # Retrieve and print Likes count and label
            likes_count_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[11]')))
            likes_count = likes_count_element.text
            likes_label_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[12]')))
            likes_label = likes_label_element.text
            print(f"{likes_label}: {likes_count}")

        except TimeoutException as e:
            print(f"Error retrieving social counts: {str(e)}")

    def verify_avatar_and_game_sections(self):
        wait = WebDriverWait(self.appium_driver, 15)

        # List of element names and their XPaths
        elements_to_verify = {
            "Create Avatar Button": '//android.widget.TextView[@text="Create Avatar"]',
            "Avatar Box": '//android.widget.HorizontalScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView',
            "Games Section": '//android.widget.TextView[@text="Games"]',
            "Drafts Section": '//android.view.View[@content-desc=" Drafts"]',
            "Drafts Locked": '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]',
            "Published Games": '//android.view.View[@content-desc="Published games"]',
            "No Created Games Message": '//android.widget.TextView[@text="You haven\'t created any games yet. Get started now!"]',
            "Create Button": '//android.widget.TextView[@text="Create!"]',
            "Activity Section": '//android.widget.TextView[@text="Activity"]',
            "Likes Section": '//android.view.View[@content-desc="Likes"]',
            "Liked Games Message": '//android.widget.TextView[@text="Games you\'ve liked will appear here."]',
            "Play Button (Activity)": '(//android.widget.TextView[@text="Play"])[1]',
            "Recently Played": '//android.view.View[@content-desc="Recently played"]',
            "Recently Played Message": '//android.widget.TextView[@text="Games you\'ve played will appear here."]',
            "Play Button (Recently Played)": '(//android.widget.TextView[@text="Play"])[1]'
        }

        try:
            # Step 1: Verify "Create Avatar" is displayed
            create_avatar_button = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Create Avatar Button"])))
            create_avatar_button.is_displayed()
            print("'Create Avatar' button is displayed.")

            # Step 2: Verify Avatar Box is displayed
            avatar_box = wait.until(EC.visibility_of_element_located((By.XPATH, elements_to_verify["Avatar Box"])))
            assert avatar_box.is_displayed(), "Avatar box is not displayed."

            # Step 3: Verify "Games" section
            games_section = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Games Section"])))
            assert games_section.is_displayed(), "Games section is not displayed."

            # Step 4: Verify "Drafts" and "Drafts locked"
            drafts = wait.until(EC.visibility_of_element_located((By.XPATH, elements_to_verify["Drafts Section"])))
            assert drafts.is_displayed(), "Drafts section is not displayed."

            drafts_locked = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Drafts Locked"])))
            assert drafts_locked.is_displayed(), "Drafts locked section is not displayed."

            # Step 5: Click on "Published games" and verify elements
            published_games = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Published Games"])))
            published_games.click()
            print("Clicked on 'Published games'.")

            msg_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["No Created Games Message"])))
            assert msg_element.is_displayed(), "Message about no created games is not displayed."

            create_button = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Create Button"])))
            assert create_button.is_displayed(), "Create button is not displayed."

            # Step 6: Click on "Activity" section
            activity_section = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Activity Section"])))
            activity_section.click()
            print("Clicked on 'Activity' section.")

            # Step 7: Verify Likes and related elements
            likes_section = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Likes Section"])))
            assert likes_section.is_displayed(), "Likes section is not displayed."

            activity_msg = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Liked Games Message"])))
            assert activity_msg.is_displayed(), "Message about liked games is not displayed."

            play_button = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Play Button (Activity)"])))
            assert play_button.is_displayed(), "Play button in Activity section is not displayed."

            # Step 8: Click on "Recently played"
            recently_played = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Recently Played"])))
            recently_played.click()
            print("Clicked on 'Recently played'.")

            # Step 9: Verify Recently played message and play button
            recently_played_msg = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Recently Played Message"])))
            assert recently_played_msg.is_displayed(), "Message about recently played games is not displayed."

            recently_played_play_button = wait.until(
                EC.visibility_of_element_located((By.XPATH, elements_to_verify["Play Button (Recently Played)"])))
            assert recently_played_play_button.is_displayed(), "Play button in Recently played section is not displayed."

            print("All elements verified successfully.")

        except TimeoutException as e:
            print(f"Error in verifying elements: {str(e)}")
        except AssertionError as e:
            print(f"Assertion error: {str(e)}")

    def edit_profile(self):
        wait = WebDriverWait(self.appium_driver, 15)

        # XPaths used in the function
        xpaths = {
            "username": '(//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.TextView)[3]',
            "userhandle": '(//android.widget.FrameLayout[@resource-id="android:id/content"]//android.widget.TextView)[4]',
            "edit_button": '//android.widget.TextView[@text="Edit"]',
            # Edit Profile Page elements
            "cross_button": '//com.horcrux.svg.GroupView/com.horcrux.svg.PathView[2]',
            "edit_profile_title": '//android.widget.TextView[@text="Edit Profile"]',
            "display_name_label": '//android.widget.TextView[@text="Display Name:"]',
            "display_name_input": '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]',
            "username_label": '//android.widget.TextView[@text="@Username:"]',
            "username_textbox": '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[3]',
            "bio_label": '//android.widget.TextView[@text="Bio"]',
            "bio_input": '//android.widget.ScrollView/android.view.ViewGroup/android.widget.EditText',
            "save_button": '//android.widget.TextView[@text="Save"]'
        }

        try:
            # Step 1: Get text and store from Username and Userhandle
            username_element = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["username"])))
            userhandle_element = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["userhandle"])))

            username_text = username_element.text
            userhandle_text = userhandle_element.text

            print(f"Username: {username_text}")
            print(f"Userhandle: {userhandle_text}")

            # Step 2: Click on Edit button
            edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["edit_button"])))
            edit_button.click()
            print("Clicked on 'Edit' button.")

            # Step 3: Verify elements on Edit Profile Page
            elements_to_verify = {
                "Cross button": xpaths["cross_button"],
                "Edit Profile title": xpaths["edit_profile_title"],
                "Display Name label": xpaths["display_name_label"]
            }

            for element_name, xpath in elements_to_verify.items():
                element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                assert element.is_displayed(), f"{element_name} is not displayed."
                print(f"{element_name} is displayed.")

            # Step 4: Clear and enter name in Display Name input field
            display_name_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["display_name_input"])))
            display_name_input.clear()
            display_name_input.send_keys("Automationuser1")
            print("Entered 'Automationuser1' in Display Name input field.")

            # Step 5: Verify Username field
            username_label = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["username_label"])))
            assert username_label.is_displayed(), "Username label is not displayed."
            print("Username label is displayed.")

            # Step 6: Get text from Username textbox
            username_textbox = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["username_textbox"])))
            username_textbox_value = username_textbox.text
            print(f"Username Textbox: {username_textbox_value}")

            # Step 7: Verify Bio label
            bio_label = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["bio_label"])))
            assert bio_label.is_displayed(), "Bio label is not displayed."
            print("Bio label is displayed.")

            # Step 8: Enter text in Bio input field
            bio_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["bio_input"])))
            bio_input.clear()
            bio_input.send_keys("Automation user 1 bio")
            print("Entered 'Automation user 1 bio' in Bio input field.")

            # Step 9: Click on Save button
            save_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["save_button"])))
            save_button.click()
            print("Clicked on 'Save' button.")

            # Step 10: Verify profile is updated and get updated Username and Userhandle
            updated_username = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["username"])))
            updated_userhandle = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["userhandle"])))

            print(f"Updated Username: {updated_username.text}")
            print(f"Updated Userhandle: {updated_userhandle.text}")

        except TimeoutException as e:
            print(f"Error: {str(e)}")
        except AssertionError as e:
            print(f"Assertion Error: {str(e)}")







