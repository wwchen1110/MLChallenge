import React from 'react';

interface ThreadItemProps {
    threadId: string;
    threadName: string;
    onSelect: (id: string) => void;
    onRename: (id: string, newName: string) => void;
    onDelete: (id: string) => void;
}

const ThreadItem: React.FC<ThreadItemProps> = ({ threadId, threadName, onSelect, onRename, onDelete }) => {
    const handleRename = () => {
        const newName = prompt("Enter new thread name:", threadName);
        if (newName) {
            onRename(threadId, newName);
        }
    };

    return (
        <div className="thread-item">
            <span onClick={() => onSelect(threadId)}>{threadName}</span>
            <button onClick={handleRename}>Rename</button>
            <button onClick={() => onDelete(threadId)}>Delete</button>
        </div>
    );
};

export default ThreadItem;