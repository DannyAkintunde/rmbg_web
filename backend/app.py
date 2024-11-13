from os import getenv
from flask import Flask, render_template_string, jsonify, request, Response
from pathlib import Path
from werkzeug.utils import secure_filename
from re import findall
from rembg import remove, new_session
from requests import get
from urllib.parse import urlparse

app = Flask(__name__)

models_path = Path(getenv('U2NET_HOME', './models '))
models_path.mkdir(parents=True, exist_ok=True)
models = ["birefnet-cod", "birefnet-dis", "birefnet-general", "birefnet-general-lite", "birefnet-hrsod", "birefnet-massive", "birefnet-portrait", "isnet-anime", "isnet-general-use", "sam", "silueta", "u2net", "u2net_cloth_seg", "u2net_human_seg", "u2netp"]
# models = [file.name for file in models_path.iterdir() if file.is_file() and file.suffix == '.onnx']

session = new_session(getenv('DEFAULT_MODEL', 'u2netp'))

def hex_to_rgba(hex_code):
    hex_code = hex_code.lstrip('#')
    
    if len(hex_code) not in (6, 8):
        return
        # raise ValueError("Invalid hex code, hex code must be 6 to 9 characters long.")
    
    # Extract the red, green, and blue components
    r = int(hex_code[0:2], 16)  # Convert the first two characters to decimal
    g = int(hex_code[2:4], 16)  # Convert the next two characters to decimal
    b = int(hex_code[4:6], 16)  # Convert the last two characters to decimal
    
    if len(hex_code) == 8:
        a = int(hex_code[6:8], 16)
        return (r, g, b, a)
    
    return (r, g, b, 255)



@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to rmbg_api</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #333;
            }
            p {
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to my rmbg_api Application!</h1>
        <p>This api is based on the rembg python package</p>
        <p>Please head to our project GitHub for documentation:</p>
        <a href="https://github.com/DannyAkintunde/rmbg_web" target="_blank">Project GitHub</a><br/>
        <small>clone this space to use the api</small>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/api/rmbg', methods=['GET', 'POST'])
def remove_bg():
      global session
      try:
          apikey = getenv('APIKEY')
          if apikey and apikey != request.headers.get('X-API-KEY'):
              return jsonify({'error': 'Invalid apikey'}), 401
          if request.method == 'POST':
              file = request.files.get('file')
              model = request.form.get('model')
              bg_color = request.form.get('bg_color')
              
              if not file:
                  return jsonify({'error': 'no file in request'}), 400
              if model:
                  if model not in models:
                      return jsonify({'error': f'invalid model name avaliable models are {models}'}), 400
                  session = new_session(model)
              
              filename = secure_filename(file.filename)
              mime_type = file.content_type
              
              data = file.stream.read()
          elif request.method == 'GET':
              url = request.args.get('url')
              model = request.args.get('model')
              bg_color = request.args.get('bg_color')
              
              if not url:
                  return jsonify({'error': 'Url is required'}), 400
              
              parsed_url = urlparse(url)
              if not parsed_url.scheme or not parsed_url.netloc:
                  return jsonify({'error': 'Invalid url passed'}), 400
              
              if model:
                  if model not in models:
                      return jsonify({'error': f'invalid model name avaliable models are {models}'}), 400
                  session = new_session(model)
              
              input_image_response = get(url)
              input_image_response.raise_for_status()
              if input_image_response.status_code == 200:
                  data = input_image_response.content
                  content_disposition = input_image_response.headers.get('Content-Disposition', '')
                  filename_search = findall("filename=(.+)", content_disposition)
                  filename = filename_search[0].strip('"').strip("'") if filename_search else url.split("/")[-1]
                  mime_type = input_image_response.headers.get('Content-Type', 'application/octet-stream')
                  
          bg_color = hex_to_rgba(bg_color) if bg_color else None
          result = remove(data, bgcolor=bg_color, session=session, alpha_matting=True, alpha_matting_foreground_threshold=270, alpha_matting_background_threshold=20, alpha_matting_erode_size=11, post_process_mask=True)
          return Response(response=result, mimetype=mime_type, headers={
                'Content-Disposition': f'inline; filename=removedbg_{filename}'
            })
      except Exception as e:
          print(e)
          return jsonify({'error': f'Server error {str(e)}'}), 500
  
if __name__ == '__main__':
    app.run(host=getenv('HOST', '127.0.0.1'),
            port=getenv('PORT', 8000), debug=(getenv('DEBUG', '').lower() == 'true'))
