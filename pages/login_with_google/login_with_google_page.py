# -*- encoding=utf8 -*-
__author__ = "UNITY_105"

import pytest
from airtest.core.api import *
from airtest.cli.parser import cli_setup

class LogInWithGoogle:



    def verify_facebook_login_button(self):
        assert_exists(
                Template(r"../../test/login_with_google/tpl1738847569050.png", record_pos=(0.026, 0.481), resolution=(1080, 2400)),
                "Verify: 'Facebook' login button displayed.")

    
    def verify_google_login_button(self):
        assert_exists(
            Template(r"tpl1738847577568.png", record_pos=(0.031, 0.654), resolution=(1080, 2400)),
            "Verify: 'Google' login button displayed."
        )

    def verify_sign_in_button(self):
        assert_exists(
            Template(r"tpl1738847595911.png", record_pos=(0.003, 0.989), resolution=(1080, 2400)),
            "Verify: 'Sign In' login button displayed."
        )

    def click_google_login_button(self):
        touch(Template(r"tpl1738847648178.png", record_pos=(0.028, 0.654), resolution=(1080, 2400)))

    def wait_for_google_email(self):
        wait(Template(r"tpl1738847697875.png", record_pos=(-0.11, 0.526), resolution=(1080, 2400)), 
             timeout=60, interval=3)

    def verify_google_email_present(self):
        assert_exists(
            Template(r"tpl1738847697875.png", record_pos=(-0.11, 0.526), resolution=(1080, 2400)),
            "Verify: Google email ID in present on the screen"
        )

    def click_email_id(self):
        touch(Template(r"tpl1738847711778.png", record_pos=(-0.072, 0.524), resolution=(1080, 2400)))
        print("Tapped on login email ID ")

    def wait_for_burger_menu(self):
        wait(Template(r"tpl1738847783748.png", record_pos=(-0.444, -0.956), resolution=(1080, 2400)), 
             timeout=60, interval=3)

    def click_burger_menu(self):
        touch(Template(r"tpl1738847783748.png", record_pos=(-0.444, -0.956), resolution=(1080, 2400)))
        print("Tapped on burger menu ")

    def verify_username_in_slider(self):
        assert_exists(
            Template(r"tpl1738847798223.png", record_pos=(-0.077, -0.892), resolution=(1080, 2400)),
            "Verify: User name in slider"
        )

    def click_settings_button(self):
        touch(Template(r"tpl1738847862492.png", record_pos=(-0.263, 0.924), resolution=(1080, 2400)))
        print("Tapped on setting button")

    def click_logout_button(self):
        touch(Template(r"tpl1738847880490.png", record_pos=(-0.015, 0.305), resolution=(1080, 2400)))
        print("Tapped on logout button")
        sleep(3.0)

    def verify_google_login_after_logout(self):
        wait(Template(r"tpl1738847908114.png", record_pos=(0.008, 0.654), resolution=(1080, 2400)))
        assert_exists(
            Template(r"tpl1738847908114.png", record_pos=(0.008, 0.654), resolution=(1080, 2400)),
            "Verify: Google login button is displayed after logout"
        )




    # generate html report
    # from airtest.report.report import simple_report
    # simple_report(__file__, logpath=True)