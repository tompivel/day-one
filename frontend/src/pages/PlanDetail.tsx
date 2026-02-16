import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Container, Typography, Card, CardContent, CardActionArea, Fab,
    Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button, Breadcrumbs, Link, Grid
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { getMacrocycles, createMacrocycle } from '../api/macrocycles';
import type { Macrocycle } from '../api/macrocycles';

const PlanDetail: React.FC = () => {
    const { planId } = useParams<{ planId: string }>();
    const navigate = useNavigate();
    const [macrocycles, setMacrocycles] = useState<Macrocycle[]>([]);
    const [isCreating, setIsCreating] = useState(false);
    const [newMacroName, setNewMacroName] = useState('');

    useEffect(() => {
        if (planId) {
            loadMacrocycles(parseInt(planId));
        }
    }, [planId]);

    const loadMacrocycles = async (id: number) => {
        try {
            const data = await getMacrocycles(id);
            setMacrocycles(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleCreateMacrocycle = async () => {
        if (!planId || !newMacroName) return;
        try {
            await createMacrocycle(parseInt(planId), newMacroName);
            setIsCreating(false);
            setNewMacroName('');
            loadMacrocycles(parseInt(planId));
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
                <Link underline="hover" color="inherit" onClick={() => navigate('/dashboard')} sx={{ cursor: 'pointer' }}>
                    Dashboard
                </Link>
                <Typography color="text.primary">Plan {planId}</Typography>
            </Breadcrumbs>

            <Typography variant="h4" gutterBottom>
                Macrocycles
            </Typography>

            <Grid container spacing={3}>
                {macrocycles.map((macro) => (
                    <Grid size={{ xs: 12, sm: 6, md: 4 }} key={macro.id}>
                        <Card>
                            <CardActionArea onClick={() => navigate(`/macrocycles/${macro.id}`)}>
                                <CardContent>
                                    <Typography variant="h6" component="div">
                                        {macro.name}
                                    </Typography>
                                </CardContent>
                            </CardActionArea>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Fab color="primary" aria-label="add" sx={{ position: 'fixed', bottom: 16, right: 16 }} onClick={() => setIsCreating(true)}>
                <AddIcon />
            </Fab>

            <Dialog open={isCreating} onClose={() => setIsCreating(false)}>
                <DialogTitle>New Macrocycle</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Name"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={newMacroName}
                        onChange={(e) => setNewMacroName(e.target.value)}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsCreating(false)}>Cancel</Button>
                    <Button onClick={handleCreateMacrocycle}>Create</Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
};

export default PlanDetail;
