from flask import Blueprint, request, jsonify, send_file
from gtts import gTTS
import io
import os
import tempfile
import uuid
from pydub import AudioSegment
from pydub.effects import speedup, normalize

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/generate', methods=['POST'])
def generate_speech():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Get optional parameters
        language = data.get('language', 'en')
        speed = float(data.get('speed', 1.0))
        
        # Validate speed
        if speed < 0.5 or speed > 2.0:
            speed = 1.0
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Create a temporary file for the initial audio
        temp_audio = io.BytesIO()
        tts.write_to_fp(temp_audio)
        temp_audio.seek(0)
        
        # Load audio with pydub for processing
        audio = AudioSegment.from_mp3(temp_audio)
        
        # Apply speed adjustment if needed
        if speed != 1.0:
            # Calculate the new frame rate for speed adjustment
            new_sample_rate = int(audio.frame_rate * speed)
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
            audio = audio.set_frame_rate(audio.frame_rate)
        
        # Normalize audio
        audio = normalize(audio)
        
        # Export to MP3
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format="mp3", bitrate="128k")
        output_buffer.seek(0)
        
        # Generate a unique filename
        filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
        
        return send_file(
            output_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate speech: {str(e)}'}), 500

@tts_bp.route('/preview', methods=['POST'])
def preview_speech():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Get optional parameters
        language = data.get('language', 'en')
        speed = float(data.get('speed', 1.0))
        
        # Validate speed
        if speed < 0.5 or speed > 2.0:
            speed = 1.0
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Create a temporary file for the initial audio
        temp_audio = io.BytesIO()
        tts.write_to_fp(temp_audio)
        temp_audio.seek(0)
        
        # Load audio with pydub for processing
        audio = AudioSegment.from_mp3(temp_audio)
        
        # Apply speed adjustment if needed
        if speed != 1.0:
            # Calculate the new frame rate for speed adjustment
            new_sample_rate = int(audio.frame_rate * speed)
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
            audio = audio.set_frame_rate(audio.frame_rate)
        
        # Normalize audio
        audio = normalize(audio)
        
        # Export to MP3
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format="mp3", bitrate="128k")
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate speech: {str(e)}'}), 500

@tts_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get available languages for TTS"""
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese (Mandarin)',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'da': 'Danish',
        'no': 'Norwegian',
        'fi': 'Finnish',
        'pl': 'Polish',
        'tr': 'Turkish',
        'th': 'Thai'
    }
    
    return jsonify({'languages': languages})

