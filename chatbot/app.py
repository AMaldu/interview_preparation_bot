from flask import Flask, request, jsonify
import uuid
from rag import rag 

app = Flask(__name__)

conversations = {}

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    conversation_id = str(uuid.uuid4())
    
    result = rag(question)

    # posible movida
    conversations[conversation_id] = {'question': question, 'result': result}
    
    return jsonify({'conversation_id': conversation_id,'question': question, 'result': result}), 200


@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    conversation_id = data.get('conversation_id')
    feedback_value = data.get('feedback')  

    if not conversation_id or feedback not in [1,-1]:
        return jsonify({"error": "Invalid Input"}), 400
    
    if conversation_id in conversations:
        conversations[conversation_id]['feedback'] = feedback_value
        
        return jsonify({'id': 'conversation_id', 'status': 'success', 'message': 'Feedback received'}), 200
    else:
        return jsonify({'id': 'conversation_id','status': 'error', 'message': 'Conversation ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
