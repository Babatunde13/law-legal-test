from app import create_app
from config import Config

app = application = create_app(Config)

@application.route('/api/v1/')
def home():
    return ''

if __name__ == "__main__":
    application.run()