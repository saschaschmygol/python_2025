import { useState } from 'react';
import { Box, Button, TextField, Typography, Card, CardContent } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  async function submit() {
    console.log('login try', username, password);
    await AuthService.login(username, password);
    navigate('/');
  }

  return (
    <Box height="100vh" display="flex" alignItems="center" justifyContent="center">
      <Card sx={{ width: 350 }}>
        <CardContent>
          <Typography variant="h5" mb={2} textAlign="center">
            Авторизация
          </Typography>

          <TextField
            fullWidth
            label="Логин"
            value={username}
            sx={{ mb: 2 }}
            onChange={(e) => setUsername(e.target.value)}
          />

          <TextField
            fullWidth
            type="password"
            label="Пароль"
            value={password}
            sx={{ mb: 2 }}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button variant="contained" fullWidth sx={{ mt: 2 }} onClick={submit}>
            Войти
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}
