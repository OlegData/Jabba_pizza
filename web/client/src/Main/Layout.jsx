import { Link } from 'react-router-dom';
import logo from '../assets/logo_192.png';
import './Layout.css';
import { API_URLS } from '../shared/routes';
const Layout = ({ children }) => {
  return (
    <div className="page">
      <header className="header">
        <div className="logo">
          <img src={logo} alt="Delicious Pizza" className="logo-image" />
        </div>
        <div className="brand">
          <div className="logo_text"> Jabba Pizza </div>
          <nav className="menu">
            <div className="menu-left">
              <Link to={API_URLS.home}>Home</Link>
              <Link to={API_URLS.restaurants}>Restaurants</Link>
              <Link to={API_URLS.orders}>Orders</Link>
              <Link to={API_URLS.news}>News</Link>
            </div>
            <div className="menu-right">
              <Link to={API_URLS.login}>Login</Link>
              <Link to={API_URLS.register}>Register</Link>
            </div>
          </nav>
        </div>
      </header>
      <main className="content">{children}</main>
    </div>
  );
};

export { Layout };
