import { Link } from 'react-router-dom';
import logo from '../assets/logo_192.png';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="page">
      <header className="header">
        <div className="logo">
          <img src={logo} alt="Delicious Pizza" className="logo-image" />
        </div>
        <div className="logo_text"> Jabba Pizza </div>
        <nav className="menu">
          <Link to="/">Home</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </nav>
      </header>
      <main className="content">
        <div className="welcome-text">
          <h1>Welcome to Jabba Pizza!</h1>
          <p>Your favorite place to order delicious pizzas online.</p>
        </div>
      </main>
      <section className="content">{children}</section>
    </div>
  );
};

export { Layout };
