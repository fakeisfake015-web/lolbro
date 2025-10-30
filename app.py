from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Network Ping Tool - Challenge 20</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #4CAF50;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .hint {
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Network Ping Tool</h1>
        <p>Enter an IP address or hostname to ping:</p>
        <form method="POST">
            <input type="text" name="host" placeholder="e.g., 8.8.8.8 or google.com" required>
            <button type="submit">Ping</button>
        </form>
        <p class="hint">💡 Hint: This tool uses the system's ping command. Think about how commands are executed...</p>
        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        host = request.form.get('host', '')
        
        # Vulnerable to command injection
        # Using shell=True with user input
        if os.name == 'nt':  # Windows
            cmd = f'ping -n 4 {host}'
        else:  # Linux
            cmd = f'ping -c 4 {host}'
        
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5)
            result = output.decode('utf-8', errors='ignore')
        except subprocess.TimeoutExpired:
            result = "Error: Command timed out"
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
