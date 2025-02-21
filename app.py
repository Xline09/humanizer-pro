from flask import Flask, request, render_template, send_file, session, jsonify
from humanizer import AdvancedHumanizer
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'supersecretkey123'
humanizer = AdvancedHumanizer()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'undo_stack' not in session:
        session['undo_stack'] = []
    if 'redo_stack' not in session:
        session['redo_stack'] = []

    original_text = session.get('original_text', '')
    humanized_text = session.get('humanized_text', '')
    changes = session.get('changes', [])
    selected_tone = request.form.get('tone', 'auto') if request.method == 'POST' else 'auto'

    if request.method == 'POST':
        action = request.form.get('action')
        original_text = request.form.get('text', '')

        if action == 'humanize' and original_text.strip():
            session['undo_stack'].append({'input': original_text, 'output': humanized_text, 'changes': changes})
            session['redo_stack'] = []
            try:
                humanized_text, changes = humanizer.humanize(original_text)
                if selected_tone != 'auto':
                    humanized_text, tone_changes = humanizer.adjust_tone(humanized_text, selected_tone)
                    changes.extend(tone_changes)
            except Exception as e:
                humanized_text = f"Failed to humanize: {str(e)}. Original: {original_text}"
                changes = []

        elif action == 'clear':
            session['undo_stack'] = []
            session['redo_stack'] = []
            original_text = ''
            humanized_text = ''
            changes = []

        elif action == 'undo' and session['undo_stack']:
            last_state = session['undo_stack'].pop()
            session['redo_stack'].append({'input': original_text, 'output': humanized_text, 'changes': changes})
            original_text = last_state['input']
            humanized_text = last_state['output']
            changes = last_state['changes']

        elif action == 'redo' and session['redo_stack']:
            next_state = session['redo_stack'].pop()
            session['undo_stack'].append({'input': original_text, 'output': humanized_text, 'changes': changes})
            original_text = next_state['input']
            humanized_text = next_state['output']
            changes = next_state['changes']

        elif action == 'save':
            if humanized_text.strip():
                file = BytesIO(humanized_text.encode('utf-8'))
                return send_file(file, as_attachment=True, download_name='humanized_text.txt', mimetype='text/plain')

        elif action == 'upload' and 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                if filename.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original_text = f.read()
                elif filename.endswith('.docx'):
                    doc = Document(file_path)
                    original_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                else:
                    original_text = "Unsupported file format. Please upload .txt or .docx."
                    humanized_text = ""
                if original_text and original_text != "Unsupported file format. Please upload .txt or .docx.":
                    humanized_text, changes = humanizer.humanize(original_text)

        session['original_text'] = original_text
        session['humanized_text'] = humanized_text
        session['changes'] = changes
        session.modified = True

    word_count = len(original_text.split()) if original_text else 0
    char_count = len(original_text)
    return render_template('index.html', original=original_text, result=humanized_text, changes=changes, tone=selected_tone,
                           word_count=word_count, char_count=char_count,
                           can_undo=len(session['undo_stack']) > 0, can_redo=len(session['redo_stack']) > 0)

@app.route('/preview', methods=['POST'])
def preview():
    text = request.form.get('text', '')
    tone = request.form.get('tone', 'auto')
    if text.strip():
        preview_text, changes = humanizer.humanize(text[:100])
        if tone != 'auto':
            preview_text, tone_changes = humanizer.adjust_tone(preview_text, tone)
            changes.extend(tone_changes)
        return jsonify({'preview': preview_text, 'changes': changes})
    return jsonify({'preview': '', 'changes': []})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)