import React, { useState } from 'react';
import './Header.css';
import { Link } from 'react-router-dom';


function Header() {
  const [selectedLanguage, setSelectedLanguage] = useState('English');

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  };

  return (
    <header className="header">
      {/* Left side: Lobbies and About buttons grouped */}
      <div className="left-buttons">
          <Link to="/lobbies">
        <button className="header-button">Lobbies</button>
      </Link>
          <Link to ="/about">
              <button className="header-button">About</button>
          </Link>

      </div>

        {/* Center: Mahjong Title */}
      <Link to="/" className="title">
        Mahjong
      </Link>

      {/* Right side: Language Dropdown */}
      <select
        className="language-dropdown"
        value={selectedLanguage}
        onChange={handleLanguageChange}
      >
        <option value="English">English</option>
        <option value="Chinese">Chinese</option>
        <option value="Japanese">Japanese</option>
        {/* Add other languages if needed */}
      </select>

      {/* Far right: Login Button */}
        <Link to="/login">
            <button className="header-button login">Login</button>
        </Link>

    </header>
  );
}

export default Header;
