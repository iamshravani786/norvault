import { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2 } from 'lucide-react';

interface VoiceAssistantProps {
  onCommand: (orgNumber: string) => void;
  isProcessing?: boolean;
}

export function VoiceAssistant({ onCommand }: VoiceAssistantProps) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      setIsSupported(true);
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      
      recognition.onresult = (event: any) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
        
        if (event.results[event.results.length - 1].isFinal) {
          handleVoiceResult(currentTranscript);
        }
      };

      recognition.onerror = () => {
        setIsListening(false);
        setTranscript('Voice recognition error. Please try again.');
        setTimeout(() => setTranscript(''), 3000);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const handleVoiceResult = (text: string) => {
    const match = text.replace(/\s/g, '').match(/\d{9}/);
    if (match) {
      const orgNum = match[0];
      speak(`Searching for company ${orgNum}`);
      onCommand(orgNum);
    } else {
      speak("I couldn't find a 9-digit organization number. Please try again.");
    }
    setTimeout(() => setTranscript(''), 4000);
  };

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    if (isListening) {
      recognitionRef.current.stop();
    } else {
      setTranscript('🎙️ Listening... say a 9-digit org number');
      try {
        recognitionRef.current.start();
      } catch {
        setTranscript('Microphone busy — please wait and try again.');
        setTimeout(() => setTranscript(''), 3000);
      }
    }
  };

  const speak = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(true);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.1;
      utterance.onend = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  if (!isSupported) return null;

  return (
    <div className="fixed bottom-6 left-6 z-50 flex flex-col items-start">
      {transcript && (
        <div className="bg-white border-2 border-[#1e3a8a] text-[#1e3a8a] p-3 rounded-xl shadow-lg mb-3 max-w-xs">
          <p className="text-sm font-medium">{transcript}</p>
        </div>
      )}
      
      <button
        onClick={toggleListening}
        className={`p-4 rounded-full shadow-2xl transition-all duration-300 flex items-center justify-center ${
          isListening 
            ? 'bg-red-500 hover:bg-red-600 text-white animate-pulse scale-110' 
            : 'bg-[#1e3a8a] hover:bg-[#1e40af] text-white'
        }`}
        title={isListening ? 'Stop listening' : 'Voice AI Agent — click to speak'}
      >
        {isListening ? <MicOff size={24} /> : (isSpeaking ? <Volume2 size={24} className="animate-pulse" /> : <Mic size={24} />)}
      </button>
    </div>
  );
}
