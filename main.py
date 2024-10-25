from fasthtml.common import *
import json

# GPU data
gpus = [
    {
        "model": "H100 80GB",
        "memory": "80 GB HBM3 @ 3.35 TBps",
        "interconnect": "NVLink Full Mesh @ 900 GBps",
        "vws_support": False,
        "best_for": ["Large models", "ML Training", "Inference", "HPC", "BERT", "DLRM"]
    },
    {
        "model": "A100 80GB",
        "memory": "80 GB HBM2e @ 1.9 TBps",
        "interconnect": "NVLink Full Mesh @ 600 GBps",
        "vws_support": False,
        "best_for": ["Large models", "ML Training", "Inference", "HPC", "BERT", "DLRM"]
    },
    {
        "model": "A100 40GB",
        "memory": "40 GB HBM2 @ 1.6 TBps",
        "interconnect": "NVLink Full Mesh @ 600 GBps",
        "vws_support": True,
        "best_for": ["ML Training", "Inference", "HPC"]
    },
    {
        "model": "L4",
        "memory": "24 GB GDDR6 @ 300 GBps",
        "interconnect": "N/A",
        "vws_support": True,
        "best_for": ["ML Inference", "Training", "Remote Visualization Workstations", "Video Transcoding", "HPC"]
    },
    {
        "model": "T4",
        "memory": "16 GB GDDR6 @ 320 GBps",
        "interconnect": "N/A",
        "vws_support": True,
        "best_for": ["ML Inference", "Training", "Remote Visualization Workstations", "Video Transcoding"]
    },
    {
        "model": "V100",
        "memory": "16 GB HBM2 @ 900 GBps",
        "interconnect": "NVLink Ring @ 300 GBps",
        "vws_support": False,
        "best_for": ["ML Training", "Inference", "HPC"]
    },
    {
        "model": "P4",
        "memory": "8 GB GDDR5 @ 192 GBps",
        "interconnect": "N/A",
        "vws_support": True,
        "best_for": ["Remote Visualization", "ML Inference", "Video Transcoding"]
    },
    {
        "model": "P100",
        "memory": "16 GB HBM2 @ 732 GBps",
        "interconnect": "N/A",
        "vws_support": True,
        "best_for": ["ML Training", "Inference", "HPC", "Remote Visualization"]
    }
]

# Set up the FastHTML app
app = FastHTML(
    hdrs=(
        picolink,
        Style("""
            .gpu-card { border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
            .memory-bar { height: 20px; background-color: #4CAF50; margin-bottom: 5px; }
            .best-for { display: flex; flex-wrap: wrap; gap: 5px; padding-bottom: 5px }
            .best-for span { background-color: #ae4c4c; padding: 2px 5px; border-radius: 3px; color: white;}
        """),
        Script("""
            function toggleDetails(id) {
                var details = document.getElementById('details-' + id);
                details.style.display = details.style.display === 'none' ? 'block' : 'none';
            }
        """)
    )
)
rt = app.route

@rt("/")
def get():
    max_memory = max(int(gpu['memory'].split()[0]) for gpu in gpus)
    
    def gpu_card(gpu, index):
        memory_size = int(gpu['memory'].split()[0])
        memory_percentage = (memory_size / max_memory) * 100
        
        return Div(
            H2(gpu['model']),
            Div(f"Memory: {gpu['memory']}"),
            Div(cls="memory-bar", style=f"width: {memory_percentage}%"),
            Div(f"Interconnect: {gpu['interconnect']}"),
            Div(f"NVIDIA RTX Virtual Workstation (vWS) support: {'Yes' if gpu['vws_support'] else 'No'}"),
            Div("Best used for:"),
            Div(cls="best-for", *[Span(use) for use in gpu['best_for']]),
            Button("Toggle Details", onclick=f"toggleDetails({index})"),
            Div(
                Div(f"Memory: {gpu['memory']}"),
                Div(f"Interconnect: {gpu['interconnect']}"),
                Div(f"vWS support: {'Yes' if gpu['vws_support'] else 'No'}"),
                Div("Best used for:"),
                Ul(*[Li(use) for use in gpu['best_for']]),
                id=f"details-{index}", style="display: none;"
            ),
            cls="gpu-card"
        )
    foot = P(f"Source: https://cloud.google.com/compute/docs/gpus")
    content = Div(*[gpu_card(gpu, i) for i, gpu in enumerate(gpus)])
    return Titled("GPU Comparison", content, foot)

@rt("/api/gpus")
def get():
    return json.dumps(gpus)

serve()
