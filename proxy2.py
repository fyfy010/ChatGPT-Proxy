import json
import os
import tls_client
import uvicorn

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, jsonify, request
from OpenAIAuth.Cloudflare import Cloudflare

GPT_PROXY = os.getenv('GPT_PROXY')
GPT_HOST = os.getenv('GPT_HOST', '0.0.0.0')
GPT_PORT = int(os.getenv('GPT_PORT', 5000))
CHAT_OPENAI_URL = 'https://chat.openai.com'

app = Flask(__name__)

session = tls_client.Session(client_identifier="chrome_108")
if GPT_PROXY:
    session.proxies.update(http=GPT_PROXY, https=GPT_PROXY)

# Get cloudflare cookies
cf_cookies = Cloudflare(proxy=GPT_PROXY).get_cf_cookies()
cf_clearance_cookie = cf_cookies.get('cf_clearance')
user_agent = cf_cookies.get('user_agent')

@app.route("/cookies", methods=["GET"])
def get_cookies():
    return jsonify({'cf_clearance': cf_clearance_cookie, 'user_agent': user_agent})

@app.route("/<path:subpath>", methods=["POST", "GET"])
def conversation(subpath: str):
    try:
        # Validate authorization header
        if 'Authorization' not in request.headers:
            return jsonify({"error": "Missing Authorization header"}), 401

        # Get cookies from request
        cookies = {
            "cf_clearance": cf_clearance_cookie,
            "__Secure-next-auth.session-token": request.cookies.get("__Secure-next-auth.session-token")
        }

        # Set headers
        headers = {
            "Accept": "text/event-stream",
            "Authorization": request.headers.get("Authorization"),
            "User-Agent": user_agent,
            "Content-Type": "application/json",
            "X-Openai-Assistant-App-Id": "",
            "Connection": "close",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"{CHAT_OPENAI_URL}/chat"
        }

        # Send request to chat.openai.com
        if request.method == "POST":
            response = session.post(
                url=f"{CHAT_OPENAI_URL}/{subpath}",
                headers=headers,
                cookies=cookies,
                data=json.dumps(request.get_json()),
                timeout_seconds=360,
            )
        elif request.method == "GET":
            response = session.get(
                url=f"{CHAT_OPENAI_URL}/{subpath}",
                headers=headers,
                cookies=cookies,
                timeout_seconds=360,
            )

        # Check status code
        if response.status_code == 403:
            # Get new cf_clearance cookie
            cf_cookies = Cloudflare(proxy=GPT_PROXY).get_cf_cookies()
            cf_clearance_cookie = cf_cookies.get('cf_clearance')
            user_agent = cf_cookies.get('user_agent')
            # return error
            return jsonify({
                "error":
                "Cloudflare token expired. Please wait a few minutes while I refresh"
            }), 403

