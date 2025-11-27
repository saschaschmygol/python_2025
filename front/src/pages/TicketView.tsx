// src/pages/TicketView.tsx
import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { TicketService } from '../services/tickets';
import { Box, Typography, TextField, Button, Paper, Container } from '@mui/material';
import { useSearchParams } from 'react-router-dom';

interface RawMsg {
  id: number;
  text: string;
  timestamp: string;
}

interface TicketMessagesResponse {
  messages_in: RawMsg[];
  messages_out: RawMsg[];
}

interface Msg {
  id: number;
  text: string;
  timestamp: string;
  type: 'in' | 'out';
}
export default function TicketView() {
  const [params] = useSearchParams();
  const readonly = params.get('view') === 'readonly';

  const navigate = useNavigate();
  const { id } = useParams();
  const ticket_id = Number(id);

  const [messages, setMessages] = useState<Msg[]>([]);
  const [text, setText] = useState('');

  const load = useCallback(async () => {
    const data: TicketMessagesResponse = await TicketService.getMessages(ticket_id);

    const merged: Msg[] = [
      ...data.messages_in.map(
        (m: RawMsg): Msg => ({
          id: m.id,
          text: m.text,
          timestamp: m.timestamp,
          type: 'in',
        }),
      ),
      ...data.messages_out.map(
        (m: RawMsg): Msg => ({
          id: m.id,
          text: m.text,
          timestamp: m.timestamp,
          type: 'out',
        }),
      ),
    ];

    merged.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

    setMessages(merged);
  }, [ticket_id]);

  useEffect(() => {
    Promise.resolve().then(() => load());
  }, [load]);

  async function send() {
    await TicketService.reply(ticket_id, text);
    setText('');
    load();
  }

  async function close() {
    await TicketService.close(ticket_id);
    history.back();
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Button variant="outlined" sx={{ mb: 2 }} onClick={() => navigate('/')}>
        ← Назад
      </Button>
      <Typography variant="h5" mb={2}>
        Тикет #{ticket_id}
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mb: 2 }}>
        {messages.map((m) => (
          <Box
            key={`${m.type}-${m.id}`}
            sx={{
              alignSelf: m.type === 'in' ? 'flex-end' : 'flex-start',
              maxWidth: '70%',
            }}>
            <Paper
              sx={{
                p: 1,
                backgroundColor: m.type === 'in' ? 'success.dark' : 'primary.dark',
                color: '#fff',
              }}>
              {m.text}
            </Paper>
          </Box>
        ))}
      </Box>
      {!readonly && (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            value={text}
            onChange={(e) => setText(e.target.value)}
            label="Ответ"
            fullWidth
          />
          <Button variant="contained" onClick={send}>
            Отправить
          </Button>
        </Box>
      )}
      {!readonly && (
        <Button variant="contained" color="error" sx={{ mt: 2 }} onClick={close}>
          Закрыть тикет
        </Button>
      )}
    </Container>
  );
}
