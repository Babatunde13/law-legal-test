from flask import current_app as app

@app.route('/')
def get_products():
    return {
        "message": "Successfully retrieved data",
        "data": {},
        "status": "ok"
    }