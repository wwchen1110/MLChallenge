import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import Conversation from '../components/Conversation';

const BACKEND_URL = 'http://localhost:5001';

const ChatPage: React.FC = () => {
    const [selectedThread, setSelectedThread] = useState<string>('');
    const [threads, setThreads] = useState<{ id: string; patient_id: string; created: string }[]>([]);
    const [messages, setMessages] = useState<{ [key: string]: any[] }>({});
    const [prompt, setPrompt] = useState('');
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    // Fetch threads from backend on mount
    useEffect(() => {
        fetch(`${BACKEND_URL}/threads`)
            .then(res => res.json())
            .then(data => {
                setThreads(data);
                if (data.length > 0) setSelectedThread(data[0].id.toString());
            });
    }, []);

    // Fetch messages for selected thread (optional: implement backend endpoint for this)
    // For now, messages are only updated locally after ask

    const handleThreadSelect = (threadId: string) => {
        setSelectedThread(threadId);
    };

    const handleCreateThread = async (patientId: string) => {
        const res = await fetch(`${BACKEND_URL}/threads`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ patient_id: patientId })
        });
        const data = await res.json();
        if (res.ok && data.thread_id) {
            // Fetch updated thread list from backend to get created date
            fetch(`${BACKEND_URL}/threads`)
                .then(res => res.json())
                .then(data => {
                    setThreads(data);
                    setSelectedThread(data[data.length - 1].id.toString());
                });
            setMessages(prev => ({ ...prev, [data.thread_id]: [] }));
        } else {
            setErrorMsg(data.error || 'Failed to create thread.');
        }
    };

    const handleRenameThread = (id: string, newName: string) => {
        setThreads(threads.map(thread => thread.id === id ? { ...thread, name: newName } : thread));
    };

    const handleDeleteThread = async (id: string) => {
        const res = await fetch(`${BACKEND_URL}/threads/${id}`, { method: 'DELETE' });
        if (res.ok) {
            const updatedThreads = threads.filter(thread => thread.id !== id);
            const updatedMessages = { ...messages };
            delete updatedMessages[id];
            setThreads(updatedThreads);
            setMessages(updatedMessages);
            if (selectedThread === id && updatedThreads.length > 0) {
                setSelectedThread(updatedThreads[0].id);
            } else if (updatedThreads.length === 0) {
                setSelectedThread('');
            }
        } else {
            const data = await res.json();
            setErrorMsg(data.error || 'Failed to delete thread.');
        }
    };

    const handlePromptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPrompt(e.target.value);
    };

    const handlePromptSubmit = async () => {
        if (!prompt.trim() || !selectedThread) return;
        setLoading(true);
        setErrorMsg(null);

        // Add user message locally
        const userMessage = {
            id: messages[selectedThread]?.length ? messages[selectedThread].length + 1 : 1,
            content: prompt,
            sender: 'user' as 'user',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => ({
            ...prev,
            [selectedThread]: [...(prev[selectedThread] || []), userMessage]
        }));

        try {
            const response = await fetch(`${BACKEND_URL}/threads/${selectedThread}/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input: prompt })
            });
            const data = await response.json();
            if (response.ok && data.reply) {
                const agentMessage = {
                    id: userMessage.id + 1,
                    content: data.reply,
                    sender: 'agent' as 'agent',
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                };
                setMessages(prev => ({
                    ...prev,
                    [selectedThread]: [...(prev[selectedThread] || []), agentMessage]
                }));
            } else {
                setErrorMsg(data.error || 'Unknown error from backend.');
                const errorMessage = {
                    id: userMessage.id + 1,
                    content: `Error: ${data.error || 'Unknown error from backend.'}`,
                    sender: 'agent' as 'agent',
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                };
                setMessages(prev => ({
                    ...prev,
                    [selectedThread]: [...(prev[selectedThread] || []), errorMessage]
                }));
            }
        } catch (error: any) {
            setErrorMsg(error.message || 'Network error');
            const errorMessage = {
                id: userMessage.id + 1,
                content: `Error: ${error.message || 'Network error'}`,
                sender: 'agent' as 'agent',
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            setMessages(prev => ({
                ...prev,
                [selectedThread]: [...(prev[selectedThread] || []), errorMessage]
            }));
        }

        setPrompt('');
        setLoading(false);
    };

    return (
        <div className="chat-page">
            <Sidebar
                threads={threads}
                onSelectThread={handleThreadSelect}
                onCreateThread={handleCreateThread}
                onDeleteThread={handleDeleteThread}
            />
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <Conversation
                    messages={messages[selectedThread] || []}
                />
                {errorMsg && (
                    <div className="error-message">
                        {errorMsg}
                    </div>
                )}
                <div className="input-area">
                    <input
                        type="text"
                        value={prompt}
                        onChange={handlePromptChange}
                        onKeyDown={e => {
                            if (e.key === 'Enter' && !loading && prompt.trim()) {
                                handlePromptSubmit();
                            }
                        }}
                        placeholder="Type your prompt..."
                        disabled={loading}
                    />
                    <button onClick={handlePromptSubmit} disabled={loading || !prompt.trim()}>
                        {loading ? 'Sending...' : 'Send'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatPage;