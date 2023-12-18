from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)


openai.api_key = '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'


fruit_files_dir = r'C:\Users\dell\Desktop\chatbot microservice'

@app.route('/get_fruit_info', methods=['POST'])
def get_fruit_info():
    try:
        data = request.get_json()
        user_input = data.get('input', 'Tell me about a sweet fruit').lower()

        
        if not user_input:
            return jsonify({'error': 'Input is empty.'}), 400

        # Call OpenAI GPT model
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=100
        )

        generated_text = response['choices'][0]['text'].strip()

        
        relevant_fruit = None
        for file_name in os.listdir(fruit_files_dir):
            if file_name.lower().startswith(generated_text.split()[0]):
                relevant_fruit = file_name.split('.')[0]
                break

        if relevant_fruit:
            file_path = os.path.join(fruit_files_dir, file_name)
            with open(file_path, 'r') as file:
                fruit_info = file.read()
            return jsonify({'fruit_info': fruit_info})
        else:
            return jsonify({'error': 'Unable to determine relevant fruit.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
