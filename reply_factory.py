from .constants import BOT_WELCOME_MESSAGE

PYTHON_QUESTION_LIST = [
    "What is the capital of France?",
    "What is 2 + 2?",
]

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id", -1)  # Initialize to -1 if not set
    if current_question_id == -1:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id == -1 or not answer:
        return False, "Please provide a valid answer."

    
    session["answers"] = session.get("answers", {})
    session["answers"][current_question_id] = answer
    return True, None  


def get_next_question(current_question_id):
    if current_question_id == -1 or current_question_id >= len(PYTHON_QUESTION_LIST) - 1:
        return None, None  

    next_question_id = current_question_id + 1
    next_question = PYTHON_QUESTION_LIST[next_question_id]
    return next_question, next_question_id


def generate_final_response(session):
    correct_answers = {
        0: "Paris",  # 
        1: "4",     # 
        
    }
    score = 0
    total_questions = len(correct_answers)
    
    for question_id, correct_answer in correct_answers.items():
        user_answer = session.get("answers", {}).get(question_id)
        if user_answer == correct_answer:
            score += 1
    return f"You scored {score} out of {total_questions}."