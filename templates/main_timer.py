import time
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

timer_running = False
timer_time = 25 * 60  # 25 minutes in seconds
start_time = 0
elapsed_time = 0

# Timer Worker
def run_timer():
    global timer_time, elapsed_time, timer_running, start_time
    while timer_running:
        if timer_running:
            # Increment elapsed time
            elapsed_time = time.time() - start_time
            time.sleep(1)

@app.route('/timer.html')
def timer():
    return render_template('timer.html', time_left=timer_time - int(elapsed_time))

@app.route('/start', methods=['POST'])
def start_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        timer_running = True
        start_time = time.time() - elapsed_time  # Start from the elapsed time
        threading.Thread(target=run_timer, daemon=True).start()
    return jsonify({'status': 'started'})

@app.route('/stop', methods=['POST'])
def stop_timer():
    global timer_running
    timer_running = False
    return jsonify({'status': 'stopped'})

@app.route('/reset', methods=['POST'])
def reset_timer():
    global timer_running, elapsed_time, timer_time
    timer_running = False
    elapsed_time = 0
    timer_time = 25 * 60  # Reset to original 25 minutes
    return jsonify({'status': 'reset', 'time_left': timer_time})

@app.route('/short_break', methods=['POST'])
def short_break():
    global timer_running, elapsed_time, timer_time
    timer_running = False
    elapsed_time = 0
    timer_time = 5 * 60  # 5 minutes in seconds
    return jsonify({'status': 'short_break', 'time_left': timer_time})

@app.route('/long_break', methods=['POST'])
def long_break():
    global timer_running, elapsed_time, timer_time
    timer_running = False
    elapsed_time = 0
    timer_time = 15 * 60  # 15 minutes in seconds
    return jsonify({'status': 'long_break', 'time_left': timer_time})

if __name__ == '__main__':
    app.run(debug=True)
