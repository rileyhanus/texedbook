from app import App

@App.route("/")
@App.route("/index")
def inde():
    return "hello world"
