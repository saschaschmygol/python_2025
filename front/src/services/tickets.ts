import api from "./api";
import type { TicketMessagesResponse } from "./api";

export const TicketService = {
  async getMyTickets() {
    const res = await api.get("/api/operator/tickets_user/");
    return res.data;
  },

  async getOpenTickets() {
    const res = await api.get("/api/operator/open_ticket/");
    return res.data;
  },

  async assign(ticket_id: number) {
    return api.post("/api/operator/ticket_assign/", { ticket_id });
  },

  async close(ticket_id: number) {
    return api.post("/api/operator/ticket_close/", { ticket_id });
  },

  async getMessages(ticket_id: number): Promise<TicketMessagesResponse> {
    const res = await api.post("/api/operator/message_ticket/", { ticket_id });
    return res.data;
  },

  async reply(ticket_id: number, text: string) {
    return api.post("/api/operator/reply/", { ticket_id, text });
  },
};
