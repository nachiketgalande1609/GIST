import json
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, current_user
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
import requests
from database import db, User, Score
from auth import auth_bp
from grammar import grammar_bp
from text_to_speech import tts_bp
from vocab import vocab_bp
from generate import create_sys_msg, generate_response
from decorators_func import user_required, therapist_required
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, static_url_path='/static')

app.register_blueprint(auth_bp)
app.register_blueprint(grammar_bp)
app.register_blueprint(tts_bp)
app.register_blueprint(vocab_bp)


# Flask Login
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'auth.login'

# Route for the home page
@app.route('/')
@app.route('/profile')
@login_required
@user_required
def profile():
    score = Score.query.filter_by(user_id=current_user.id).first()
    try:
        grammar_score_perc = int(score.total_correct_grammar_score/score.total_grammar_score*100)
    except:
        grammar_score_perc = int(0)
    
    try:
        stories_score_perc = int(score.total_correct_stories_score/score.total_stories_score*100)
    except:
        stories_score_perc = int(0)

    if grammar_score_perc<=35:
        grammar_score_color = '#de1a24'
    elif grammar_score_perc>35 and grammar_score_perc<=75:
        grammar_score_color = '#FFBF00'
    elif grammar_score_perc>75 and grammar_score_perc<=100:
        grammar_score_color = '#3f8f29'

    if stories_score_perc<=35:
        stories_score_color = '#de1a24'
    elif stories_score_perc>35 and stories_score_perc<=75:
        stories_score_color = '#FFBF00'
    elif stories_score_perc>75 and stories_score_perc<=100:
        stories_score_color = '#3f8f29'

    return render_template('profile.html', score=score, grammar_score_perc=grammar_score_perc, stories_score_perc=stories_score_perc, grammar_score_color=grammar_score_color, stories_score_color=stories_score_color)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    print('Running')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    age = request.form.get('age')
    dob_str  = request.form.get('dob')
    gender = request.form.get('gender')
    father_name = request.form.get('fatherName')
    mother_name = request.form.get('motherName')
    address = request.form.get('address')
    state = request.form.get('state')
    pincode = request.form.get('pincode')

    dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
    dob = dob if dob_str else None
    father_name = father_name if father_name else None
    mother_name = mother_name if mother_name else None
    address = address if address else None
    state = state if state else None
    pincode = pincode if pincode else None
    # Retrieve the current user
    user = current_user

    # Update the user's profile
    user.first_name = first_name
    user.last_name = last_name
    user.age = age
    user.dob = dob
    user.gender = gender
    user.father_name = father_name
    user.mother_name = mother_name
    user.address = address
    user.state = state
    user.pincode = pincode

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'})

@app.route('/talk_to_me')
@login_required
@user_required
def talk_to_me():
    return render_template('talk_to_me.html')


@app.route('/pronunciation')
@login_required
@user_required
def pronunciation():
    letters = ['p', 'b', 't', 'd', 'k', 'g']
    return render_template('pronunciation.html', letters=letters)

@app.route('/prac_with_words/<selectedLetter>')
@login_required
@user_required
def prac_with_words(selectedLetter):
    # message = create_sys_msg('Generate 3 simple comma separated words for children starting from the prompted letter', selectedLetter)
    # words = generate_response(message)
    # words_list = words.split(',')
    
    # headers = {
    #     'Authorization': 'UFUD1Sf8ucQPKBrW8sBnnN5VivqqsHyjhtQqg7aWXWFAfg7XvfpDON7O'
    # }

    # word_image_dict = {}

    # for word in words_list:
    #     # Fetch image for the word
    #     word_query = f'https://api.pexels.com/v1/search?query={word}&per_page=1'
    #     response = requests.get(word_query, headers=headers)
        
    #     if response.status_code == 200:
    #         data = response.json()
    #         if 'photos' in data and len(data['photos']) > 0:
    #             image_url = data['photos'][0]['src']['original']
    #             word_image_dict[word] = image_url
    #         else:
    #             word_image_dict[word] = None
    #     else:
    #         word_image_dict[word] = None
    # print(word_image_dict)

    word_image_dict = {'Pen': '../static/images/pronunciation/pen.jpg', ' Pencil': '../static/images/pronunciation/pencil.jpg', ' Pot': '../static/images/pronunciation/pot.jpg', 'Pan': '../static/images/pronunciation/pan.jpg'}
    return render_template('prac_with_words.html', selectedLetter=selectedLetter, word_image_dict=word_image_dict)

@app.route('/tongue_twisters/<selectedLetter>')
@login_required
@user_required
def tongue_twisters(selectedLetter):
    # message = create_sys_msg('Generate 2 simple | separated tongue twister for kids having the prompted letter', selectedLetter)
    # response = generate_response(message)
    # twisters_list = response.split('|')
    twisters_list = ["Peter Piper picked a peck of pickled peppers", "Polly the pink parrot prances in the park."]
    return render_template('tongue_twisters.html', selectedLetter=selectedLetter, twisters_list=twisters_list)

@app.route('/stories')
@login_required
@user_required
def stories():
    # message = create_sys_msg('Generate a 30 words story for children having simple prompted letter', selectedLetter)
    # story = generate_response(message)
    # message = create_sys_msg('Generate 1 mcq questions based on this story and give 4 choices for each question in json format: {"questions":[{"question": "What is the name of the tiny bird in the story?","options": ["Bella", "Stella", "Della", "Ella"],"correct_answer": "Bella"}]}', story)
    # questions_json = generate_response(message)
    questions_json = '{"questions":[{"question": "What did the fox say about the grapes he couldn\'t reach?","options": ["They were sweet.", "They were sour.", "They were spicy.", "They were bitter."],"correct_answer": "They were sour."}]}'
    questions_data = json.loads(questions_json)
    story = "The fox couldn't reach the grapes, so he said they were sour."
    return render_template('stories.html', story=story, questions=questions_data)

@app.route('/update_stories_score', methods=['POST'])
@login_required
@user_required
def update_stories_score():
    data = request.get_json()
    value = data.get('score', '')

    # Find the score entry for the current user
    score = Score.query.filter_by(user_id=current_user.id).first()

    if score:
        # Update the scores based on the received value
        if value == 1:
            score.total_stories_score += 1
            score.total_correct_stories_score += 1
        elif value == 0:
            score.total_stories_score += 1

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Score Updated'})
    else:
        # Create a new score entry if none exists for the user
        if value == 1:
            total_stories_score = 1
            total_correct_stories_score = 1
        else:
            total_stories_score = 0
            total_correct_stories_score = 0

        new_score = Score(total_stories_score=total_stories_score,
                        total_correct_stories_score=total_correct_stories_score,
                        user_id=current_user.id)
        db.session.add(new_score)
        db.session.commit()

        return jsonify({'message': 'New Score Created'})

@app.route('/connect')
@login_required
@user_required
def connect():
    return render_template('connect.html')    

@app.route('/therapist_dashboard')
@login_required
@therapist_required
def therapist_dashboard():
    return render_template('therapist_dashboard.html')

@app.route('/add_patient')
@login_required
@therapist_required
def add_patient():
    return render_template('add_patient.html')

@app.route('/patient_details/<int:user_id>')
@login_required
@therapist_required
def patient_details(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('patient_details.html', user=user)
    else:
        return redirect(url_for('patient_search'))

@app.route('/patient_search', methods=['GET', 'POST'])
@login_required
@therapist_required
def patient_search():
    search_results = []
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        # Retrieve users who are not therapists based on search query
        search_results = User.query.filter_by(is_therapist=False).filter(
            (User.first_name.ilike(f'%{search_query}%')) | 
            (User.last_name.ilike(f'%{search_query}%'))
        ).all()
    return render_template('patient_search.html', search_results=search_results)

@app.route('/session_call')
@login_required
def session_call():
    return render_template('session_call.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)