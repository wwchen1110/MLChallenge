import React from 'react';
import ThreadItem from './ThreadItem';

interface Thread {
    id: string;
    patient_id: string;
    created: string;
}

interface ThreadListProps {
    threads: Thread[];
    onSelectThread: (id: string) => void;
    onDeleteThread: (id: string) => void;
}

const ThreadList: React.FC<ThreadListProps> = ({ threads, onSelectThread, onDeleteThread }) => (
    <div className="thread-list">
        {threads.map(thread => (
            <ThreadItem
                key={thread.id}
                threadId={thread.id}
                patientId={thread.patient_id}
                created={thread.created}
                onSelect={onSelectThread}
                onDelete={onDeleteThread}
            />
        ))}
    </div>
);

export default ThreadList;