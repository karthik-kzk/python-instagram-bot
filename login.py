from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger()

INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')


def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    
    login_via_session = False
    login_via_pw = False
    
    
    if os.path.exists("session.json"):
        session = cl.load_settings("session.json")
        if session:
            try:
                cl.set_settings(session)
                cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

                # check if session is valid
                try:
                    cl.get_timeline_feed()
                except LoginRequired:
                    logger.info(
                        "Session is invalid, need to login via username and password")

                    old_session = cl.get_settings()

                    # use the same device uuids across logins
                    cl.set_settings({})
                    cl.set_uuids(old_session["uuids"])

                    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                login_via_session = True
                print("login_via_session ")
            except Exception as e:
                logger.info(
                    "Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s" % INSTAGRAM_USERNAME)
            if cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD):              
                cl.dump_settings("session.json")
                print("userName")
                login_via_pw = True
        except Exception as e:
            logger.info(
                "Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    return cl
