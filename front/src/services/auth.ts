import api from "./api";

export const AuthService = {
  async login(username: string, password: string) {
    const res = await api.post("/api/auth/login/", { username, password });
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
    return res.data.user;
  },

  async refresh() {
    const refresh = localStorage.getItem("refresh");
    const res = await api.post("/api/auth/refresh/", { refresh });
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
  },
};
