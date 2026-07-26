import os
from flask import Blueprint, send_from_directory, current_app

views = Blueprint('download_kk', __name__)

@views.route('/download/kk/<path:filename>')
def download_kk(filename):
    # Menggunakan current_app.root_path agar path dinamis dan aman
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    
    return send_from_directory(
        upload_folder,
        filename,
        as_attachment=True
    )