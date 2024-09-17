const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();

// CORS'u aktif et
app.use(cors());

// Binance API'den veri çekme
app.get('/api/data', async (req, res) => {
    try {
        const response = await axios.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
        res.json(response.data);
    } catch (error) {
        res.status(500).send('Error fetching data');
    }
});

// 5000 portunda çalıştır
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
