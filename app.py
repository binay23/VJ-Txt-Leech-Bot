from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Tech VJ'

# Run the app on all available interfaces (0.0.0.0) to allow external access
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
