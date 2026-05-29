from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Calculator</title>
</head>
<body>
<h1>ZESHAN'S CALCULATOR</h1>
<input type="text" id="display" value="0" readonly style="font-size:24px;width:200px;text-align:right"><br><br>
<button onclick="appendNum('7')">7</button>
<button onclick="appendNum('8')">8</button>
<button onclick="appendNum('9')">9</button>
<button onclick="appendOp('+')">+</button><br>
<button onclick="appendNum('4')">4</button>
<button onclick="appendNum('5')">5</button>
<button onclick="appendNum('6')">6</button>
<button onclick="appendOp('-')">-</button><br>
<button onclick="appendNum('1')">1</button>
<button onclick="appendNum('2')">2</button>
<button onclick="appendNum('3')">3</button>
<button onclick="appendOp('*')">*</button><br>
<button onclick="appendNum('0')">0</button>
<button onclick="calculate()">=</button>
<button onclick="clearAll()">AC</button>
<button onclick="appendOp('/')">/</button>

<script>
let expr = '';
function appendNum(n) { 
  expr += n; 
  document.getElementById('display').value = expr; 
}
function appendOp(op) { 
  expr += op; 
  document.getElementById('display').value = expr; 
}
function calculate() { 
  document.getElementById('display').value = eval(expr); 
  expr = document.getElementById('display').value; 
}
function clearAll() { 
  expr = ''; 
  document.getElementById('display').value = '0'; 
}
</script>
</body>
</html>
"""

@app.route('/')
def calculator():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
