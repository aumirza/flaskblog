from flask import render_template, request , url_for, redirect ,send_from_directory,send_file
from flask_login import current_user
from flask import jsonify
from Myblog.gallery.models import Image
from Myblog.gallery.utils import draw_placeholder_image
from Myblog.gallery import gallery

@gallery.before_request
def restrict_dashboard_to_admins():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

@gallery.route('/media', methods=['GET', 'POST'])
def show_gallery():
    images = Image.all('Myblog/uploads')
    return render_template('gallery/index.html', images=images)

@gallery.route('/media/<filename>')
def uploads(filename):
    try:
        return send_from_directory('./uploads', filename=filename)
    except FileNotFoundError:
        abort(404)

@gallery.route('/media/<string:size>/')
def placeholder_image(size):
    text = request.args.get('text')
    bgcolor='#808080'
    color='#ffffff'
    return  draw_placeholder_image(size,bgcolor,color,text)

@gallery.route('/media/<string:size>/<bgcolor>/<color>')
def placeholder_image_with_color(size,bgcolor,color):
    text = request.args.get('text')
    return  draw_placeholder_image(size,bgcolor,color,text)
    


@gallery.route('/media/upload', methods=['POST'])
def upload():
    app.logger.info(f'uploading')
    if request.method == 'POST' and 'image' in request.files:
        image = Image('', post=request.files['image'], root=app.config['GALLERY_ROOT_DIR'])

        if image.path.suffix in app.config['UPLOAD_ALLOWED_EXTENSIONS']:
            return ("ok", 201,)

        app.logger.info(f'failed to upload {image!r}')

    return (jsonify({'error': 'you need to pass an image'}), 400)

