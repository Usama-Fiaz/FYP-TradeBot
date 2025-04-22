# FYP-TradeBot

A sophisticated Forex Trading Bot that combines machine learning predictions with sentiment analysis for automated trading decisions.

![Authentication Background](https://i.ibb.co/nrQYCVC/authentication-bg.jpg)

## Demo Video
[Watch the Demo](https://drive.google.com/file/d/1DXq7jF5JqbEvCWVBkcpkmKn-HJHmL9Os/view?usp=drive_link)

## Features

### 1. Machine Learning Predictions
- LSTM-based price prediction models for multiple currency pairs
- Predictions for Open, High, Low, and Close prices
- Historical data analysis and pattern recognition
- 10-day lookback window for accurate predictions

### 2. Sentiment Analysis
- Real-time news sentiment analysis using FinBERT
- Twitter sentiment analysis for market trends
- Automated news and tweet fetching
- MongoDB storage for historical sentiment data
- Support for multiple currency pairs:
  - EUR/USD
  - GBP/USD
  - USD/JPY
  - AUD/USD
  - EUR/GBP
  - USD/CAD
  - USD/CHF
  - NZD/CHF

### 3. Trading Features
- Manual trading interface
- Automated trading based on predictions
- Trading history tracking
- Real-time order placement
- Volume control for trades
- Multiple trading modes

### 4. Data Visualization
- Interactive live charts
- Historical price data visualization
- Sentiment analysis charts
- Multiple chart types and timeframes
- Real-time market data updates

### 5. User Interface
- Modern, responsive dashboard
- Authentication system
- Wallet management
- Trading history view
- News feed integration
- Tweet analysis view
- Prediction results display

### 6. Technical Features
- Flask backend with RESTful API
- React frontend with modern UI components
- MongoDB Atlas for data storage
- Real-time data processing
- Automated data fetching and analysis
- Background scheduling for data updates

## Project Structure
- `frontend/`: React-based user interface
- `flasktest/`: Backend server and API
- `LSTM Prediction Model/`: Machine learning models and predictions

## Technologies Used
- Frontend: React.js
- Backend: Flask (Python)
- Database: MongoDB Atlas
- Machine Learning: TensorFlow, LSTM
- NLP: FinBERT, NLTK
- Data Processing: Pandas, NumPy
- Visualization: Matplotlib, Chart.js

## Getting Started
[Add installation and setup instructions here]

## License
[Add license information here]

Welcome to the trading bot web application! This application allows users to make automated trades in the financial markets using artificial intelligence.

The bot uses a combination of machine learning algorithms and natural language processing techniques to analyze various market influencing factors, including tweets, news articles, and technical indicator data. It then uses this analysis to make smart market predictions and execute trades on behalf of the user.

With this application, users can take advantage of the power of AI to make informed and profitable trades, without the need for extensive market analysis and manual trade execution.

## Demo Video Link

https://drive.google.com/file/d/1DXq7jF5JqbEvCWVBkcpkmKn-HJHmL9Os/view?usp=drive_link

## Installation 

To run the project in development

```bash
  npm i --legacy-peer-deps
```

```bash
  npm start
```

To build and deploy

```bash
  npm run build
```

## Technology Stack

The trading bot web application is built using a modern and powerful technology stack that allows for efficient development and reliable performance.

At the frontend, we have used React and Redux to build a interactive and responsive user interface. We have also used the Fetch API to communicate with the backend server and retrieve data in a seamless and efficient manner. For styling and UI components, we have utilized Bootstrap and React-strap to give the application a professional and polished look.

On the backend, we have implemented a Flask RESTful API server to handle requests from the frontend and communicate with the trading bot. Flask is a lightweight Python web framework that is easy to set up and customize, making it a great choice for this application.

Overall, the combination of React, Redux, and Flask allows us to build a powerful and scalable web application for automated trading with artificial intelligence.

## Architecture Diagram

![alt text](https://i.ibb.co/2gDybBK/Mac-Book-Air-2.jpg)