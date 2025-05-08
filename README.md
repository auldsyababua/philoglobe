# Philosophy Globe

This project aims to parse a philosophy textbook to create JSON objects that conform to a specified schema. These JSON objects will be used to create an interactive Google Earth timeline web app to visualize the migration of philosophical ideas over time.

## Setup

1. **Clone the Repository**
   ```bash
   git clone git@github.com:auldsyababua/philoglobe.git
   cd philoglobe
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Extract Text from EPUB**
   
   Run the script to extract text from the EPUB file:
   ```bash
   python3 extract_epub.py
   ```

2. **Check Outputs**

   JSON files will be generated in the `outputs` directory.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. 