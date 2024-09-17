import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/features">Features</Link>
        <Link to="/education">Education</Link>
        <Link to="/community">Community</Link>
        <Link to="/sentiment">Sentiment Analysis</Link>
        <Link to="/contact">Contact</Link>
      </nav>
    </header>
  );
};

export default Header;
