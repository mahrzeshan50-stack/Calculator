cat > app.py << 'EOF'
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Calculator</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0a0a0f;
    background-image:
      radial-gradient(ellipse at 20% 50%, rgba(0,255,180,0.05) 0%, transparent 60%),
      radial-gradient(ellipse at 80% 20%, rgba(0,180,255,0.05) 0%, transparent 60%);
    font-family: 'Share Tech Mono', monospace;
  }

  .calc-wrapper { position: relative; }

  .calc-wrapper::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 24px;
    background: linear-gradient(135deg, #00ffb4, #0088ff, #00ffb4);
    background-size: 200% 200%;
    animation: borderGlow 4s linear infinite;
    z-index: 0;
    opacity: 0.7;
  }

  @keyframes borderGlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  .calculator {
    position: relative;
    z-index: 1;
    background: #0f0f1a;
    border-radius: 22px;
    padding: 24px;
    width: 320px;
    box-shadow: 0 0 60px rgba(0,255,180,0.1), inset 0 1px 0 rgba(255,255,255,0.05);
  }

  .display {
    background: #070710;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,255,180,0.15);
    min-height: 90px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-end;
    gap: 4px;
    overflow: hidden;
  }

  .display .expression {
    font-size: 13px;
    color: rgba(0,255,180,0.4);
    font-family: 'Share Tech Mono', monospace;
    min-height: 18px;
    letter-spacing: 1px;
    word-break: break-all;
    text-align: right;
  }

  .display .result {
    font-family: 'Orbitron', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: #00ffb4;
    letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(0,255,180,0.5);
    transition: all 0.1s;
    word-break: break-all;
    text-align: right;
    line-height: 1;
  }

  .display .result.flash { color: #fff; text-shadow: 0 0 30px rgba(255,255,255,0.8); }

  .buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }

  button {
    height: 60px;
    border: none;
    border-radius: 12px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.12s ease;
    position: relative;
    overflow: hidden;
    outline: none;
  }

  button:active { transform: scale(0.94); }

  .btn-num { background: #1a1a2e; color: #e0e0ff; border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 4px 0 rgba(0,0,0,0.4); }
  .btn-num:hover { background: #22223a; border-color: rgba(0,255,180,0.2); color: #fff; }

  .btn-op { background: #0d2233; color: #00d4ff; border: 1px solid rgba(0,212,255,0.15); box-shadow: 0 4px 0 rgba(0,0,0,0.4); font-size: 22px; }
  .btn-op:hover { background: #112840; border-color: rgba(0,212,255,0.4); box-shadow: 0 0 12px rgba(0,212,255,0.2), 0 4px 0 rgba(0,0,0,0.4); color: #00eeff; }

  .btn-eq { background: linear-gradient(135deg, #00c896, #0099cc); color: #000; font-weight: bold; font-size: 22px; border: none; box-shadow: 0 4px 0 #005566, 0 0 20px rgba(0,255,180,0.2); }
  .btn-eq:hover { background: linear-gradient(135deg, #00ffb4, #00aaee); box-shadow: 0 4px 0 #005566, 0 0 30px rgba(0,255,180,0.4); }

  .btn-clear { background: #2a0d1a; color: #ff6b8a; border: 1px solid rgba(255,107,138,0.15); box-shadow: 0 4px 0 rgba(0,0,0,0.4); font-size: 14px; }
  .btn-clear:hover { background: #3a0d22; border-color: rgba(255,107,138,0.4); }

  .btn-del { background: #1a1520; color: #ff9f43; border: 1px solid rgba(255,159,67,0.15); box-shadow: 0 4px 0 rgba(0,0,0,0.4); font-size: 20px; }
  .btn-del:hover { background: #231d2a; border-color: rgba(255,159,67,0.4); }

  .btn-percent { background: #1a1520; color: #a78bfa; border: 1px solid rgba(167,139,250,0.15); box-shadow: 0 4px 0 rgba(0,0,0,0.4); }
  .btn-percent:hover { background: #231d2a; border-color: rgba(167,139,250,0.4); }

  .btn-zero { grid-column: span 2; }
  .label { text-align: center; margin-top: 16px; font-size: 10px; letter-spacing: 3px; color: rgba(0,255,180,0.2); font-family: 'Orbitron', sans-serif; }
</style>
</head>
<body>
<div class="calc-wrapper">
  <div class="calculator">
    <div class="display">
      <div class="expression" id="expression"></div>
      <div class="result" id="result">0</div>
    </div>
    <div class="buttons">
      <button class="btn-clear" onclick="clearAll()">AC</button>
      <button class="btn-del" onclick="deleteLast()">⌫</button>
      <button class="btn-percent" onclick="percent()">%</button>
      <button class="btn-op" onclick="appendOp('/')">÷</button>
      <button class="btn-num" onclick="appendNum('7')">7</button>
      <button class="btn-num" onclick="appendNum('8')">8</button>
      <button class="btn-num" onclick="appendNum('9')">9</button>
      <button class="btn-op" onclick="appendOp('*')">×</button>
      <button class="btn-num" onclick="appendNum('4')">4</button>
      <button class="btn-num" onclick="appendNum('5')">5</button>
      <button class="btn-num" onclick="appendNum('6')">6</button>
      <button class="btn-op" onclick="appendOp('-')">−</button>
      <button class="btn-num" onclick="appendNum('1')">1</button>
      <button class="btn-num" onclick="appendNum('2')">2</button>
      <button class="btn-num" onclick="appendNum('3')">3</button>
      <button class="btn-op" onclick="appendOp('+')">+</button>
      <button class="btn-num btn-zero" onclick="appendNum('0')">0</button>
      <button class="btn-num" onclick="appendDot()">.</button>
      <button class="btn-eq" onclick="calculate()">=</button>
    </div>
    <div class="label">ZESHAN'S CALCULATOR</div>
  </div>
</div>

<script>
  let current = '0', expression = '', justCalculated = false;
  const resultEl = document.getElementById('result');
  const expressionEl = document.getElementById('expression');

  function updateDisplay() {
    resultEl.textContent = current.length > 10 ? parseFloat(current).toPrecision(8) : current;
    expressionEl.textContent = expression;
  }

  function appendNum(n) {
    if (justCalculated) { current = ''; expression = ''; justCalculated = false; }
    if (current === '0' && n !== '.') current = n;
    else current += n;
    updateDisplay();
  }

  function appendDot() {
    if (justCalculated) { current = '0'; expression = ''; justCalculated = false; }
    if (!current.includes('.')) current += '.';
    updateDisplay();
  }

  function appendOp(op) {
    justCalculated = false;
    expression += current + ' ' + op + ' ';
    current = '0';
    updateDisplay();
  }

  function clearAll() { current = '0'; expression = ''; justCalculated = false; updateDisplay(); }

  function deleteLast() {
    if (justCalculated) { clearAll(); return; }
    current = current.length > 1 ? current.slice(0, -1) : '0';
    updateDisplay();
  }

  function percent() { current = String(parseFloat(current) / 100); updateDisplay(); }

  function calculate() {
    try {
      const fullExpr = expression + current;
      expressionEl.textContent = fullExpr + ' =';
      const res = Function('"use strict"; return (' + fullExpr + ')')();
      current = String(parseFloat(res.toFixed(10)));
      expression = '';
      justCalculated = true;
      resultEl.classList.add('flash');
      setTimeout(() => resultEl.classList.remove('flash'), 150);
      updateDisplay();
      expressionEl.textContent = fullExpr + ' =';
    } catch {
      current = 'Error'; expression = '';
      updateDisplay();
      setTimeout(clearAll, 1200);
    }
  }

  document.addEventListener('keydown', e => {
    if (e.key >= '0' && e.key <= '9') appendNum(e.key);
    else if (e.key === '.') appendDot();
    else if (e.key === '+') appendOp('+');
    else if (e.key === '-') appendOp('-');
    else if (e.key === '*') appendOp('*');
    else if (e.key === '/') { e.preventDefault(); appendOp('/'); }
    else if (e.key === 'Enter' || e.key === '=') calculate();
    else if (e.key === 'Backspace') deleteLast();
    else if (e.key === 'Escape') clearAll();
    else if (e.key === '%') percent();
  });
</script>
</body>
</html>
"""

@app.route('/')
def calculator():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF
