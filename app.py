from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def receive_location():
    location_data = request.json
    print("\n=== 用户位置信息 ===")
    print(f"纬度: {location_data.get('latitude')}")
    print(f"经度: {location_data.get('longitude')}")
    print(f"精确度: {location_data.get('accuracy')} 米")
    print(f"海拔: {location_data.get('altitude', '不可用')}")
    print(f"方向: {location_data.get('heading', '不可用')}")
    print(f"速度: {location_data.get('speed', '不可用')}")
    print("==================\n")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)