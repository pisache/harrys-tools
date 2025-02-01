import sys
import os
import win32com.client as win32

class ToPDF: 

    def convert():
        if len(sys.argv) < 2:
            print("Usage: python toPDF.py <output.xlsx>")
            sys.exit(1)

        # The path to your already-created Excel file (output.xlsx)
        excel_file = sys.argv[1]

        # Create a subfolder named "개별학습확인표" in the same directory as toPDF.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_folder = os.path.join(script_dir, "개별학습확인표")

        # Make the folder if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Absolute path to the Excel file
        excel_file_path = os.path.abspath(excel_file)

        if not os.path.exists(excel_file_path):
            print(f"Error: File '{excel_file_path}' does not exist.")
            sys.exit(1)

        # Start Excel via COM automation
        excel_app = win32.Dispatch("Excel.Application")
        excel_app.Visible = False  # Run in background

        # Open the workbook
        try:
            wb = excel_app.Workbooks.Open(excel_file_path)
        except Exception as e:
            print(f"Error opening '{excel_file_path}' in Excel: {e}")
            excel_app.Quit()
            sys.exit(1)

        # Constants for ExportAsFixedFormat
        xlTypePDF = 0  # PDF format

        # Iterate through each sheet in the workbook
        for sh in wb.Sheets:
            sheet_name = sh.Name

            # Create a PDF file name based on the sheet name
            pdf_name = f"{sheet_name}.pdf"
            pdf_path = os.path.join(save_folder, pdf_name)

            # Export the sheet to PDF
            try:
                sh.ExportAsFixedFormat(xlTypePDF, pdf_path)
                print(f"Exported sheet '{sheet_name}' to PDF => {pdf_path}")
            except Exception as e:
                print(f"Failed to export sheet '{sheet_name}' to PDF: {e}")

        # Close the workbook without saving changes
        wb.Close(False)
        # Quit Excel
        excel_app.Quit()

        print("All sheets have been exported to PDF in the folder '개별학습확인표'.")