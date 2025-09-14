import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64

def generate_dummy_chart(title: str, labels=None, values=None) -> str:
    """
    Generates a dummy bar chart and returns it as a base64-encoded PNG data URL.
    """
    if labels is None:
        labels = ["A", "B", "C"]
    if values is None:
        values = [10, 20, 30]

    plt.figure(figsize=(4, 3))
    plt.bar(labels, values, color="skyblue")
    plt.title(title)

    # Save chart to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Encode as base64 and return as a data URL
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"
