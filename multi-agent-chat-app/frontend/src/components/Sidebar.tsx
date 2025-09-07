import React from 'react';

interface Thread {
    id: string;
    name: string;
}

interface SidebarProps {
    threads: Thread[];
    onSelectThread: (id: string) => void;
    onCreateThread: (name: string) => void;
    onRenameThread: (id: string, newName: string) => void;
    onDeleteThread: (id: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ threads, onSelectThread, onCreateThread, onRenameThread, onDeleteThread }) => {
    const handleCreateThread = () => {
        const threadName = prompt("Enter thread name:");
        if (threadName) {
            onCreateThread(threadName);
        }
    };

    const handleRenameThread = (threadId: string) => {
        const newName = prompt("Enter new thread name:");
        if (newName) {
            onRenameThread(threadId, newName);
        }
    };

    const handleDeleteThread = (threadId: string) => {
        if (window.confirm("Are you sure you want to delete this thread?")) {
            onDeleteThread(threadId);
        }
    };

    return (
        <div className="sidebar">
            <h2>Threads</h2>
            <button onClick={handleCreateThread}>Create Thread</button>
            <ul>
                {threads.map(thread => (
                    <li key={thread.id}>
                        <span onClick={() => onSelectThread(thread.id)}>{thread.name}</span>
                        <button onClick={() => handleRenameThread(thread.id)}>Rename</button>
                        <button onClick={() => handleDeleteThread(thread.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;