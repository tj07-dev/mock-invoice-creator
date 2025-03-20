import json
import os
import random

from faker import Faker
from flask import Flask, render_template, request, send_file, url_for
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
fake = Faker()

# Load mock data from JSON file
with open("mock_data.json", "r") as f:
    MOCK_DATA = json.load(f)

# Invoice templates
TEMPLATES = {
    "simple": "Clean and straightforward design.",
    "professional": "Structured and formal with detailed branding.",
    "modern": "Sleek, colorful, and contemporary.",
    "elegant": "Refined and luxurious with subtle sophistication.",
    "minimal": "Ultra-clean with a focus on essentials.",
    "corporate": "Bold and authoritative for business use.",
    "uber_receipt": "Uber Ride Receipt with a dynamic look.",
    "utility_bill": "Utility Bill with a clear, functional design.",
}


# Function to generate a realistic item
def generate_realistic_item(used_items=None):
    if used_items is None:
        used_items = set()
    category = random.choice(list(MOCK_DATA["product_categories"].keys()))
    available_items = [
        item
        for item in MOCK_DATA["product_categories"][category]
        if item not in used_items
    ]
    if not available_items:
        available_items = MOCK_DATA["product_categories"][category]
    item_name = random.choice(available_items)
    used_items.add(item_name)
    return {
        "name": item_name,
        "quantity": fake.random_int(min=1, max=5),
        "price": round(fake.random_number(digits=2) + fake.random.random(), 2),
    }


# Function to generate realistic random invoice data
def generate_random_invoice(template="simple"):
    if template == "uber_receipt":
        items = MOCK_DATA["uber_ride_data"]["items"]
        subtotal = sum(item["price"] for item in items)
        tax_rate = 8
        tax = subtotal * (tax_rate / 100)
        total = subtotal + tax
        return {
            "invoice_number": f"UBER-{fake.random_int(min=10000, max=99999)}",
            "date": fake.date_this_year().strftime("%Y-%m-%d"),
            "customer_name": fake.name(),
            "customer_address": fake.address().replace("\n", ", "),
            "customer_email": fake.email(),
            "items": [{**item, "quantity": 1} for item in items],
            "tax_rate": tax_rate,
            "total": total,
        }
    elif template == "utility_bill":
        items = MOCK_DATA["utility_bill_data"]["items"]
        subtotal = sum(item["price"] for item in items)
        tax_rate = 5
        tax = subtotal * (tax_rate / 100)
        total = subtotal + tax
        return {
            "invoice_number": f"UTIL-{fake.random_int(min=1000, max=9999)}",
            "date": fake.date_this_year().strftime("%Y-%m-%d"),
            "customer_name": fake.name(),
            "customer_address": fake.address().replace("\n", ", "),
            "customer_email": fake.email(),
            "items": [{**item, "quantity": 1} for item in items],
            "tax_rate": tax_rate,
            "total": total,
        }
    else:
        used_items = set()
        items = [
            generate_realistic_item(used_items)
            for _ in range(fake.random_int(min=2, max=4))
        ]
        subtotal = sum(item["quantity"] * item["price"] for item in items)
        tax_rate = fake.random_int(min=5, max=15)
        tax = subtotal * (tax_rate / 100)
        total = subtotal + tax
        return {
            "invoice_number": f"INV-{fake.random_int(min=1000, max=9999)}",
            "date": fake.date_this_year().strftime("%Y-%m-%d"),
            "customer_name": fake.company(),
            "customer_address": fake.address().replace("\n", ", "),
            "customer_email": fake.company_email(),
            "items": items,
            "tax_rate": tax_rate,
            "total": total,
        }


# Function to generate a PDF invoice
def create_invoice(filename, invoice_data, template="simple"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    if template == "simple":
        c.setFillColor(colors.lightgrey)
        c.rect(0, height - 60, width, 60, fill=True)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 40, "Invoice")
        c.setFont("Helvetica", 10)
        c.drawString(
            40,
            height - 75,
            f"{MOCK_DATA['company_info']['name']} | {MOCK_DATA['company_info']['phone']}",
        )
        c.drawString(40, height - 90, MOCK_DATA["company_info"]["address"])

    elif template == "professional":
        c.setFillColor(colors.darkblue)
        c.rect(0, height - 100, width, 100, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 40, "INVOICE")
        c.setFont("Helvetica", 12)
        c.drawString(40, height - 70, MOCK_DATA["company_info"]["name"])
        c.setFillColor(colors.lightgrey)
        c.rect(40, height - 95, width - 80, 20, fill=True)
        c.setFillColor(colors.black)
        c.drawString(
            45,
            height - 90,
            f"{MOCK_DATA['company_info']['address']} | {MOCK_DATA['company_info']['email']}",
        )

    elif template == "modern":
        c.setFillColor(colors.teal)
        c.rect(0, height - 120, width, 120, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width / 2, height - 50, "INVOICE")
        c.setFont("Helvetica", 12)
        c.drawString(40, height - 80, MOCK_DATA["company_info"]["name"])
        c.setFillColor(colors.black)
        c.drawString(
            40,
            height - 100,
            f"{MOCK_DATA['company_info']['phone']} | {MOCK_DATA['company_info']['email']}",
        )
        c.line(40, height - 105, width - 40, height - 105)

    elif template == "elegant":
        c.setFillColor(colors.black)
        c.rect(0, height - 80, width, 80, fill=True)
        c.setFillColor(colors.gold)
        c.setFont("Times-Bold", 22)
        c.drawCentredString(width / 2, height - 50, "Invoice")
        c.setFillColor(colors.black)
        c.setFont("Times-Roman", 12)
        c.drawString(40, height - 100, MOCK_DATA["company_info"]["name"])
        c.drawString(40, height - 115, MOCK_DATA["company_info"]["address"])
        c.setStrokeColor(colors.gold)
        c.setLineWidth(1)
        c.line(40, height - 120, width - 40, height - 120)

    elif template == "minimal":
        c.setFont("Helvetica", 16)
        c.drawString(40, height - 40, "Invoice")
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 60, MOCK_DATA["company_info"]["name"])
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(40, height - 65, width - 40, height - 65)

    elif template == "corporate":
        c.setFillColor(colors.navy)
        c.rect(0, height - 90, width, 90, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(width / 2, height - 50, "INVOICE")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)
        c.drawString(
            40,
            height - 80,
            f"{MOCK_DATA['company_info']['name']} - {MOCK_DATA['company_info']['phone']}",
        )
        c.drawString(40, height - 95, MOCK_DATA["company_info"]["address"])
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.line(40, height - 100, width - 40, height - 100)

    elif template == "uber_receipt":
        c.setFillColor(colors.black)
        c.rect(0, height - 100, width, 100, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 40, "UBER RECEIPT")
        c.setFillColor(colors.grey)
        c.rect(40, height - 85, width - 80, 20, fill=True)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)
        c.drawString(
            45,
            height - 80,
            f"{MOCK_DATA['uber_ride_data']['name']} | {MOCK_DATA['uber_ride_data']['email']}",
        )

    elif template == "utility_bill":
        c.setFillColor(colors.darkgreen)
        c.rect(0, height - 90, width, 90, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width / 2, height - 50, "UTILITY BILL")
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)
        c.drawString(40, height - 75, MOCK_DATA["utility_bill_data"]["name"])
        c.drawString(
            40,
            height - 90,
            f"{MOCK_DATA['utility_bill_data']['address']} | {MOCK_DATA['utility_bill_data']['email']}",
        )

    # Invoice details
    c.setFont("Helvetica", 12)
    details_y = height - 160
    c.drawString(40, details_y, f"Invoice #: {invoice_data['invoice_number']}")
    c.drawString(40, details_y - 15, f"Date: {invoice_data['date']}")
    c.drawString(40, details_y - 40, "Bill To:")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, details_y - 55, invoice_data["customer_name"])
    c.setFont("Helvetica", 10)
    c.drawString(60, details_y - 70, invoice_data["customer_address"])
    c.drawString(60, details_y - 85, invoice_data["customer_email"])

    # Items table
    c.setFillColor(colors.lightgrey)
    c.rect(40, details_y - 110, width - 80, 20, fill=True)
    headers = ["Item", "Qty", "Price", "Total"]
    x_positions = [50, 250, 350, 450]
    y = details_y - 100
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y, header)

    y -= 20
    c.setFont("Helvetica", 11)
    for item in invoice_data["items"]:
        c.drawString(x_positions[0], y, item["name"])
        c.drawString(x_positions[1], y, str(item["quantity"]))
        c.drawString(x_positions[2], y, f"${item['price']:.2f}")
        c.drawString(x_positions[3], y, f"${item['quantity'] * item['price']:.2f}")
        y -= 15

    # Totals box
    subtotal = sum(item["quantity"] * item["price"] for item in invoice_data["items"])
    tax = subtotal * (invoice_data["tax_rate"] / 100)
    total = subtotal + tax
    y -= 20
    c.setFillColor(colors.whitesmoke)
    c.rect(width - 210, y - 60, 170, 60, fill=True)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    c.drawString(width - 200, y - 15, "Subtotal:")
    c.drawString(width - 100, y - 15, f"${subtotal:.2f}")
    c.drawString(width - 200, y - 30, f"Tax ({invoice_data['tax_rate']}%):")
    c.drawString(width - 100, y - 30, f"${tax:.2f}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(width - 200, y - 45, "Total:")
    c.drawString(width - 100, y - 45, f"${total:.2f}")

    # Footer
    if template in ["professional", "modern", "corporate", "elegant"]:
        c.setFillColor(colors.grey)
        c.rect(0, 0, width, 40, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, 25, "Thank you for your business!")
        c.drawCentredString(
            width / 2,
            10,
            f"{MOCK_DATA['company_info']['name']} - {MOCK_DATA['company_info']['email']}",
        )
    elif template == "uber_receipt":
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width / 2, 30, "Ride completed. Rate your driver!")
        c.setStrokeColor(colors.black)
        c.line(width / 2 - 50, 25, width / 2 + 50, 25)
    elif template == "utility_bill":
        c.setFillColor(colors.lightgreen)
        c.rect(0, 0, width, 50, fill=True)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, 30, "Payment due within 30 days.")
        c.drawCentredString(width / 2, 15, "Contact us at: billing@marscityutils.com")

    c.save()


# Generate preview PDFs at startup
def generate_previews():
    os.makedirs("static/previews", exist_ok=True)
    for template in TEMPLATES.keys():
        invoice_data = generate_random_invoice(template)
        preview_path = f"static/previews/{template}_preview.pdf"
        create_invoice(preview_path, invoice_data, template)


# Home route with previews
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "generate_random" in request.form:
            template = request.form.get("template", "simple")
            invoice_data = generate_random_invoice(template)
        else:
            items = []
            for i in range(int(request.form["item_count"])):
                items.append(
                    {
                        "name": request.form[f"item{i}_name"],
                        "quantity": int(request.form[f"item{i}_quantity"]),
                        "price": float(request.form[f"item{i}_price"]),
                    }
                )
            subtotal = sum(item["quantity"] * item["price"] for item in items)
            tax_rate = float(request.form["tax_rate"])
            tax = subtotal * (tax_rate / 100)
            total = subtotal + tax

            invoice_data = {
                "invoice_number": request.form["invoice_number"],
                "date": request.form["date"],
                "customer_name": request.form["customer_name"],
                "customer_address": request.form["customer_address"],
                "customer_email": request.form["customer_email"],
                "items": items,
                "tax_rate": tax_rate,
                "total": total,
            }
            template = request.form.get("template", "simple")

        pdf_path = f"static/{invoice_data['invoice_number']}-invoice.pdf"
        os.makedirs("static", exist_ok=True)
        create_invoice(pdf_path, invoice_data, template)
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{invoice_data['invoice_number']}-invoice.pdf",
        )

    previews = {
        template: url_for("static", filename=f"previews/{template}_preview.pdf")
        for template in TEMPLATES.keys()
    }
    return render_template("index.html", templates=TEMPLATES, previews=previews)


# Run previews generation at startup
generate_previews()

if __name__ == "__main__":
    app.run(debug=True)
