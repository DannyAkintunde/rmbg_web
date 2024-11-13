# Backend api

# rmbg_api

Welcome to the *rmbg_api* project! This API is built using Flask and leverages the `rembg` Python package to remove backgrounds from images. 

 Overview

The rmbg_api allows users to remove backgrounds from images either by uploading a file or by providing a URL to an image. Users can also select from various models for background removal and specify a background color.

 Features

- Remove backgrounds from images using multiple models.
- Support for file uploads and URL-based image processing.
- Customizable background color for removed backgrounds.
- Simple API with easy-to-use endpoints.

 Requirements

- Python 3.6 or higher
- Flask
- rembg
- werkzeug
- requests

 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DannyAkintunde/rmbg_web.git
   cd rmbg_web/backend # for api
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - `U2NET_HOME`: Path to the models directory (default is `./models`).
   - `DEFAULT_MODEL`: The model to use by default (default is `u2netp`).
   - `APIKEY`: Your API key for authentication (optional).
   - `HOST`: Host address for the Flask app (default is `127.0.0.1`).
   - `PORT`: Port for the Flask app (default is `8000`).
   - `DEBUG`: Set to `true` to enable debug mode (default is `false`).

 Usage

To start the server, run:

```bash
python app.py
```

 Endpoints

 Home

- *GET /*: Displays a welcome message and links to the project GitHub.

 Remove Background

- *POST /api/rmbg*
  
  Request Body (form-data):
  - `file`: The image file to process.
  - `model`: (optional) The model to use for background removal.
  - `bg_color`: (optional) The background color in hex format (e.g., `#FFFFFF`).

- *GET /api/rmbg*
  
  Query Parameters:
  - `url`: The URL of the image to process.
  - `model`: (optional) The model to use for background removal.
  - `bg_color`: (optional) The background color in hex format.

 Example

Here’s how to use the API to remove a background from an image:

*POST Request*:
```bash
curl -X POST -F "file=@path/to/image.jpg" -F "model=u2netp" -F "bg_color=#FFFFFF" http://localhost:8000/api/rmbg
```

*GET Request*:
```bash
curl "http://localhost:8000/api/rmbg?url=https://example.com/image.jpg&model=u2netp&bg_color=#FFFFFF"
```

 Models

The following models are available for background removal:
- birefnet-cod
- birefnet-dis
- birefnet-general
- birefnet-general-lite
- birefnet-hrsod
- birefnet-massive
- birefnet-portrait
- isnet-anime
- isnet-general-use
- silueta
- u2net
- u2net_cloth_seg
- u2net_human_seg
- u2netp

 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

 Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

 Acknowledgments

- This project uses the [rembg](https://github.com/danielgindi/rembg) library for image background removal.
- Special thanks to the contributors of the Flask framework and the Python community.

For more information, please refer to our [GitHub page](https://github.com/DannyAkintunde/rmbg_web).
