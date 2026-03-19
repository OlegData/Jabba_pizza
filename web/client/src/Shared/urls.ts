import { UNEXPECTED_ERROR, FAILED_TO_FETCH_ERROR } from './Constants';

const getUrl = async (path: string) => {
  try {
    const response = await fetch(path, { credentials: 'include', redirect: 'manual' });
    if (response.ok) {
      const ct = response.headers.get('content-type') || '';
      if (ct.includes('application/json')) {
        const json = await response.json();
        return json;
      } else {
        return { error: UNEXPECTED_ERROR };
      }
    }
  } catch (e) {
    return { error: FAILED_TO_FETCH_ERROR };
  }
};

const getTicketUrl = (ticketId: string) => {
  token = getUrl('/token');
};

export { getUrl };
