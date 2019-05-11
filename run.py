from app import app
from config import DEBUG, APP_PORT

if __name__ == '__main__':
    app.run(debug=DEBUG, port=APP_PORT, host="0.0.0.0")
