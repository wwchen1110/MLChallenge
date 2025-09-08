import React from 'react';
import ReactMarkdown from 'react-markdown';

interface MessageProps {
    sender: 'user' | 'agent';
    content: string;
    timestamp: string;
}

const Message: React.FC<MessageProps> = ({ sender, content, timestamp }) => {
    return (
        <div className={`message ${sender}`}>
            <div className="message-content" style={{ whiteSpace: 'pre-wrap' }}>
                {sender === 'agent' ? (
                    <ReactMarkdown>{content}</ReactMarkdown>
                ) : (
                    content
                )}
            </div>
            <div className="message-timestamp">{timestamp}</div>
        </div>
    );
};

export default Message;