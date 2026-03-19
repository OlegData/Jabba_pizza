import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

import { Layout } from './Layout';

describe('Layout', () => {
  it('renders the layout component', () => {
    render(
      <MemoryRouter>
        <Layout>Test</Layout>
      </MemoryRouter>
    );
    const layoutElement = screen.getByTestId('layout');
    expect(layoutElement).toBeInTheDocument();
    expect(screen.getByText(/Jabba Pizza/i)).toBeInTheDocument();
    expect(screen.getByAltText(/Delicious Pizz/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /home/i })).toBeInTheDocument();

    expect(screen.getByRole('link', { name: /restaurants/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /orders/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /news/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Sign Up/i })).toBeInTheDocument();
  });
});
