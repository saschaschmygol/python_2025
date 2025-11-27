import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.response?.status === 401) {
      const refresh = localStorage.getItem("refresh");
      if (!refresh) return Promise.reject(err);

      const r = await axios.post("http://localhost:8000/api/auth/refresh/", {
        refresh,
      });

      localStorage.setItem("access", r.data.access);
      localStorage.setItem("refresh", r.data.refresh);

      err.config.headers.Authorization = `Bearer ${r.data.access}`;
      return api.request(err.config);
    }
    return Promise.reject(err);
  }
);

export default api;

export interface MessageIn {
  id: number;
  chat_id_id: number;
  text: string;
  timestamp: string;
  ticket_id_id: number;
}

export interface MessageOut {
  id: number;
  user_id: number;
  text: string;
  timestamp: string;
  ticket_id_id: number;
}
export interface TicketMessagesResponse {
  ticket_id: number;
  messages_in: MessageIn[];
  messages_out: MessageOut[];
}