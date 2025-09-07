import React, { useRef, useEffect } from 'react';
import Message from './Message';

interface ConversationProps {
    messages: { id: number; content: string; sender: 'user' | 'agent'; timestamp: string }[];
}

const Conversation: React.FC<ConversationProps> = ({ messages }) => {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="conversation" ref={containerRef} style={{ flex: 1, overflowY: 'auto', padding: '1rem' }}>
            {messages.map((message) => (
                <Message
                    key={message.id}
                    content={message.content}
                    sender={message.sender}
                    timestamp={message.timestamp}
                />
            ))}
        </div>
    );
};

export default Conversation;