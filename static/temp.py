'''import time
import threading
from flask import Flask, render_template, jsonify
from subprocess import call
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
def open_py_file():
    call(["python", "list.py"])
open_py_file()

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
    global timer_running, elapsed_time
    timer_running = False
    elapsed_time = 0
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


@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/login.html')
def login():
    return render_template("login.html")

@app.route('/timer.html')
def timer():
    return render_template('timer.html')


@app.route("/")
def __init__():
    from list import delete
    from list import update
    from list import create
    from list import homepage
    from todo import fetch_todo
    from todo import update_task_entry
    from todo import update_status_entry
    from todo import insert_new_task
    from todo import remove_task_by_id



def main():
    print(delete())
    print(update())
    print(create())
    print(homepage())
    print(fetch_todo())
    print(update_task_entry())
    print(update_status_entry())
    print(insert_new_task())
    print(remove_task_by_id())



if __name__ == '__main__':
    app.run(debug=True)'''



from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="timezap"
)

cursor = db.cursor()

# Create table if not exists
'''cursor.execute("""
CREATE TABLE IF NOT EXISTS list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255),
    status VARCHAR(255)
)
""")'''

@app.route('/')
def index():
    cursor.execute("SELECT * FROM task")
    tasks = cursor.fetchall()
    return render_template('login.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task= request.form.get('task')
    cursor.execute("INSERT INTO list (task, status) VALUES (%s, %s)", (task, 'Pending'))
    db.commit()
    return redirect('/')
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    status = request.form.get('status')
    cursor.execute("UPDATE list SET status = %s WHERE id = %s", (status, id))
    db.commit()

    return redirect('/')

@app.route('/remove/<int:id>')
def remove(id):
    cursor.execute("DELETE FROM list WHERE id = %s", (id,))
    db.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
