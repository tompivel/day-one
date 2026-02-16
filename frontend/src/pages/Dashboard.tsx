import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    AppBar, Toolbar, Typography, Button, Container, Card, CardContent,
    Fab, Dialog, DialogTitle, DialogContent, TextField, DialogActions, Box, Grid
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { useAuthStore } from '../store/useAuthStore';
import { getPlans, createPlan } from '../api/plans';
import type { Plan } from '../api/plans';
import { exportProfileData } from '../api/profiles';

const Dashboard: React.FC = () => {
    const { user, isAuthenticated, logout } = useAuthStore();
    const navigate = useNavigate();
    const [plans, setPlans] = useState<Plan[]>([]);
    const [isCreating, setIsCreating] = useState(false);
    const [newPlanTitle, setNewPlanTitle] = useState('');
    const [newPlanDescription, setNewPlanDescription] = useState('');

    useEffect(() => {
        if (!isAuthenticated || !user) {
            navigate('/');
            return;
        }
        loadPlans();
    }, [isAuthenticated, user, navigate]);

    const loadPlans = async () => {
        try {
            const allPlans = await getPlans();
            setPlans(allPlans);
        } catch (err) {
            console.error(err);
        }
    };

    const handleCreatePlan = async () => {
        if (!user || !newPlanTitle) return;
        try {
            await createPlan(user.id, newPlanTitle, newPlanDescription);
            setIsCreating(false);
            setNewPlanTitle('');
            setNewPlanDescription('');
            loadPlans();
        } catch (err) {
            console.error(err);
        }
    };

    const handleExport = async () => {
        if (!user) return;
        try {
            const data = await exportProfileData(user.id);
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `training_data_${user.username}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch (err) {
            console.error(err);
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Dashboard - {user?.username}
                    </Typography>
                    <Button color="inherit" onClick={handleExport}>Export</Button>
                    <Button color="inherit" onClick={handleLogout}>Logout</Button>
                </Toolbar>
            </AppBar>
            <Container sx={{ mt: 4 }}>
                <Grid container spacing={3}>
                    {plans.map((plan) => (
                        <Grid size={{ xs: 12, sm: 6, md: 4 }} key={plan.id}>
                            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', cursor: 'pointer' }} onClick={() => navigate(`/plans/${plan.id}`)}>
                                <CardContent sx={{ flexGrow: 1 }}>
                                    <Typography gutterBottom variant="h5" component="div">
                                        {plan.title}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {plan.description}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
                <Fab color="primary" aria-label="add" sx={{ position: 'fixed', bottom: 16, right: 16 }} onClick={() => setIsCreating(true)}>
                    <AddIcon />
                </Fab>
            </Container>

            <Dialog open={isCreating} onClose={() => setIsCreating(false)}>
                <DialogTitle>Create New Plan</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="title"
                        label="Plan Title"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={newPlanTitle}
                        onChange={(e) => setNewPlanTitle(e.target.value)}
                    />
                    <TextField
                        margin="dense"
                        id="description"
                        label="Description"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={newPlanDescription}
                        onChange={(e) => setNewPlanDescription(e.target.value)}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsCreating(false)}>Cancel</Button>
                    <Button onClick={handleCreatePlan}>Create</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default Dashboard;
