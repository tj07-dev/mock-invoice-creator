# Mock Invoice Creator

A Flask-based web application for generating mock invoices with a futuristic **cyberpunk aesthetic**. Create custom invoices or generate random ones with various templates (e.g., simple, professional, Uber receipt, utility bill) and download them as PDFs. The app features a neon-drenched UI with glitch effects, glowing shadows, and a dark dystopian vibe.

## Features

- **Custom Invoices**: Input customer details, items, and tax rates to create tailored invoices.
- **Random Generation**: Generate random invoices with realistic mock data from a JSON file.
- **Templates**: Choose from multiple invoice designs (simple, modern, elegant, corporate, Uber receipt, utility bill).
- **Cyberpunk Theme**: Neon gradients, glitch animations, and a dark, futuristic layout.
- **Previews**: Toggleable design previews with lazy-loaded PDFs.
- **Responsive**: Works across desktop, tablet, and mobile devices.

## Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **pip**: Python package manager (comes with Python).
- **Git**: Optional, for cloning the repository.

## Setup Instructions

### 1. Clone the Repository (Optional)

If you have the project in a Git repository:

```bash
git clone https://github.com/tj07-dev/mock-invoice-creator.git
cd mock-invoice-creator
```

Alternatively, create a new directory and copy the project files into it.

### 2. Create a Virtual Environment

Set up a Python virtual environment to isolate dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

You’ll see `(venv)` in your terminal prompt when activated.

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install flask faker reportlab
```

- **Flask**: Web framework for the app.
- **Faker**: Generates realistic mock data.
- **ReportLab**: Creates PDF invoices.

### 4. Project Structure

Ensure your project directory looks like this:

```
mock-invoice-creator/
├── app.py              # Main Flask application
├── mock_data.json      # Mock data for invoices
├── static/             # Static files (generated PDFs, previews)
│   ├── previews/       # Pre-generated template previews
│   └── (generated PDFs)
├── templates/          # HTML templates
│   └── index.html      # Main UI with cyberpunk theme
└── README.md           # This file
```

### 5. Configure the App

- **mock_data.json**: Contains company info, product categories, Uber ride data, and utility bill data. Edit this file to customize mock data:
  - Update `company_info` with your business details.
  - Add or modify `product_categories` for custom items.
  - Adjust `uber_ride_data` or `utility_bill_data` for special templates.

No additional configuration is required unless you want to change ports or static file paths in `app.py`.

### 6. Run the Application

Start the Flask app:

```bash
python app.py
```

- The app will generate preview PDFs in `static/previews/` on startup.
- Open your browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Access the App**:

   - Visit `http://127.0.0.1:5000/` in your browser.

2. **Create a Custom Invoice**:

   - Fill in the form fields (invoice number, date, customer details, tax rate).
   - Add items by clicking "Add Item" and entering item details.
   - Select a template from the dropdown (e.g., "simple", "uber_receipt").
   - Click "Generate PDF Invoice" to download the PDF.

3. **Generate a Random Invoice**:

   - Select a template.
   - Click "Generate Random PDF Invoice" to download a PDF with mock data.

4. **View Previews**:

   - Click "Show Design Previews" to toggle the preview section.
   - Hover over previews for a neon glow effect; click links to open PDFs in a new tab.

5. **Exit the App**:
   - Stop the server with `Ctrl+C` in the terminal.
   - Deactivate the virtual environment:
     ```bash
     deactivate
     ```

## Configuration Options

- **Templates**: Add new templates by updating `TEMPLATES` in `app.py` and defining their PDF layouts in `create_invoice()`.
- **Mock Data**: Modify `mock_data.json` to change company details, product lists, or special invoice data.
- **Port**: Change the Flask port in `app.py` by adding `app.run(debug=True, port=5001)` if 5000 is in use.
- **Static Files**: Adjust `static/` paths in `app.py` if you relocate the folder.

## Troubleshooting

- **Dependencies Fail**: Ensure `pip` is up-to-date (`pip install --upgrade pip`) and re-run the install command.
- **PDFs Not Generating**: Check write permissions in `static/` and ensure `reportlab` is installed.
- **Previews Missing**: Verify `static/previews/` exists and was populated on startup.
- **Port Conflict**: Change the port in `app.py` if 5000 is occupied.

## Customization

- **Cyberpunk Theme**: Edit `index.html` CSS to tweak neon colors (e.g., `#00ffcc` to `#ff0066`), animation speeds, or glitch effects.
- **New Templates**: Extend `TEMPLATES` and `create_invoice()` in `app.py` for custom designs.
- **Data**: Expand `mock_data.json` with new categories or items.

## License

This project is open-source under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute it!
