from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
...
"""

@app.route('/')
def calculator():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
