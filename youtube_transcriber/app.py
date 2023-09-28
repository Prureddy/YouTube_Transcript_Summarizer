from flask import Flask, request, jsonify
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    # Get the YouTube video URL from the request
    youtube_video = request.json.get('youtube_url')
    video_id = youtube_video.split("=")[1]

    # Retrieve the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Concatenate the transcript text
    result = ""
    for i in transcript:
        result += ' ' + i['text']

    # Initialize the summarization pipeline
    summarizer = pipeline('summarization')

    # Calculate the number of iterations based on the text length
    num_iters = int(len(result) / 1000)
    summarized_text = []

    # Summarize the transcript in chunks of 1000 characters
    for i in range(0, num_iters + 1):
        start = i * 1000
        end = (i + 1) * 1000

        # Summarize the chunk
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']

        # Append the summarized text to the list
        summarized_text.append(out)

    # Convert the summarized text list to a string
    summarized_text_str = ' '.join(summarized_text)

    # Return the summarized text as a JSON response
    return jsonify({'summarized_text': summarized_text_str})

if __name__ == '__main__':
    app.run(debug=True)