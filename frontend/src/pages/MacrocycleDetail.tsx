import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Container, Typography, Card, CardContent, CardActionArea, Fab,
    Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button, Breadcrumbs, Link, Grid
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { getMicrocycles, createMicrocycle } from '../api/microcycles';
import type { Microcycle } from '../api/microcycles';

const MacrocycleDetail: React.FC = () => {
    const { macrocycleId } = useParams<{ macrocycleId: string }>();
    const navigate = useNavigate();
    const [microcycles, setMicrocycles] = useState<Microcycle[]>([]);
    const [isCreating, setIsCreating] = useState(false);
    const [newMicroName, setNewMicroName] = useState('');

    useEffect(() => {
        if (macrocycleId) {
            loadMicrocycles(parseInt(macrocycleId));
        }
    }, [macrocycleId]);

    const loadMicrocycles = async (id: number) => {
        try {
            const data = await getMicrocycles(id);
            setMicrocycles(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleCreateMicrocycle = async () => {
        if (!macrocycleId || !newMicroName) return;
        try {
            await createMicrocycle(parseInt(macrocycleId), newMicroName);
            setIsCreating(false);
            setNewMicroName('');
            loadMicrocycles(parseInt(macrocycleId));
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
                <Typography color="text.primary">Macrocycle {macrocycleId}</Typography>
            </Breadcrumbs>

            <Typography variant="h4" gutterBottom>
                Microcycles
            </Typography>

            <Grid container spacing={3}>
                {microcycles.map((micro) => (
                    <Grid size={{ xs: 12, sm: 6, md: 4 }} key={micro.id}>
                        <Card>
                            <CardActionArea onClick={() => navigate(`/microcycles/${micro.id}`)}>
                                <CardContent>
                                    <Typography variant="h6" component="div">
                                        {micro.name}
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
                <DialogTitle>New Microcycle</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Name"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={newMicroName}
                        onChange={(e) => setNewMicroName(e.target.value)}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setIsCreating(false)}>Cancel</Button>
                    <Button onClick={handleCreateMicrocycle}>Create</Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
};

export default MacrocycleDetail;
