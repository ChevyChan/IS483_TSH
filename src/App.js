import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from './components/Login';
import Register from './components/Register';
import Reset from './components/Reset';
import Dashboard from './components/Dashboard';
import UploadDocument from './components/UploadDocument';
import MyCalender from './components/calendar/MyCalendar';
import Chat from './components/chat';

function App() {
  return (
    <div className="app">
      <Router>
        <Routes>
          <Route exact path="/" element={<Login />} />
          <Route exact path="/register" element={<Register />} />
          <Route exact path="/reset" element={<Reset />} />
          <Route exact path="/dashboard" element={<Dashboard />} />
          <Route exact path="/upload_document" element={<UploadDocument/>} />
          <Route exact path="/calendar" element={<MyCalender/>} />
          <Route exact path="/chat" element={<Chat/>} />          
        </Routes>
      </Router>
    </div>
  );
}

export default App;
