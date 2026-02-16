import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Container, Typography, Box, Fab,
    Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button,
    List, ListItem, ListItemText, Divider, Slider, InputLabel, Select, MenuItem, FormControl
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { getSessions, createSession } from '../api/sessions';
import type { Session } from '../api/sessions';

const MicrocycleDetail: React.FC = () => {
    const { microcycleId } = useParams<{ microcycleId: string }>();
    const navigate = useNavigate();
    const [sessions, setSessions] = useState<Session[]>([]);
    const [isLogging, setIsLogging] = useState(false);

    // Form State
    const [sport, setSport] = useState('Running');
    const [dateStart, setDateStart] = useState('');
    const [duration, setDuration] = useState(0);
    const [rpe, setRpe] = useState(5);
    const [description, setDescription] = useState('');

    useEffect(() => {
        if (microcycleId) {
            loadSessions(parseInt(microcycleId));
        }
    }, [microcycleId]);

    const loadSessions = async (id: number) => {
        try {
            const data = await getSessions(id);
            setSessions(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleLogSession = async () => {
        if (!microcycleId) return;
        try {
            await createSession(parseInt(microcycleId), {
                sport,
                date_start: new Date(dateStart).toISOString(),
                duration_minutes: duration,
                perceived_exertion: rpe,
                description
            });
            setIsLogging(false);
            resetForm();
            loadSessions(parseInt(microcycleId));
        } catch (err) {
            console.error(err);
        }
    };

    const resetForm = () => {
        setSport('Running');
        setDateStart('');
        setDuration(0);
        setRpe(5);
        setDescription('');
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Box sx={{ mb: 2 }}>
                <Button onClick={() => navigate(-1)}>Back</Button>
            </Box>
            <Typography variant="h4" gutterBottom>
                Sessions
            </Typography>

            <List>
                {sessions.map((session) => (
                    <React.Fragment key={session.id}>
                        <ListItem alignItems="flex-start">
                            <ListItemText
                                primary={`${session.sport} - ${new Date(session.date_start).toLocaleString()}`}
                                secondary={
                                    <React.Fragment>
                                        <Typography
                                            sx={{ display: 'inline' }}
                                            component="span"
                                            variant="body2"
                                            color="text.primary"
                                        >
                                            {session.duration_minutes} mins | RPE: {session.perceived_exertion}/10
                                        </Typography>
                                        {" — " + session.description}
                                    </React.Fragment>
                                }
                            />
                        </ListItem>
                        <Divider variant="inset" component="li" />
                    </React.Fragment>
                ))}
            </List>

            <Fab color="primary" aria-label="add" sx={{ position: 'fixed', bottom: 16, right: 16 }} onClick={() => setIsLogging(true)}>
                <AddIcon />
            </Fab>

            <Dialog open={isLogging} onClose={() => setIsLogging(false)} maxWidth="sm" fullWidth>
                <DialogTitle>Log Session</DialogTitle>
                <DialogContent>
                    <FormControl fullWidth margin="dense">
                        <InputLabel id="sport-label">Sport</InputLabel>
                        <Select
                            labelId="sport-label"
                            value={sport}
                            label="Sport"
                            onChange={(e) => setSport(e.target.value)}
                        >
                            <MenuItem value="Running">Running</MenuItem>
                            <MenuItem value="Cycling">Cycling</MenuItem>
                            <MenuItem value="Swimming">Swimming</MenuItem>
                            <MenuItem value="Strength">Strength</MenuItem>
                        </Select>
                    </FormControl>
                    <TextField
                        margin="dense"
                        id="date"
                        label="Date & Time"
                        type="datetime-local"
                        fullWidth
                        variant="outlined"
                        InputLabelProps={{ shrink: true }}
                        value={dateStart}
                        onChange={(e) => setDateStart(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="duration"
                        label="Duration (minutes)"
                        type="number"
                        fullWidth
                        variant="outlined"
                        value={duration}
                        onChange={(e) => setDuration(parseInt(e.target.value))}
                    />
                    <Typography gutterBottom sx={{ mt: 2 }}>RPE (1-10)</Typography>
                    <Slider
                        value={rpe}
                        onChange={(_, val) => setRpe(val as number)}
                        step={1}
                        marks
                        min={1}
                        max={10}
                        valueLabelDisplay="auto"
                    />
                    <TextField
                        margin="dense"
                        id="description"
                        label="Description"
                        type="text"
                        fullWidth
                        multiline
                        rows={4}
                        variant="outlined"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsLogging(false)}>Cancel</Button>
                    <Button onClick={handleLogSession}>Log</Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
};

export default MicrocycleDetail;
