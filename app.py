"""Simple Python application for final CI/CD validation."""

def my_function(x):
    """Returns 'High' if x > 100, otherwise 'Low'."""
    if x > 100:
        return "High"
    return "Low"

if __name__ == "__main__":
    result = my_function(150)
    print("Application Logic Initialized and Running.")
    print(f"Result for 150: {result}")
