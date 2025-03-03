[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rqkun-voidpet.streamlit.app/)
[![GPL License][license-shield]][license-url]
# Void Pet 

A Python-based **Streamlit** application that utilizes the **Warframe Status API** and the **Warframe.market API** to provide up-to-date information on in-game events, vendor inventories, and market pricing.

Checkout the website [here](https://rqkun-voidpet.streamlit.app/)

---

## Features

- **In-Game Event Tracking**: Stay updated with current and upcoming events in Warframe.
- **Vendor Inventory Lookup**: View the latest inventory of in-game vendors like Baro Ki'Teer.
- **Market Price Checkup**: Check real-time market prices for items, including seller information and availability.
- **News Updates**: Check news, stream announcements, updates.
- **Riven mods Auction Checkup**: Check real-time market prices for rivens, including auctions and buyouts.
- **User-Friendly Interface**: Built with Streamlit for an intuitive, lightweight, and responsive user experience.
- **Discord Bot Integration**: Run a bot for integrating with Discord.

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

3. Update the required export files:

   ```bash
   python3 ./utils/local_manifest_update.py
   ```

4. Insert discord credentials in the `./streamlit/secrets.toml`
   ```
   [discord]
   key="<your-bot-secret-key>"
   [host]
   local = "http://localhost:8501/"
   cloud = "<your-host-here>" #remember to add the "/" at the end. Ex: https://rqkun-voidpet.streamlit.app/
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
   - Check out items market prices.

---

## Project Structure

```plaintext
void-pet/
├── app.py              # Main application file
├── components/         # Reusable UI components
├── config/             # Constants
├── datasources/        # Data related files 
    ├── images/         # Static image files
    └── exports/        # Downloaded JSON Exports
├── utils/              # Utility functions
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
└── ...
```

---

## APIs Used

1. **[Warframe Stat API](https://docs.warframestat.us/)**:
   - Provides data on in-game events, alerts and vendors.

2. **[Warframe.market API](https://warframe.market/api_docs/)**:
   - Enables retrieval of real-time item prices and market trends.

3. **[Discord](https://discord.com/developers/docs/intro)**
   - Enables Discord bot hooks.
---

## License

Distributed under the MIT License. See LICENSE for more information.

---

## Acknowledgments

- **Warframe Status API** and **Warframe.market API** for making data accessible.
- **Discord** for making ease of access to their bot features.
- The Warframe community for their support and feedback.

---
