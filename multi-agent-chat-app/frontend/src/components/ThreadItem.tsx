import React from 'react';

interface ThreadItemProps {
    threadId: string;
    patientId: string;
    created: string;
    onSelect: (id: string) => void;
    onDelete: (id: string) => void;
}

const ThreadItem: React.FC<ThreadItemProps> = ({ threadId, patientId, created, onSelect, onDelete }) => (
    <div className="thread-item">
        <span onClick={() => onSelect(threadId)}>
            {created} — Patient ID: {patientId}
        </span>
        <button onClick={() => onDelete(threadId)}>Delete</button>
    </div>
);

export default ThreadItem;