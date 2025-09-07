import React from 'react';

interface MessageProps {
    key: number;
    sender: 'user' | 'agent';
    content: string;
    timestamp: string;
}

const Message: React.FC<MessageProps> = ({ sender, content, timestamp }) => {
    return (
        <div className={`message ${sender}`}>
            <div className="message-content" style={{ whiteSpace: 'pre-wrap' }}>
                {content}
            </div>
            <div className="message-timestamp">{timestamp}</div>
        </div>
    );
};

export default Message;