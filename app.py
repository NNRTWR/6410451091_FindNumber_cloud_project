import random
from flask import Flask,render_template,request
from flask_socketio import SocketIO,emit

app=Flask(__name__)
app.config['SECRET_KEY']='secret_key'
socketio = SocketIO(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


rand = random.randint(1, 100)  # random int number 1-100
print(rand)

@socketio.on('connect')
def on_connect():
    print('Client connected')

game_data = {
    "rand": rand,  # ตัวเลขสุ่ม
    "count": 0,  # จำนวนการทาย
    "status": 0,  # สถานะเกม 0=กำลังเล่น, 1=เกมจบ
}
print(game_data['rand'])

@app.route('/')
def test():
    return render_template('findNum.html')

@socketio.on('hint')
def hint(data):
    print(data)
    
    global game_data

    try:
        num = int(data)
    except ValueError:
        # แจ้งเตือนผู้เล่นว่าฟาวล์
        socketio.emit('hints', f"{data} : Foul. Please enter NUMBER only.")
        game_data["count"] += 1
        return
    
    # เพิ่มจำนวนการทาย
    game_data["count"] += 1
    
    # ตรวจสอบว่าผู้เล่นทายถูกหรือไม่
    
    if num == game_data["rand"]:
        # ผู้เล่นทายถูก
        game_data["status"] = 1
        socketio.emit('hints', f" You guessed right. Guessed {game_data['count']} times.")
    else:
        # ผู้เล่นทายผิด
        if num < game_data["rand"]:
            hint = "Too little"
        else:
            hint = "Too much"
        
        message = [f"{num}: {hint}", f"\nGuessed: {game_data['count']} times  >>  Try more  >>  "]

        socketio.emit('hints', message)
        

if __name__==("__main__"):
    socketio.run(app, debug=True)