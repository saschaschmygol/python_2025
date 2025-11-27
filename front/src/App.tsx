// src/App.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Tickets from './pages/Tickets';
import TicketView from './pages/TicketView';

export default function App() {
  const isAuth = !!localStorage.getItem('access');

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={isAuth ? <Tickets /> : <Navigate to="/login" />} />
      <Route path="/ticket/:id" element={<TicketView />} />
    </Routes>
  );
}
