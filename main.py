import os,requests,json
from flask import Flask, request, jsonify , Response
from flask_caching import Cache
from datetime import datetime

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL')
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache = Cache(app)


STACKEXCHANGE_API_BASE_URL = "https://api.stackexchange.com/2.3"
STACKEXCHANGE_API_KEY = "7KZ5FugAHgvz2vnCLYHGlw(("


def get_stackoverflow_data(since, until):
    params = {
        "site": "stackoverflow",
        "key": STACKEXCHANGE_API_KEY,
        "fromdate": int(since.timestamp()),
        "todate": int(until.timestamp()),
        "order": "desc",
        "sort": "creation"
    }

    # Retrieve StackOverflow answer data
    response = requests.get(f"{STACKEXCHANGE_API_BASE_URL}/answers", params=params)
    
    answers_data = response.json()["items"]

    # Retrieve comment data for these answers , could be seperate method but code is pretty compact already.
    answer_ids = [answer["answer_id"] for answer in answers_data]
    comment_params = {
        "site": "stackoverflow",
        "key": STACKEXCHANGE_API_KEY,
    }
    comment_counts = {}
    for answer_id in answer_ids:
        comment_params["ids"] = answer_id
        response = requests.get(f"{STACKEXCHANGE_API_BASE_URL}/answers/{answer_id}/comments", params=comment_params)
        comment_counts[answer_id] = len(response.json()["items"])

    return answers_data, comment_counts


def calculate_statistics(answers_data, comment_counts):
    total_accepted_answers = sum(1 for answer in answers_data if answer["is_accepted"])
    average_score_accepted_answers = sum(answer["score"] for answer in answers_data if answer["is_accepted"]) / total_accepted_answers if total_accepted_answers > 0 else 0
    average_answer_count_per_question = len(answers_data) / len(set(answer["question_id"] for answer in answers_data))
    top_10_answers_with_highest_score = sorted(answers_data, key=lambda x: x["score"], reverse=True)[:10]
    top_10_comments_count = {answer["answer_id"]: comment_counts[answer["answer_id"]] for answer in top_10_answers_with_highest_score}

    return {
        "total_accepted_answers": total_accepted_answers,
        "average_score_accepted_answers": average_score_accepted_answers,
        "average_answer_count_per_question": average_answer_count_per_question,
        "top_10_comments_count": top_10_comments_count,
    }


@app.route('/api/v1/stackstats')
@cache.cached(timeout=300 , key_prefix=lambda: request.url)  # Cache results for 5 minutes
def stack_stats():
    since = datetime.strptime(request.args.get('since'), "%Y-%m-%d %H:%M:%S")
    until = datetime.strptime(request.args.get('until'), "%Y-%m-%d %H:%M:%S")

    answers_data, comment_counts = get_stackoverflow_data(since, until)
    statistics = calculate_statistics(answers_data, comment_counts)

    json_data = json.dumps(statistics, sort_keys=False)

    # Return a Flask Response object with the JSON data
    return Response(json_data, mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True ,host='0.0.0.0', port=5000)