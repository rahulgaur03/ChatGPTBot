import time
import os 
import flask
import sys
from flask import g
from playwright.sync_api import sync_playwright

PROFILE_DIR = "/tmp/playwright" if '--profile' not in sys.argv else sys.argv[sys.argv.index('--profile') + 1]
PORT = 5001 if '--port' not in sys.argv else int(sys.argv[sys.argv.index('--port') + 1])
APP = flask.Flask(__name__)

browser = None
page = None
 
def start_browser():
    global browser, page
    if browser is None:
        PLAY = sync_playwright().start()
        browser = PLAY.firefox.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
        )
        page = browser.new_page()
    page.goto("https://chat.openai.com/")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
    else:
        print("Logged in")

def is_logged_in():
    try:
        return get_input_box() is not None
    except:
        return False

def get_input_box():
    """Find the input box by searching for the largest visible one."""
    try:
        textareas = page.query_selector_all("textarea")
        candidate = None
        for textarea in textareas:
            if textarea.is_visible():
                if candidate is None:
                    candidate = textarea
                elif textarea.bounding_box().width > candidate.bounding_box().width:
                    candidate = textarea
        return candidate
    except:
        return None

def send_message(message):
    try:
        # Send the message
        box = get_input_box()
        box.click()
        box.fill(message)
        box.press("Enter")
        page.wait_for_selector(".result-streaming",state='hidden')
    except:
        pass

def get_last_message():
    """Get the latest message"""
    try:
        page_elements = page.query_selector_all(".flex.flex-col.items-center > div")
        last_element = page_elements[-2]
        return last_element.inner_text()
    except:
        return None

@APP.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    send_message(message)
    response = get_last_message()
    print("Response: ", response)
    return response

if __name__ == "__main__":
    start_browser()
    APP.run(port=PORT, threaded=False)
