import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { HomePage } from './Home';

describe('HomePage', () => {
  beforeEach(() => {
    globalThis.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ token: 'fake-token' }),
      })
    ) as unknown as jest.Mock;
  });
  it('renders the home page with welcome message and call-to-action buttons', async () => {
    render(
      <MemoryRouter>
        {' '}
        <HomePage />{' '}
      </MemoryRouter>
    );
    await waitFor(() => {
      screen.getByText(/Welcome to Jabba Pizza!/i);
    });
    await screen.getByText(/Your favorite place to order delicious pizzas online/i);
    await screen.getByRole('link', { name: /Order now/i });
    await screen.getByRole('link', { name: /Create account/i });
  });
});
