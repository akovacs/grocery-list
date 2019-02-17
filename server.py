from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
    <html>
<body>
<h1>Camera Test</h1>
<input type="file" accept="image/*;capture=camera">
</body>
</html>
"""
