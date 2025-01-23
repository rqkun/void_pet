[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rqkun-voidpet.streamlit.app/)
# Void Pet 

A Python-based **Streamlit** application that utilizes the **Warframe Status API** and the **Warframe.market API** to provide up-to-date information on in-game events, vendor inventories, and market pricing.

Checkout the website [here](https://rqkun-voidpet.streamlit.app/)

---

## Features

- **In-Game Event Tracking**: Stay updated with current and upcoming events in Warframe. (WIP)
- **Vendor Inventory Lookup**: View the latest inventory of in-game vendors like Baro Ki'Teer.
- **Market Price Analysis**: Check real-time market prices for items, including trends and availability.
- **User-Friendly Interface**: Built with Streamlit for an intuitive, lightweight, and responsive user experience.

---

## Getting Started

Follow these steps to set up and run the project locally:

### Prerequisites

Ensure you have the following installed:

- Python 3.9+
- pip (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rqkun/void_pet.git
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open the application in your web browser at `http://localhost:8501`.

3. Use the provided interface to:
   - View live in-game events.
   - Check vendor inventories.
   - From vendor inventories, check out item details and view their market prices.

---

## Project Structure

```plaintext
void-pet/
├── app.py              # Main application file
├── components/         # Reusable UI components
├── config/             # Constants
├── datasources/        # Static Files
    ├── images/         # Static image files
    └── exports/        # Downloaded JSON Exports
├── utils/              # Utility functions
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## APIs Used

1. **[Warframe Status API](https://docs.warframestat.us/)**:
   - Provides data on in-game events, alerts, and fissures.

2. **[Warframe.market API](https://warframe.market/)**:
   - Enables retrieval of real-time item prices and market trends.

---

## Acknowledgments

- **Warframe Status API** and **Warframe.market API** for making data accessible.
- The Warframe community for their support and feedback.

---
