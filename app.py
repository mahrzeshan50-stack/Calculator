from flask import Flask, render_template_string
import math

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Scientific Calculator</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono&family=Orbitron:wght@400;700&display=swap');

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Space Mono', monospace;
  }

  .container {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    width: 90%;
    max-width: 500px;
  }

  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
    font-size: 28px;
  }

  .display {
    background: #f0f0f0;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    text-align: right;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }

  .expression {
    color: #666;
    font-size: 14px;
    margin-bottom: 5px;
    word-break: break-all;
  }

  .result {
    color: #667eea;
    font-size: 36px;
    font-weight: bold;
    word-break: break-all;
  }

  .buttons-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 15px;
  }

  .scientific-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 15px;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 10px;
  }

  button {
    padding: 15px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    font-family: 'Space Mono', monospace;
  }

  .btn-number {
    background: #e0e0e0;
    color: #333;
  }

  .btn-number:hover {
    background: #d0d0d0;
    transform: scale(1.05);
  }

  .btn-operator {
    background: #667eea;
    color: white;
  }

  .btn-operator:hover {
    background: #764ba2;
    transform: scale(1.05);
  }

  .btn-equals {
    background: #4caf50;
    color: white;
    grid-column: span 2;
  }

  .btn-equals:hover {
    background: #45a049;
    transform: scale(1.05);
  }

  .btn-clear {
    background: #f44336;
    color: white;
    grid-column: span 2;
  }

  .btn-clear:hover {
    background: #da190b;
    transform: scale(1.05);
  }

  .btn-delete {
    background: #ff9800;
    color: white;
  }

  .btn-delete:hover {
    background: #e68900;
    transform: scale(1.05);
  }

  .btn-scientific {
    background: #9c27b0;
    color: white;
    font-size: 14px;
  }

  .btn-scientific:hover {
    background: #7b1fa2;
    transform: scale(1.05);
  }

  .info {
    text-align: center;
    color: #666;
    font-size: 12px;
    margin-top: 15px;
  }
</style>
</head>
<body>

<div class="container">
  <h1>🧮 Scientific Calculator</h1>
  
  <div class="display">
    <div class="expression" id="expression"></div>
    <div class="result" id="result">0</div>
  </div>

  <div class="buttons-grid">
    <button class="btn-clear" onclick="clearDisplay()">AC</button>
    <button class="btn-delete" onclick="deleteLast()">DEL</button>
    <button class="btn-operator" onclick="appendOperator('/')" style="grid-column: span 2;">÷</button>
  </div>

  <div class="scientific-grid">
    <button class="btn-scientific" onclick="scientificFunction('sin')">sin</button>
    <button class="btn-scientific" onclick="scientificFunction('cos')">cos</button>
    <button class="btn-scientific" onclick="scientificFunction('tan')">tan</button>
    <button class="btn-scientific" onclick="scientificFunction('sqrt')">√</button>
    
    <button class="btn-scientific" onclick="scientificFunction('log')">log</button>
    <button class="btn-scientific" onclick="scientificFunction('ln')">ln</button>
    <button class="btn-scientific" onclick="appendValue('Math.PI')">π</button>
    <button class="btn-scientific" onclick="appendValue('Math.E')">e</button>
    
    <button class="btn-scientific" onclick="scientificFunction('fact')">n!</button>
    <button class="btn-scientific" onclick="scientificFunction('pow')">x^y</button>
    <button class="btn-scientific" onclick="toggleSign()">+/-</button>
    <button class="btn-scientific" onclick="scientificFunction('percent')">%</button>
  </div>

  <div class="buttons-grid">
    <button class="btn-number" onclick="appendNumber('7')">7</button>
    <button class="btn-number" onclick="appendNumber('8')">8</button>
    <button class="btn-number" onclick="appendNumber('9')">9</button>
    <button class="btn-operator" onclick="appendOperator('*')">×</button>

    <button class="btn-number" onclick="appendNumber('4')">4</button>
    <button class="btn-number" onclick="appendNumber('5')">5</button>
    <button class="btn-number" onclick="appendNumber('6')">6</button>
    <button class="btn-operator" onclick="appendOperator('-')">−</button>

    <button class="btn-number" onclick="appendNumber('1')">1</button>
    <button class="btn-number" onclick="appendNumber('2')">2</button>
    <button class="btn-number" onclick="appendNumber('3')">3</button>
    <button class="btn-operator" onclick="appendOperator('+')">+</button>

    <button class="btn-number" onclick="appendNumber('0')" style="grid-column: span 2;">0</button>
    <button class="btn-number" onclick="appendNumber('.')">.</button>
    <button class="btn-equals" onclick="calculate()">=</button>
  </div>

  <div class="info">
    Made with ❤️ by Zeshan | DevOps Engineer in Training
  </div>
</div>

<script>
  let display = '0';
  let expression = '';
  let lastWasOperator = false;

  function updateDisplay() {
    document.getElementById('result').textContent = display.length > 15 ? display.substring(0, 15) + '...' : display;
    document.getElementById('expression').textContent = expression;
  }

  function appendNumber(num) {
    if (display === '0' && num !== '.') {
      display = num;
    } else if (num === '.' && display.includes('.')) {
      return;
    } else {
      display += num;
    }
    lastWasOperator = false;
    updateDisplay();
  }

  function appendValue(val) {
    display = val;
    lastWasOperator = false;
    updateDisplay();
  }

  function appendOperator(op) {
    if (!lastWasOperator) {
      expression += display + ' ' + op + ' ';
      display = '0';
      lastWasOperator = true;
    }
    updateDisplay();
  }

  function clearDisplay() {
    display = '0';
    expression = '';
    lastWasOperator = false;
    updateDisplay();
  }

  function deleteLast() {
    display = display.length > 1 ? display.slice(0, -1) : '0';
    updateDisplay();
  }

  function toggleSign() {
    display = String(parseFloat(display) * -1);
    updateDisplay();
  }

  function scientificFunction(func) {
    let result;
    let num = parseFloat(display);

    switch(func) {
      case 'sin': result = Math.sin(num * Math.PI / 180); break;
      case 'cos': result = Math.cos(num * Math.PI / 180); break;
      case 'tan': result = Math.tan(num * Math.PI / 180); break;
      case 'sqrt': result = Math.sqrt(num); break;
      case 'log': result = Math.log10(num); break;
      case 'ln': result = Math.log(num); break;
      case 'fact': result = factorial(Math.floor(num)); break;
      case 'pow': expression += display + '^'; display = '0'; lastWasOperator = true; updateDisplay(); return;
      case 'percent': result = num / 100; break;
    }

    display = String(result.toFixed(10)).replace(/\.?0+$/, '');
    lastWasOperator = false;
    updateDisplay();
  }

  function factorial(n) {
    if (n < 0) return NaN;
    if (n === 0 || n === 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) result *= i;
    return result;
  }

  function calculate() {
    try {
      let fullExpression = expression + display;
      fullExpression = fullExpression.replace(/\^/g, '**');
      fullExpression = fullExpression.replace(/Math.PI/g, Math.PI.toString());
      fullExpression = fullExpression.replace(/Math.E/g, Math.E.toString());
      
      let result = Function('"use strict"; return (' + fullExpression + ')')();
      display = String(parseFloat(result.toFixed(10)));
      expression = '';
      lastWasOperator = false;
      updateDisplay();
    } catch (e) {
      display = 'Error';
      updateDisplay();
      setTimeout(clearDisplay, 1500);
    }
  }

  document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9') appendNumber(e.key);
    else if (e.key === '.') appendNumber('.');
    else if (e.key === '+') appendOperator('+');
    else if (e.key === '-') appendOperator('-');
    else if (e.key === '*') appendOperator('*');
    else if (e.key === '/') { e.preventDefault(); appendOperator('/'); }
    else if (e.key === 'Enter' || e.key === '=') calculate();
    else if (e.key === 'Backspace') deleteLast();
    else if (e.key === 'Escape') clearDisplay();
  });

  updateDisplay();
</script>

</body>
</html>
"""

@app.route('/')
def calculator():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
