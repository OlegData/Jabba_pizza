import { Routes, Route } from 'react-router-dom';
import { HomePage } from './Home/Home.jsx';
import { OrdersPage } from './Orders/Orders.jsx';
import { Layout } from './Main/Layout.jsx';
import { NewsPage } from './News/News.jsx';
import { RestaurantsPage } from './Restaurants/Restaurants.jsx';
import { LoginForm } from './Auth/Login.jsx';
import { RegisterForm } from './Registration/RegisterForm.jsx';
import { API_URLS } from './shared/routes.js';

import './App.css';

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path={API_URLS.home} element={<HomePage />} />
        <Route path={API_URLS.orders} element={<OrdersPage />} />
        <Route path={API_URLS.restaurants} element={<RestaurantsPage />} />
        <Route path={API_URLS.news} element={<NewsPage />} />
        <Route path={API_URLS.login} element={<LoginForm />} />
        <Route path={API_URLS.register} element={<RegisterForm />} />
      </Routes>
    </Layout>
  );
};

export default App;
