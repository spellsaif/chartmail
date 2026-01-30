"""
📊 Complete Data Processing & Email Automation Pipeline
=====================================================

Educational Python program demonstrating:
- Database operations (SQLite)
- Data manipulation (Pandas)
- Data visualization (Matplotlib)
- File I/O (CSV, Excel, HTML)
- Email automation (SMTP)
- Environment variables for security

Perfect for teaching students real-world data processing workflows!

Author: Educational Demo
Purpose: Teaching complete data pipeline development
"""

import sqlite3      # Built-in database for lightweight data storage
import pandas as pd # Data manipulation and analysis library
import matplotlib.pyplot as plt  # Plotting and visualization library
import smtplib      # Email sending protocol library
import os           # Operating system interface
import base64       # Binary data encoding for embedding images
from email.mime.multipart import MIMEMultipart  # Email structure
from email.mime.text import MIMEText            # Email content
from io import BytesIO  # In-memory binary streams
from dotenv import load_dotenv  # Load environment variables from .env file

# 🔐 LOAD ENVIRONMENT VARIABLES
# This loads sensitive data from .env file instead of hardcoding in source
load_dotenv()

class DataProcessor:
    """
    🎓 EDUCATIONAL CLASS: Complete Data Processing Pipeline
    
    This class demonstrates Object-Oriented Programming principles
    by encapsulating all data processing functionality in one place.
    
    Key OOP Concepts Demonstrated:
    - Encapsulation: All related methods grouped together
    - Constructor: __init__ method for initialization
    - Instance Variables: self.db_name stores object state
    - Method Organization: Each method has a single responsibility
    """
    
    def __init__(self, db_name="sales_data.db"):
        """
        🏗️ CONSTRUCTOR METHOD
        
        Called automatically when creating a new DataProcessor object.
        Sets up the initial state and creates the database.
        
        Args:
            db_name (str): Name of the SQLite database file
        
        Teaching Point: Constructor pattern for object initialization
        """
        self.db_name = db_name  # Instance variable - stores database name
        self.setup_database()   # Automatically create database with sample data
    
    def setup_database(self):
        """
        🗄️ DATABASE SETUP & MOCK DATA CREATION
        
        Creates SQLite database and populates it with sample sales data.
        Demonstrates database operations and SQL commands.
        
        Key Database Concepts:
        - Connection management
        - Table creation with proper data types
        - Batch data insertion
        - SQL injection prevention with parameterized queries
        
        Teaching Points:
        - Always use 'IF NOT EXISTS' to prevent errors
        - Use parameterized queries (?) to prevent SQL injection
        - Close connections to free resources
        """
        # Step 1: Create database connection
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Step 2: Create table with proper schema
        # 'IF NOT EXISTS' prevents errors if table already exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,        -- Auto-incrementing unique identifier
                product_name TEXT,            -- Product name (string data)
                category TEXT,                -- Product category for grouping
                sales_amount REAL,            -- Sales amount (decimal number)
                sale_date TEXT,              -- Date of sale (stored as text)
                region TEXT                  -- Geographic region
            )
        ''')
        
        # Step 3: Create realistic sample data for demonstration
        # This simulates real business data students might encounter
        mock_data = [
            (1, 'Laptop', 'Electronics', 1200.00, '2024-01-15', 'North'),
            (2, 'Phone', 'Electronics', 800.00, '2024-01-16', 'South'),
            (3, 'Desk Chair', 'Furniture', 250.00, '2024-01-17', 'East'),
            (4, 'Monitor', 'Electronics', 300.00, '2024-01-18', 'West'),
            (5, 'Keyboard', 'Electronics', 75.00, '2024-01-19', 'North'),
            (6, 'Table', 'Furniture', 400.00, '2024-01-20', 'South'),
            (7, 'Mouse', 'Electronics', 25.00, '2024-01-21', 'East'),
            (8, 'Bookshelf', 'Furniture', 180.00, '2024-01-22', 'West')
        ]
        
        # Step 4: Insert data using parameterized query (prevents SQL injection)
        # 'OR REPLACE' handles duplicate IDs gracefully
        cursor.executemany('INSERT OR REPLACE INTO sales VALUES (?, ?, ?, ?, ?, ?)', mock_data)
        
        # Step 5: Save changes and close connection
        conn.commit()  # Permanently save the changes
        conn.close()   # Free up system resources
    
    def retrieve_data(self):
        """
        📊 DATA RETRIEVAL FROM DATABASE
        
        Fetches data from SQLite database and converts to Pandas DataFrame.
        Demonstrates the bridge between SQL databases and Python data analysis.
        
        Returns:
            pandas.DataFrame: All sales data in a structured format
        
        Key Concepts:
        - SQL SELECT queries
        - Pandas DataFrame creation from database
        - Connection management best practices
        
        Teaching Point: DataFrames are the foundation of data analysis in Python
        """
        # Create database connection
        conn = sqlite3.connect(self.db_name)
        
        # Execute SQL query and create DataFrame in one step
        # This is more efficient than fetching rows manually
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        
        # Always close connections to prevent resource leaks
        conn.close()
        
        return df  # Return structured data for further processing
    
    def export_to_files(self, df):
        """
        💾 DATA EXPORT TO MULTIPLE FORMATS
        
        Converts DataFrame to CSV and Excel formats for different use cases.
        Demonstrates file I/O operations and format conversion.
        
        Args:
            df (pandas.DataFrame): Data to export
        
        File Formats Explained:
        - CSV: Universal format, readable by any spreadsheet software
        - Excel: Formatted spreadsheet with potential for styling
        
        Teaching Points:
        - Same data, multiple formats for different audiences
        - index=False prevents row numbers in output files
        - Pandas handles file creation automatically
        """
        # Export to CSV (Comma-Separated Values)
        # Universal format that works with Excel, Google Sheets, etc.
        df.to_csv('sales_data.csv', index=False)
        
        # Export to Excel format
        # Preserves data types and allows for future formatting
        df.to_excel('sales_data.xlsx', index=False)
        
        print("✅ Data exported to sales_data.csv and sales_data.xlsx")
    
    def create_charts(self, df):
        """
        📈 DATA VISUALIZATION & CHART CREATION
        
        Creates professional charts and converts them to base64 format
        for embedding in HTML emails. Demonstrates data aggregation and visualization.
        
        Args:
            df (pandas.DataFrame): Source data for visualization
            
        Returns:
            dict: Base64-encoded chart images ready for HTML embedding
        
        Key Visualization Concepts:
        - Data aggregation with groupby()
        - Different chart types for different data stories
        - Memory management with plt.close()
        - Base64 encoding for web compatibility
        
        Teaching Points:
        - Bar charts: Compare quantities across categories
        - Pie charts: Show proportions of a whole
        - Base64: Convert binary data to text for HTML embedding
        """
        charts = {}  # Dictionary to store encoded chart images
        
        # 📊 CHART 1: Sales by Category (Bar Chart)
        # Bar charts are perfect for comparing quantities across categories
        plt.figure(figsize=(10, 6))  # Set chart size for readability
        
        # Data aggregation: Group by category and sum sales amounts
        category_sales = df.groupby('category')['sales_amount'].sum()
        
        # Create bar chart
        plt.bar(category_sales.index, category_sales.values, color=['#2E86AB', '#A23B72', '#F18F01'])
        plt.title('Sales by Category', fontsize=16, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Sales Amount ($)', fontsize=12)
        plt.xticks(rotation=45)  # Rotate labels for better readability
        
        # Convert chart to base64 for HTML embedding
        buffer = BytesIO()  # Create in-memory buffer
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)  # High quality
        buffer.seek(0)  # Reset buffer position
        charts['category_chart'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()  # Free memory - important for preventing memory leaks!
        
        # 🥧 CHART 2: Sales by Region (Pie Chart)
        # Pie charts show proportions and percentages effectively
        plt.figure(figsize=(8, 8))
        
        # Data aggregation: Group by region and sum sales amounts
        region_sales = df.groupby('region')['sales_amount'].sum()
        
        # Create pie chart with custom colors
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        plt.pie(region_sales.values, 
                labels=region_sales.index, 
                autopct='%1.1f%%',  # Show percentages
                colors=colors,
                startangle=90)  # Start from top
        plt.title('Sales Distribution by Region', fontsize=16, fontweight='bold')
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        charts['region_chart'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()  # Always close to prevent memory issues
        
        return charts  # Return dictionary of base64-encoded images
    
    def create_html_report(self, df, charts):
        """
        🌐 HTML REPORT GENERATION
        
        Creates a complete HTML document with embedded charts and data table.
        Demonstrates HTML templating, CSS styling, and data integration.
        
        Args:
            df (pandas.DataFrame): Data for the report
            charts (dict): Base64-encoded chart images
            
        Returns:
            str: Complete HTML document as string
        
        Key Web Development Concepts:
        - HTML document structure
        - CSS styling for professional appearance
        - Base64 data URLs for embedded images
        - F-string templating for dynamic content
        
        Teaching Points:
        - HTML emails need embedded images (not file references)
        - CSS styling makes reports professional
        - F-strings allow mixing Python variables with HTML
        """
        # Calculate summary statistics for the report header
        total_sales = df['sales_amount'].sum()
        transaction_count = len(df)
        
        # 🎨 HTML TEMPLATE WITH EMBEDDED CSS
        # Using f-string for dynamic content insertion
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sales Report - Professional Dashboard</title>
            <style>
                /* 🎨 CSS STYLING FOR PROFESSIONAL APPEARANCE */
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                
                h1 {{ 
                    color: #2c3e50; 
                    text-align: center;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                
                h2 {{ 
                    color: #34495e; 
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                }}
                
                .summary-stats {{
                    display: flex;
                    justify-content: space-around;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                
                .stat-item {{
                    text-align: center;
                }}
                
                .stat-value {{
                    font-size: 2em;
                    font-weight: bold;
                }}
                
                .stat-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                
                table {{ 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 20px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                th, td {{ 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: left; 
                }}
                
                th {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    font-weight: bold;
                }}
                
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                
                tr:hover {{
                    background-color: #e3f2fd;
                }}
                
                .chart {{ 
                    text-align: center; 
                    margin: 30px 0;
                    padding: 20px;
                    background-color: #fafafa;
                    border-radius: 8px;
                }}
                
                .chart img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Sales Performance Report</h1>
                
                <!-- SUMMARY STATISTICS SECTION -->
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-value">${total_sales:,.2f}</div>
                        <div class="stat-label">Total Sales</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{transaction_count}</div>
                        <div class="stat-label">Transactions</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${total_sales/transaction_count:,.2f}</div>
                        <div class="stat-label">Average Sale</div>
                    </div>
                </div>
                
                <!-- CHARTS SECTION -->
                <h2>📈 Visual Analytics</h2>
                
                <div class="chart">
                    <h3>Sales Performance by Category</h3>
                    <img src="data:image/png;base64,{charts['category_chart']}" 
                         alt="Sales by Category Chart">
                    <p><em>Bar chart showing total sales amount for each product category</em></p>
                </div>
                
                <div class="chart">
                    <h3>Regional Sales Distribution</h3>
                    <img src="data:image/png;base64,{charts['region_chart']}" 
                         alt="Sales by Region Chart">
                    <p><em>Pie chart displaying the percentage breakdown of sales by region</em></p>
                </div>
                
                <!-- DATA TABLE SECTION -->
                <h2>📋 Detailed Transaction Data</h2>
                {df.to_html(index=False, classes='data-table', escape=False)}
                
                <!-- FOOTER -->
                <div class="footer">
                    <p>Report generated automatically by Python Data Processing Pipeline</p>
                    <p>📧 This report was created and sent using Python automation</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save HTML file for local viewing/debugging
        with open('sales_report.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_content
    
    def send_email(self, html_content):
        """
        📧 GMAIL EMAIL AUTOMATION WITH MAXIMUM RELIABILITY
        
        Sends HTML report via Gmail SMTP with optimized settings for success.
        Uses App Password authentication for security and reliability.
        
        Args:
            html_content (str): Complete HTML document to send
        
        🔐 GMAIL SECURITY REQUIREMENTS:
        - Must use App Password (not regular password)
        - 2-Factor Authentication must be enabled
        - Less secure app access not needed with App Password
        
        📧 GMAIL CONFIGURATION:
        - SMTP Server: smtp.gmail.com
        - Port: 587 (TLS encryption)
        - Authentication: App Password required
        
        🚨 GUARANTEED SUCCESS STEPS:
        1. Enable 2FA on Gmail account
        2. Generate App Password in Google Account settings
        3. Use App Password in .env file
        4. Ensure internet connection is stable
        """
        
        # 🔐 LOAD GMAIL CONFIGURATION FROM ENVIRONMENT VARIABLES
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD') 
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')  # Default to Gmail
        smtp_port = int(os.getenv('SMTP_PORT', '587'))  # Gmail TLS port
        email_subject = os.getenv('EMAIL_SUBJECT', '📊 Automated Sales Report')
        
        # 🚨 CRITICAL VALIDATION: Check all required variables
        required_vars = ['SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAIL']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print("❌ CRITICAL ERROR: Missing Gmail configuration!")
            print(f"   Missing variables: {', '.join(missing_vars)}")
            print("🔧 GMAIL SETUP REQUIRED:")
            print("   1. Update .env file with your Gmail credentials")
            print("   2. SENDER_EMAIL=your_email@gmail.com")
            print("   3. SENDER_PASSWORD=your_16_char_app_password")
            print("   4. RECIPIENT_EMAIL=destination@email.com")
            print("\\n🚨 IMPORTANT: Use App Password, not regular Gmail password!")
            return False
        
        # 📧 VALIDATE EMAIL FORMAT
        if not sender_email.endswith('@gmail.com'):
            print("⚠️  WARNING: Sender email should be @gmail.com for Gmail SMTP")
            print(f"   Current: {sender_email}")
        
        # 📝 CREATE EMAIL MESSAGE WITH GMAIL-OPTIMIZED HEADERS
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['X-Priority'] = '1'  # High priority
        msg['X-MSMail-Priority'] = 'High'
        
        # 🌐 ATTACH HTML CONTENT
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 🔄 RETRY MECHANISM FOR MAXIMUM RELIABILITY
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"🔗 Attempt {retry_count + 1}/{max_retries}: Connecting to Gmail SMTP...")
                print(f"   Server: {smtp_server}:{smtp_port}")
                
                # 📡 ESTABLISH CONNECTION WITH TIMEOUT
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
                server.set_debuglevel(0)  # Disable debug for clean output
                
                # 🔒 ENABLE TLS ENCRYPTION (REQUIRED FOR GMAIL)
                print("🔒 Enabling TLS encryption...")
                server.starttls()
                print("✅ Secure TLS connection established")
                
                # 🔑 AUTHENTICATE WITH GMAIL
                print("🔑 Authenticating with Gmail...")
                server.login(sender_email, sender_password)
                print("✅ Gmail authentication successful!")
                
                # 📤 SEND EMAIL
                print(f"📤 Sending email to {recipient_email}...")
                server.send_message(msg)
                server.quit()
                
                # 🎉 SUCCESS!
                print("\\n🎉 EMAIL SENT SUCCESSFULLY!")
                print("=" * 50)
                print(f"📧 From: {sender_email}")
                print(f"📧 To: {recipient_email}")
                print(f"📋 Subject: {email_subject}")
                print(f"📊 Content: HTML report with embedded charts")
                print("=" * 50)
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                print(f"❌ AUTHENTICATION FAILED (Attempt {retry_count + 1})!")
                print("🚨 GMAIL APP PASSWORD REQUIRED!")
                print("\\n🔧 STEP-BY-STEP FIX:")
                print("   1. Go to myaccount.google.com")
                print("   2. Click 'Security' in left menu")
                print("   3. Enable '2-Step Verification' if not already enabled")
                print("   4. Click 'App passwords'")
                print("   5. Select 'Mail' and generate password")
                print("   6. Copy the 16-character password to .env file")
                print("   7. Remove spaces: 'abcd efgh ijkl mnop' → 'abcdefghijklmnop'")
                print(f"\\n   Error details: {e}")
                return False
                
            except smtplib.SMTPConnectError as e:
                retry_count += 1
                print(f"❌ CONNECTION FAILED (Attempt {retry_count})!")
                if retry_count < max_retries:
                    print(f"🔄 Retrying in 5 seconds...")
                    import time
                    time.sleep(5)
                else:
                    print("🚨 ALL CONNECTION ATTEMPTS FAILED!")
                    print("🔧 TROUBLESHOOTING:")
                    print("   1. Check internet connection")
                    print("   2. Verify Gmail SMTP settings")
                    print("   3. Check firewall/antivirus blocking port 587")
                    print(f"   Error: {e}")
                    return False
                    
            except Exception as e:
                retry_count += 1
                print(f"❌ UNEXPECTED ERROR (Attempt {retry_count}): {e}")
                if retry_count < max_retries:
                    print("🔄 Retrying...")
                    import time
                    time.sleep(3)
                else:
                    print("🚨 MAXIMUM RETRIES EXCEEDED!")
                    print("💾 HTML report saved as 'sales_report.html'")
                    print("📧 You can manually send this file")
                    return False
        
        return False
    
    def run_complete_process(self):
        """
        🚀 MAIN PIPELINE ORCHESTRATOR
        
        Executes the complete data processing workflow in logical sequence.
        Demonstrates workflow orchestration and process management.
        
        Pipeline Steps:
        1. Data Retrieval → Get data from database
        2. File Export → Save data in multiple formats  
        3. Visualization → Create professional charts
        4. Report Generation → Build HTML document
        5. Email Delivery → Send automated report
        
        Teaching Points:
        - Workflow orchestration: Managing complex multi-step processes
        - Error handling: Each step can fail independently
        - Progress tracking: User feedback during long operations
        - Modular design: Each step is a separate, testable method
        """
        print("🚀 Starting automated data processing pipeline...")
        print("=" * 60)
        
        try:
            # 📊 STEP 1: DATA RETRIEVAL
            print("📊 Step 1: Retrieving data from database...")
            df = self.retrieve_data()
            print(f"   ✅ Successfully retrieved {len(df)} records")
            print(f"   📈 Total sales value: ${df['sales_amount'].sum():,.2f}")
            
            # 💾 STEP 2: FILE EXPORT
            print("\\n💾 Step 2: Exporting data to files...")
            self.export_to_files(df)
            print("   ✅ Data exported to CSV and Excel formats")
            
            # 📈 STEP 3: VISUALIZATION
            print("\\n📈 Step 3: Creating data visualizations...")
            charts = self.create_charts(df)
            print("   ✅ Generated bar chart (Sales by Category)")
            print("   ✅ Generated pie chart (Sales by Region)")
            
            # 🌐 STEP 4: HTML REPORT GENERATION
            print("\\n🌐 Step 4: Building HTML report...")
            html_content = self.create_html_report(df, charts)
            print("   ✅ Professional HTML report created")
            print("   📄 Report saved as 'sales_report.html'")
            
            # 📧 STEP 5: EMAIL DELIVERY
            print("\\n📧 Step 5: Sending email report...")
            email_success = self.send_email(html_content)
            
            if email_success:
                print("   ✅ Email delivered successfully!")
            else:
                print("   ⚠️  Email delivery failed - check configuration")
            
            # 🎉 SUCCESS SUMMARY
            print("\\n" + "=" * 60)
            if email_success:
                print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            else:
                print("⚠️  PIPELINE COMPLETED WITH EMAIL ISSUES")
            print("📋 Summary of outputs:")
            print("   • sales_data.db (SQLite database)")
            print("   • sales_data.csv (CSV export)")
            print("   • sales_data.xlsx (Excel export)")
            print("   • sales_report.html (HTML report)")
            if email_success:
                print("   • Email sent with embedded charts ✅")
            else:
                print("   • Email delivery failed - check .env configuration ⚠️")
            print("=" * 60)
            
        except Exception as e:
            # 🚨 ERROR HANDLING
            print(f"\\n❌ Pipeline failed at step: {e}")
            print("🔧 Check the error message above for debugging information")
            print("💡 Each step is independent - you can run them individually for testing")


# 🎓 EDUCATIONAL DEMONSTRATION
if __name__ == "__main__":
    """
    🎯 MAIN EXECUTION BLOCK
    
    This block only runs when the script is executed directly,
    not when imported as a module. Perfect for demonstrations!
    
    Teaching Points:
    - if __name__ == "__main__": Python idiom for script execution
    - Object instantiation and method calling
    - Complete workflow demonstration
    """
    print("🎓 EDUCATIONAL DATA PROCESSING PIPELINE")
    print("=====================================")
    print("This program demonstrates a complete real-world data workflow:")
    print("Database → Analysis → Visualization → Reporting → Email Automation")
    print("\\nStarting demonstration...\\n")
    
    # Create DataProcessor instance and run complete workflow
    processor = DataProcessor()
    processor.run_complete_process()
    
    print("\\n🎓 LEARNING COMPLETE!")
    print("Students can now understand how data flows through a complete pipeline!")