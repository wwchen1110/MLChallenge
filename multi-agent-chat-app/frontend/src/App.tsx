import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import './styles/main.css';

const App: React.FC = () => {
    return (
        <Router>
            <div className="app">
                <Routes>
                    <Route path="/" element={<ChatPage />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;