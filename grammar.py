from flask import Blueprint, jsonify, render_template, request
import json
from flask_login import current_user, login_required
from generate import create_sys_msg, generate_response
from database import db, Score
from decorators_func import user_required

grammar_bp = Blueprint('grammar', __name__)

@grammar_bp.route('/grammar')
@login_required
@user_required
def grammar():
    return render_template('grammar.html')

@grammar_bp.route('/grammar/nouns')
@login_required
@user_required
def nouns():
    return render_template('nouns.html')

@grammar_bp.route('/grammar/verbs')
@login_required
@user_required
def verbs():
    return render_template('verbs.html')

@grammar_bp.route('/grammar/pronouns')
@login_required
@user_required
def pronouns():
    return render_template('pronouns.html')

@grammar_bp.route('/grammar/adverbs')
@login_required
@user_required
def adverbs():
    return render_template('adverbs.html')

@grammar_bp.route('/grammar/unjumble')
@login_required
@user_required
def unjumble():
    return render_template('unjumble.html')

@grammar_bp.route('/grammar/quiz')
@login_required
@user_required
def grammar_quiz():
    # message = create_sys_msg('Generate 1 small mcq grammatical questions for nursery kids and give 4 choices for each question in json format: {"questions":[{"question": "What is the name of the tiny bird in the story?","options": ["Bella", "Stella", "Della", "Ella"],"correct_answer": "Bella"}]}', '')
    # questions_json = generate_response(message)
    questions_json = '{"questions": [{"question": "Which of the following is an example of a preposition?","options": ["Run", "Jump", "Above", "Quickly"],"correct_answer": "Above"}]}'
    questions_data = json.loads(questions_json)
    return render_template('grammar_quiz.html', questions=questions_data)

@grammar_bp.route('/update_grammar_score', methods=['POST'])
@login_required
@user_required
def update_grammar_score():
    data = request.get_json()
    value = data.get('score', '')

    # Find the score entry for the current user
    score = Score.query.filter_by(user_id=current_user.id).first()

    if score:
        # Update the scores based on the received value
        if value == 1:
            score.total_grammar_score += 1
            score.total_correct_grammar_score += 1
        elif value == 0:
            score.total_grammar_score += 1

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Score Updated'})
    else:
        # Create a new score entry if none exists for the user
        if value == 1:
            total_grammar_score = 1
            total_correct_grammar_score = 1
        else:
            total_grammar_score = 0
            total_correct_grammar_score = 0

        new_score = Score(total_grammar_score=total_grammar_score,
                        total_correct_grammar_score=total_correct_grammar_score,
                        user_id=current_user.id)
        db.session.add(new_score)
        db.session.commit()

        return jsonify({'message': 'New Score Created'})