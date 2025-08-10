from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Store user states and data in memory
user_state = {}
user_bus = {}
user_stop = {}

# Demo bus data
bus_stops = {
    "7": ["Stop A", "Stop B", "Stop C", "Stop D"],
    "12": ["Stop X", "Stop Y", "Stop Z"],
    "5": ["Stop M", "Stop N", "Stop O"]
}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    sender = request.form.get('From')
    msg = request.form.get('Body').strip().lower()

    resp = MessagingResponse()
    reply = ""

    if sender not in user_state:
        # First message from user
        user_state[sender] = "ask_bus"
        reply = "👋 Hi! Welcome to InstiTrack.\nPlease enter your Bus Number to register."
    
    elif user_state[sender] == "ask_bus":
        # Save bus number
        bus_num = msg
        if bus_num in bus_stops:
            user_bus[sender] = bus_num
            user_state[sender] = "ask_stop"
            stops_list = "\n".join([f"{i+1}. {stop}" for i, stop in enumerate(bus_stops[bus_num])])
            reply = f"✅ Bus {bus_num} registered.\nNow choose your stop by sending the number:\n{stops_list}"
        else:
            reply = "❌ Invalid bus number. Please try again."
    
    elif user_state[sender] == "ask_stop":
        bus_num = user_bus[sender]
        stops = bus_stops[bus_num]
        try:
            stop_choice = int(msg)
            if 1 <= stop_choice <= len(stops):
                chosen_stop = stops[stop_choice - 1]
                user_stop[sender] = chosen_stop
                user_state[sender] = "registered"
                reply = f"✅ You are registered for Bus {bus_num}, Stop: {chosen_stop}.\nYou will get alerts when your bus is near."
            else:
                reply = "❌ Invalid stop number. Please try again."
        except ValueError:
            reply = "❌ Please enter a valid stop number."
    
    elif user_state[sender] == "registered":
        reply = "✅ You are already registered.\nWe’ll notify you when your bus is approaching your stop."

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
