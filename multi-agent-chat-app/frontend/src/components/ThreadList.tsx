import React from 'react';
import ThreadItem from './ThreadItem';

interface Thread {
    id: string;
    name: string;
}

interface ThreadListProps {
    threads: Thread[];
    onSelectThread: (id: string) => void;
    onRenameThread: (id: string, newName: string) => void;
    onDeleteThread: (id: string) => void;
}

const ThreadList: React.FC<ThreadListProps> = ({ threads, onSelectThread, onRenameThread, onDeleteThread }) => {
    return (
        <div className="thread-list">
            {threads.map(thread => (
                <ThreadItem
                    key={thread.id}
                    threadId={thread.id}
                    threadName={thread.name}
                    onSelect={onSelectThread}
                    onRename={onRenameThread}
                    onDelete={onDeleteThread}
                />
            ))}
        </div>
    );
};

export default ThreadList;