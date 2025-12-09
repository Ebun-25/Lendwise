from backend.repository import generate_reports

def view_reports():
    data = generate_reports()
    output = [f"{key}: {value}" for key, value in data.items()]
    return output
