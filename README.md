# YouTube Scraper

## Project Overview

YouTube Scraper is a web application that allows users to fetch details of the first 5 videos from a specified YouTube channel using the YouTube Data API. The details fetched include video length, title, and other metadata.

## How It Works

1. **API Key**: Users need to enter their YouTube API key, which can be obtained from the Google Developer Console.
2. **Channel Handle**: Enter the channel handle, which starts with "@" (e.g., @channelname).
3. **Data Fetching**: The program fetches details of the first 5 videos from the specified YouTube channel. The number of videos can be increased by modifying the code.

## Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Flask
- **API**: YouTube Data API
- **Deployment**: AWS (Beanstalk and CodePipeline)

## How to Set Up

1. **Install Requirements**:
   - Ensure you have Python installed.
   - Install required packages by running:
     ```sh
     pip install -r requirements.txt
     ```
2. **Run the Application**:
   - Start the application by running:
     ```sh
     python application.py
     ```

## Contributing

This project is open-source and free to use. Contributions and modifications are welcome. Feel free to fork the repository and make your changes.

## License

This project is licensed under the MIT License. You are free to use and modify the project as you please.

---

For any issues or questions, please contact the project maintainer.

Enjoy using the YouTube Scraper!