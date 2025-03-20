from flask import Flask, render_template, request, jsonify, make_response
import logging
import socket

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;")
    return response

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;"
    return response

@app.route('/location', methods=['POST', 'OPTIONS'])
def receive_location():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        location_data = request.json
        logger.info("收到位置信息请求")
        print("\n=== 用户位置信息 ===")
        print(f"纬度: {location_data.get('latitude')}")
        print(f"经度: {location_data.get('longitude')}")
        print(f"精确度: {location_data.get('accuracy')} 米")
        print(f"海拔: {location_data.get('altitude', '不可用')}")
        print(f"方向: {location_data.get('heading', '不可用')}")
        print(f"速度: {location_data.get('speed', '不可用')}")
        print("==================\n")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"处理位置信息时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        ip_address = get_local_ip()
        logger.info(f"服务器启动在 http://{ip_address}:80")
        app.run(host='0.0.0.0', port=80, debug=True)
    except Exception as e:
        logger.error(f"启动服务器时出错: {str(e)}")
        exit(1)