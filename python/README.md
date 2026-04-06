# Habit Tracker

A simple full-stack habit tracking app for building daily consistency. The backend exposes a REST API for managing habits, streaks, badges, and summary stats, while the frontend provides a lightweight browser UI for tracking progress.

## Features

- Create and delete habits
- Mark habits as completed for the day
- Track current and best streaks
- View habit statistics
- Unlock achievement badges based on progress
- Responsive frontend with a modal form for adding habits

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Node.js, Express
- Database: MongoDB with Mongoose
- Utilities: CORS, dotenv

## Project Structure

```text
habit-tracker/
├── backend/
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── README.md
```

## Prerequisites

- Node.js 18+ recommended
- MongoDB running locally on `mongodb://localhost:27017`
- A browser to open the frontend

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd habit-tracker
```

### 2. Install backend dependencies

```bash
cd backend
npm install
```

### 3. Start MongoDB

Make sure MongoDB is running locally. The backend connects to:

```text
mongodb://localhost:27017/habit-tracker
```

### 4. Start the backend server

```bash
npm start
```

By default, the API runs on `http://localhost:5000`.

### 5. Open the frontend

Open `frontend/index.html` directly in a browser, or serve the `frontend/` folder with a local static server such as VS Code Live Server.

## API Endpoints

Base URL: `http://localhost:5000/api`

- `GET /habits` - Fetch all habits
- `POST /habits` - Create a new habit
- `PATCH /habits/:id/complete` - Mark a habit as completed for today
- `DELETE /habits/:id` - Delete a habit
- `GET /badges` - Fetch all badges
- `PATCH /badges/:id` - Update badge unlock status
- `GET /stats` - Fetch habit summary statistics

### Health Check

- `GET /` - Basic API status response

## Notes

- Default badges are created automatically the first time the backend starts with an empty badge collection.
- The frontend currently uses a local API base URL, so it is intended for local development unless you update `frontend/script.js`.
- The calendar view in the UI is currently decorative and not yet synced to actual completion history.

## Future Improvements

- Add user authentication
- Persist and render real calendar heatmap data
- Add environment-based configuration for the API URL and MongoDB connection
- Add automated tests and deployment setup
