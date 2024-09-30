import json

class ReportGenerator:
    def __init__(self, report_data):
        """
        Initializes the ReportGenerator with the collected report data.
        :param report_data: A dictionary containing all analysis results.
        """
        self.report_data = report_data

    def generate_json_report(self, output_file='report.json'):
        """
        Generates a JSON report and saves it to the specified file.
        :param output_file: The filename for the output JSON report.
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(self.report_data, f, indent=4)
            print(f"Report saved to {output_file}")
        except Exception as e:
            print(f"Error saving report: {e}")