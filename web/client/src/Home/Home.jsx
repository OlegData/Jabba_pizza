import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import pizza from '../assets/pizza.png';
import css from './Home.module.css';
const Home = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('/token', { credentials: 'include', redirect: 'manual' });
        if (response.ok) {
          setData(await response.json());
          console.log('Data:', data);
        }
      } catch (error) {
        console.error('Error fetching token:', error);
      } finally {
        setLoading(false);
      }
    }
    setLoading(true);
    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <section className={css.hero}>
      <div className={css.heroText}>
        <p className={css.eyebrow}>Hot, fast, and made to order</p>
        <h1 className={css.title}>Welcome to Jabba Pizza!</h1>
        <p className={css.subtitle}>
          Your favorite place to order delicious pizzas online. Fresh dough, bold flavors, and
          extra-cheesy slices delivered right to your door.
        </p>
        <div className={css.ctaRow}>
          <Link to="/login" className={css.ctaPrimary}>
            Order now
          </Link>
          <Link to="/register" className={css.ctaSecondary}>
            Create account
          </Link>
        </div>
      </div>
      <div className={css.heroImageWrap}>
        <img src={pizza} alt="Order Pizza" className={css.heroImg} />
      </div>
    </section>
  );
};

export { Home };
