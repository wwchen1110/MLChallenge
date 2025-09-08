import React, { useState } from 'react';

interface Thread {
    id: string;
    patient_id: string;
    created: string;
}

interface SidebarProps {
    threads: Thread[];
    onSelectThread: (id: string) => void;
    onCreateThread: (patientId: string) => void;
    onDeleteThread: (id: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
    threads,
    onSelectThread,
    onCreateThread,
    onDeleteThread
}) => {
    const [newPatientId, setNewPatientId] = useState('');

    const handleCreateThread = () => {
        if (newPatientId.trim()) {
            onCreateThread(newPatientId);
            setNewPatientId('');
        } else {
            alert("Please enter a patient ID.");
        }
    };

    return (
        <div className="sidebar">
            <h2>Threads</h2>
            <input
                type="text"
                placeholder="Patient ID"
                value={newPatientId}
                onChange={e => setNewPatientId(e.target.value)}
                style={{ marginBottom: '8px', width: '100%', padding: '8px' }}
            />
            <button onClick={handleCreateThread}>Create Thread</button>
            <ul>
                {threads.map(thread => (
                    <li key={thread.id}>
                        <span onClick={() => onSelectThread(thread.id)}>
                            {thread.created} — Patient ID: {thread.patient_id}
                        </span>
                        <button onClick={() => onDeleteThread(thread.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;