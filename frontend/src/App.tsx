import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  TextField,
  Button,
  Box,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody
} from '@mui/material';

interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
}

function App() {
  // -------------------------
  // 1. Local State
  // -------------------------
  // Default to showing course id and name
  const [columns, setColumns] = useState<string[]>(['id', 'name']);
  const [courses, setCourses] = useState<any[]>([]);

  // For chat: store an array of chat messages with sender and text
  const [chatMessage, setChatMessage] = useState<string>('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  // For swarm
  const [swarmQuery, setSwarmQuery] = useState<string>('');

  // -------------------------
  // 2. Load Initial Courses from Backend
  // -------------------------
  useEffect(() => {
    async function fetchInitialCourses() {
      try {
        const res = await fetch('/filter_state');
        const data = await res.json();
        // Expecting backend to return { columns: [...], courses: [...] }
        if (data.columns) setColumns(data.columns);
        if (data.courses) setCourses(data.courses);
      } catch (error) {
        console.error('Error fetching initial courses:', error);
      }
    }
    fetchInitialCourses();
  }, []);

  // -------------------------
  // 3. Handle Interactive Chat (Mode=1)
  // -------------------------
  const handleChatSubmit = async () => {
    if (!chatMessage.trim()) return;

    try {
      const response = await fetch('/interactive_chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: chatMessage }),
      });
      const data = await response.json();

      if (data.error) {
        console.error(data.error);
        return;
      }
      if (data.message === 'User requested exit') {
        console.log('User requested exit');
      }

      // Update chat history: add user's message and bot's response as separate entries
      setChatHistory(prev => [
        ...prev,
        { sender: 'user', text: chatMessage },
        { sender: 'bot', text: data.response }
      ]);

      // Update the columns and courses from the filter state
      if (data.columns) setColumns(data.columns);
      if (data.courses) setCourses(data.courses);

      // Clear the chat input
      setChatMessage('');
    } catch (error) {
      console.error('Error in handleChatSubmit:', error);
    }
  };

  // -------------------------
  // 4. Handle Agentic Swarm (Mode=2)
  // -------------------------
  const handleSwarmSubmit = async () => {
    if (!swarmQuery.trim()) return;

    try {
      const response = await fetch('/agentic_swarm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: swarmQuery }),
      });
      const data = await response.json();

      if (data.error) {
        console.error(data.error);
        return;
      }
      if (data.message === 'User requested exit') {
        console.log('User requested exit');
      }

      // Add a new column called "Swarm Answer" if not already present
      const newColumnName = 'Swarm Answer';
      if (!columns.includes(newColumnName)) {
        setColumns(prev => [...prev, newColumnName]);
      }

      // Merge the swarm results into each course object
      // Assuming data.results is an object with keys as course id
      const updatedCourses = courses.map(course => {
        const courseId = course.id;
        const swarmAnswer = data.results && data.results[courseId] ? data.results[courseId] : '';
        return { ...course, swarmAnswer };
      });

      setCourses(updatedCourses);
      setSwarmQuery('');
    } catch (error) {
      console.error('Error in handleSwarmSubmit:', error);
    }
  };

  // -------------------------
  // 5. Render
  // -------------------------
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Top bar for Swarm Query */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Wharton Courses
          </Typography>
          <TextField
            variant="outlined"
            size="small"
            placeholder="Agentic Swarm Query..."
            value={swarmQuery}
            onChange={(e) => setSwarmQuery(e.target.value)}
            sx={{ backgroundColor: 'white', borderRadius: 1, marginRight: 1 }}
          />
          <Button variant="contained" color="secondary" onClick={handleSwarmSubmit}>
            Swarm
          </Button>
        </Toolbar>
      </AppBar>

      <Box sx={{ display: 'flex', flex: 1 }}>
        {/* Left Chat Panel */}
        <Box
          sx={{
            width: 300,
            borderRight: '1px solid #ccc',
            padding: 2,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Typography variant="subtitle1" gutterBottom>
            Interactive Chat
          </Typography>
          <Paper
            variant="outlined"
            sx={{
              flex: 1,
              overflowY: 'auto',
              marginBottom: 2,
              padding: 1
            }}
          >
            {chatHistory.map((msg, idx) => (
              <Box
                key={idx}
                sx={{
                  marginBottom: 1,
                  textAlign: msg.sender === 'user' ? 'right' : 'left',
                }}
              >
                <Typography
                  variant="body2"
                  sx={{
                    display: 'inline-block',
                    padding: '6px 10px',
                    borderRadius: '12px',
                    backgroundColor: msg.sender === 'user' ? '#1976d2' : '#e0e0e0',
                    color: msg.sender === 'user' ? 'white' : 'black'
                  }}
                >
                  {msg.text}
                </Typography>
              </Box>
            ))}
          </Paper>
          <Box sx={{ display: 'flex' }}>
            <TextField
              variant="outlined"
              size="small"
              fullWidth
              placeholder="Type your message..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
            />
            <Button variant="contained" onClick={handleChatSubmit} sx={{ marginLeft: 1 }}>
              Send
            </Button>
          </Box>
        </Box>

        {/* Center Table for Courses */}
        <Box sx={{ flex: 1, padding: 2, overflow: 'auto' }}>
          <Table>
            <TableHead>
              <TableRow>
                {columns.map((col) => (
                  <TableCell key={col}>{col}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {courses.map((course, idx) => (
                <TableRow key={idx}>
                  {columns.map((col) => {
                    // For 'Swarm Answer', we expect course.swarmAnswer; otherwise, display course id or name
                    const cellValue =
                      col === 'Swarm Answer'
                        ? course.swarmAnswer || ''
                        : course[col] || '';
                    return <TableCell key={col}>{cellValue}</TableCell>;
                  })}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </Box>
    </Box>
  );
}

export default App;