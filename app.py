from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'hi' in incoming_msg:
        msg.body("Hello! 👋 Please enter your bus number.")
    elif incoming_msg.isdigit():
        msg.body(f"Thanks! Bus number {incoming_msg} registered. 🚍")
    else:
        msg.body("Sorry, I didn't understand that. Please send your bus number.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
