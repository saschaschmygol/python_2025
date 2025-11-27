import { useEffect, useState, useCallback } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Ticket {
  id: number;
  status: string;
  user_id: number | null;
  chat_id: number;
  timestamp: string;
}

export default function Tickets() {
  const [my, setMy] = useState<Ticket[]>([]);
  const [open, setOpen] = useState<Ticket[]>([]);
  const [statusFilter, setStatusFilter] = useState('all');
  const navigate = useNavigate();

  const reloadTickets = useCallback(async () => {
    const myR = await api.get('/api/operator/tickets_user/');
    const openR = await api.get('/api/operator/open_ticket/');

    const sortFn = (a: Ticket, b: Ticket) =>
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();

    setMy(myR.data.sort(sortFn));
    setOpen(openR.data.sort(sortFn));
  }, []);
  useEffect(() => {
    (async () => {
      await reloadTickets();
    })();
  }, [reloadTickets]);

  async function take(ticket_id: number) {
    await api.get('/api/operator/ticket_assign/', { params: { ticket_id } });
    await reloadTickets();
  }

  const filterFn = (t: Ticket) => (statusFilter === 'all' ? true : t.status === statusFilter);

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Typography
        variant="h5"
        textAlign="center"
        mb={3}
        sx={{ color: 'primary.main', fontWeight: 'bold' }}>
        @Desk_123_bot
      </Typography>

      <FormControl fullWidth sx={{ mb: 4 }}>
        <InputLabel>Статус</InputLabel>
        <Select
          label="Статус"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}>
          <MenuItem value="all">Все</MenuItem>
          <MenuItem value="open">Open</MenuItem>
          <MenuItem value="appointed">Назначенные</MenuItem>
          <MenuItem value="closed">Closed</MenuItem>
        </Select>
      </FormControl>

      <Grid container spacing={4}>
        {/* Назначенные */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Typography variant="h6" mb={2} color="success.main">
            Назначенные мне
          </Typography>

          {my.filter(filterFn).map((t) => (
            <Card
              key={`my-${t.id}`}
              sx={{
                mb: 2,
                backgroundColor: t.status === 'closed' ? '#600000' : '#003300',
              }}>
              <CardContent sx={{ color: '#fff' }}>
                <Typography>
                  #{t.id} — {t.status}
                </Typography>

                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  {new Date(t.timestamp).toLocaleString()}
                </Typography>

                <Button
                  variant="outlined"
                  sx={{ mt: 1, color: '#fff', borderColor: '#fff' }}
                  onClick={() => navigate(`/ticket/${t.id}`)}>
                  Открыть
                </Button>
              </CardContent>
            </Card>
          ))}
        </Grid>

        {/* Не назначенные */}
        <Grid size={{ xs: 12, md: 6 }}>
          <Typography variant="h6" mb={2} color="error.main">
            Не назначенные
          </Typography>

          {open.filter(filterFn).map((t) => (
            <Card
              key={`open-${t.id}`}
              sx={{
                mb: 2,
                backgroundColor: t.status === 'closed' ? '#600000' : '#330000',
              }}>
              <CardContent sx={{ color: '#fff' }}>
                <Typography>
                  #{t.id} — {t.status}
                </Typography>

                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  {new Date(t.timestamp).toLocaleString()}
                </Typography>

                <Button
                  variant="outlined"
                  sx={{ mt: 1, color: '#fff', borderColor: '#fff' }}
                  onClick={() => take(t.id)}>
                  Взять тикет
                </Button>
                <Button
                  variant="outlined"
                  sx={{ color: '#fff', borderColor: '#fff' }}
                  onClick={() => navigate(`/ticket/${t.id}?view=readonly`)}>
                  Просмотр
                </Button>
              </CardContent>
            </Card>
          ))}
        </Grid>
      </Grid>
    </Container>
  );
}
