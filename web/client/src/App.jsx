import { Routes, Route } from 'react-router-dom';
import { Home } from './Home/Home.jsx';
import { Layout } from './Main/Layout.jsx';
import { LoginForm } from './Auth/Login.jsx';
import { RegisterForm } from './Registration/RegisterForm.jsx';
import { API_URLS } from './shared/routes.js';

import './App.css';

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path={API_URLS.home} element={<Home />} />
        <Route path={API_URLS.orders} element={<Home />} />
        <Route path={API_URLS.restaurants} element={<Home />} />
        <Route path={API_URLS.news} element={<Home />} />
        <Route path={API_URLS.login} element={<LoginForm />} />
        <Route path={API_URLS.register} element={<RegisterForm />} />
      </Routes>
    </Layout>
  );
};

export default App;
