# 🌍 Itinera – AI Travel Planner

> **Plan smarter. Travel better. Powered by AI.**

Itinera is an AI-powered travel planning application that generates personalized travel recommendations and detailed itineraries based on a user's interests, budget, trip duration, and destination. The application combines a content-based recommendation engine with Google's Gemini AI to help travelers discover attractions and plan memorable trips efficiently.

---

## ✨ Features

- 🎯 Personalized attraction recommendations
- 🤖 AI-generated day-wise travel itineraries
- 💰 Budget-aware trip planning
- 📍 Destination filtering by city and interests
- ⭐ Student-friendly attraction ranking
- 📊 Estimated trip cost calculation
- 📄 Download AI-generated itinerary
- 🖥️ Interactive Streamlit web interface

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity

### AI
- Google Gemini API

### Data Processing
- Pandas
- NumPy

### Dataset
- Indian Tourist Attractions Dataset (Processed)

---

## 📂 Project Structure

```text
Itinera/
│
├── data/
│   └── processed_travel_dataset.csv
│
├── recommender.py
├── trip_planner.py
├── itinerary_generator.py
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ How It Works

### Step 1 — User Input

The user selects:

- Destination City
- Budget
- Trip Duration
- Interest
  - Historical
  - Religious
  - Nature
  - Adventure
  - Wildlife
  - Beach
  - Museum

---

### Step 2 — Recommendation Engine

The system filters attractions using:

- TF-IDF Vectorization
- Cosine Similarity
- Student Score
- Budget Constraints

---

### Step 3 — Trip Planning

The planner:

- Selects suitable attractions
- Estimates total trip cost
- Calculates remaining budget

---

### Step 4 — AI Itinerary Generation

The selected attractions are converted into a detailed prompt and sent to **Google Gemini AI**, which generates:

- Day-wise itinerary
- Budget breakdown
- Food recommendations
- Transport suggestions
- Student travel tips

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/Itinera.git

cd Itinera
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Create `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Get your free Gemini API key from:

https://aistudio.google.com/app/apikey

---

### Run the Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots
<img width="1532" height="701" alt="image" src="https://github.com/user-attachments/assets/ecd39e6c-8e8d-4c35-a721-b46754b24e60" />

---

## 📊 Recommendation Algorithm

The recommendation engine uses **Content-Based Filtering**.

It compares attraction tags using **TF-IDF Vectorization** and **Cosine Similarity** to recommend destinations with similar characteristics.

Additional ranking factors include:

- Student Score
- Budget
- Entrance Fee
- Attraction Type

---

## 🤖 AI Integration

Google Gemini AI is used to generate personalized travel itineraries.

The generated itinerary includes:

- Daily travel schedule
- Estimated expenses
- Food recommendations
- Transport options
- Travel tips

---

## 📈 Future Enhancements

- 🗺️ Interactive route mapping
- 📍 Live GPS integration
- 🌦️ Weather forecasting
- 🚆 Real-time transport suggestions
- 🏨 Hotel recommendations
- 🍽️ Restaurant recommendations
- 💬 Multilingual support
- ❤️ Save favorite trips
- 📱 Mobile application

---

## 🎯 Use Cases

- Students
- Solo Travelers
- Family Trips
- Budget Travelers
- Weekend Getaways
- College Projects

---

## 📚 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | Frontend |
| Pandas | Data Processing |
| Scikit-learn | Recommendation Engine |
| Google Gemini | AI Itinerary Generation |
| TF-IDF | Feature Extraction |
| Cosine Similarity | Similarity Measurement |

---

## 👨‍💻 Author

**Arushi Bakshi**

Feel free to connect and contribute!

---


## 📄 License

This project is intended for educational and learning purposes.
